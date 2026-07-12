#!/usr/bin/env python3
"""Aggregate privacy-preserving Codex skill usage from retained local sessions."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType
from typing import Iterable


EXPLICIT_SKILL_RE = re.compile(r"\$([a-z0-9][a-z0-9-]{0,63})\b")
SKILL_FILE_RE = re.compile(r"(?:^|[/\\])([a-z0-9][a-z0-9-]{0,63})[/\\]SKILL\.md\b")


@dataclass
class Usage:
    sessions: set[str] = field(default_factory=set)
    primary_sessions: set[str] = field(default_factory=set)
    subagent_sessions: set[str] = field(default_factory=set)
    explicit_sessions: set[str] = field(default_factory=set)
    file_read_sessions: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class SessionEvidence:
    session_id: str
    timestamp: str
    is_subagent: bool
    explicit_skills: frozenset[str]
    file_read_skills: frozenset[str]


def parse_args() -> argparse.Namespace:
    repository = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description=(
            "Count skill invocations per retained Codex session without emitting prompts, "
            "tool output, or working directories."
        )
    )
    parser.add_argument(
        "--sessions-root",
        type=Path,
        default=Path.home() / ".codex" / "sessions",
        help="Codex rollout directory to scan.",
    )
    parser.add_argument(
        "--root",
        action="append",
        type=Path,
        help="Skill root to scan. Repeat for multiple roots.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path.home() / ".codex" / "config.toml",
        help="Codex config used to exclude disabled skills.",
    )
    parser.add_argument(
        "--frequent-threshold",
        type=int,
        default=5,
        help="Sessions required for the frequent tier (default: 5).",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format (default: markdown).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repository / "reports" / "CODEX_SKILL_USAGE.md",
        help="Output file. Use '-' for stdout.",
    )
    return parser.parse_args()


def load_audit_module() -> ModuleType:
    path = Path(__file__).resolve().with_name("audit-codex-skills.py")
    spec = importlib.util.spec_from_file_location("codex_skill_audit", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load audit module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def strings(value: object) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)


def session_evidence(path: Path, installed_names: set[str]) -> SessionEvidence | None:
    session_id = path.stem
    timestamp = ""
    is_subagent = False
    explicit: set[str] = set()
    file_reads: set[str] = set()

    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None

    for line in lines:
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(record, dict):
            continue
        payload = record.get("payload")
        if not isinstance(payload, dict):
            continue

        if record.get("type") == "session_meta":
            session_id = str(payload.get("session_id") or payload.get("id") or session_id)
            timestamp = str(payload.get("timestamp") or record.get("timestamp") or "")
            is_subagent = isinstance(payload.get("source"), dict)
            continue

        if record.get("type") != "response_item":
            continue

        payload_type = payload.get("type")
        if payload_type == "message" and payload.get("role") == "user":
            for text in strings(payload.get("content")):
                explicit.update(EXPLICIT_SKILL_RE.findall(text))
        elif payload_type in {"custom_tool_call", "function_call"}:
            for text in strings(payload.get("input")):
                file_reads.update(SKILL_FILE_RE.findall(text))

    explicit.intersection_update(installed_names)
    file_reads.intersection_update(installed_names)
    return SessionEvidence(
        session_id=session_id,
        timestamp=timestamp,
        is_subagent=is_subagent,
        explicit_skills=frozenset(explicit),
        file_read_skills=frozenset(file_reads),
    )


def usage_tier(sessions: int, frequent_threshold: int) -> str:
    if sessions >= frequent_threshold:
        return "frequent"
    if sessions >= 2:
        return "used"
    if sessions == 1:
        return "rare"
    return "no-evidence"


def review_signal(skill: dict, usage: Usage, frequent_threshold: int) -> str:
    count = len(usage.sessions)
    implicit = bool(skill["allow_implicit_invocation"])
    if implicit and count >= frequent_threshold and len(skill["description"]) > 140:
        return "shorten-frequent-description"
    if not implicit and count >= frequent_threshold:
        return "review-explicit-only"
    if implicit and count == 0:
        return "review-unused-implicit"
    return "keep"


def build_report(args: argparse.Namespace) -> dict:
    audit_module = load_audit_module()
    roots = args.root or [Path.home() / ".agents" / "skills", Path.home() / ".codex" / "skills"]
    audit = audit_module.audit(roots, args.config, False, 140)
    skills = audit["skills"]
    names = {skill["name"] for skill in skills}
    usage = {name: Usage() for name in names}

    session_files = sorted(args.sessions_root.expanduser().glob("**/*.jsonl"))
    sessions: list[SessionEvidence] = []
    for path in session_files:
        evidence = session_evidence(path, names)
        if evidence is None:
            continue
        sessions.append(evidence)
        touched = evidence.explicit_skills | evidence.file_read_skills
        for name in touched:
            item = usage[name]
            item.sessions.add(evidence.session_id)
            if evidence.is_subagent:
                item.subagent_sessions.add(evidence.session_id)
            else:
                item.primary_sessions.add(evidence.session_id)
        for name in evidence.explicit_skills:
            usage[name].explicit_sessions.add(evidence.session_id)
        for name in evidence.file_read_skills:
            usage[name].file_read_sessions.add(evidence.session_id)

    rows: list[dict[str, object]] = []
    for skill in skills:
        item = usage[skill["name"]]
        count = len(item.sessions)
        rows.append(
            {
                "name": skill["name"],
                "sessions": count,
                "primary_sessions": len(item.primary_sessions),
                "subagent_sessions": len(item.subagent_sessions),
                "explicit_sessions": len(item.explicit_sessions),
                "file_read_sessions": len(item.file_read_sessions),
                "tier": usage_tier(count, args.frequent_threshold),
                "invocation": (
                    "implicit" if skill["allow_implicit_invocation"] else "explicit-only"
                ),
                "description_chars": len(skill["description"]),
                "signal": review_signal(skill, item, args.frequent_threshold),
            }
        )
    rows.sort(key=lambda row: (-int(row["sessions"]), str(row["name"])))

    timestamps = sorted(session.timestamp for session in sessions if session.timestamp)
    tiers = Counter(str(row["tier"]) for row in rows)
    signals = Counter(str(row["signal"]) for row in rows)
    return {
        "summary": {
            "retained_sessions": len(sessions),
            "primary_sessions": sum(not session.is_subagent for session in sessions),
            "subagent_sessions": sum(session.is_subagent for session in sessions),
            "window_start": timestamps[0] if timestamps else None,
            "window_end": timestamps[-1] if timestamps else None,
            "installed_skills": len(skills),
            "frequent_threshold": args.frequent_threshold,
            "tiers": dict(sorted(tiers.items())),
            "signals": dict(sorted(signals.items())),
        },
        "skills": rows,
    }


def markdown_table(rows: list[dict[str, object]]) -> list[str]:
    lines = [
        "| Skill | Sessions | Primary | Explicit | Reads | Policy | Description | Signal |",
        "| --- | ---: | ---: | ---: | ---: | --- | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| {name} | {sessions} | {primary_sessions} | {explicit_sessions} | "
            "{file_read_sessions} | {invocation} | {description_chars} | {signal} |".format(
                **row
            )
        )
    return lines


def render_markdown(report: dict) -> str:
    summary = report["summary"]
    rows = report["skills"]
    frequent = [row for row in rows if row["tier"] == "frequent"]
    description_review = [
        row for row in rows if row["signal"] == "shorten-frequent-description"
    ]
    policy_review = [row for row in rows if row["signal"] == "review-explicit-only"]
    unused_implicit = [row for row in rows if row["signal"] == "review-unused-implicit"]

    lines = [
        "# Codex Skill Usage Audit",
        "",
        (
            f"Evidence window: `{summary['window_start']}` to `{summary['window_end']}`. "
            f"Retained sessions: **{summary['retained_sessions']}** "
            f"({summary['primary_sessions']} primary, {summary['subagent_sessions']} subagent)."
        ),
        "",
        (
            "This report stores aggregate session counts only. It does not include prompts, "
            "tool output, working directories, or session identifiers. A session counts as "
            "usage when the user explicitly mentions `$skill` or Codex reads that skill's "
            "`SKILL.md`. `no-evidence` means no match in retained logs, not that the skill was "
            "never used."
        ),
        "",
        "## Summary",
        "",
        f"- Installed and enabled skills: {summary['installed_skills']}",
        f"- Frequent threshold: {summary['frequent_threshold']} sessions",
    ]
    for tier, count in summary["tiers"].items():
        lines.append(f"- {tier}: {count}")

    lines.extend(["", "## Frequent skills", ""])
    lines.extend(markdown_table(frequent) if frequent else ["No frequent skills found."])

    lines.extend(["", "## Review signals", "", "### Frequent descriptions over 140 chars", ""])
    lines.extend(
        markdown_table(description_review)
        if description_review
        else ["No frequent implicit descriptions exceed 140 characters."]
    )
    lines.extend(["", "### Frequently used explicit-only skills", ""])
    lines.extend(
        markdown_table(policy_review)
        if policy_review
        else ["No explicit-only skill crossed the frequent threshold."]
    )
    lines.extend(["", "### Implicit skills with no retained evidence", ""])
    lines.extend(markdown_table(unused_implicit) if unused_implicit else ["None."])

    lines.extend(["", "## Complete inventory", ""])
    lines.extend(markdown_table(rows))
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    if args.frequent_threshold < 1:
        raise SystemExit("--frequent-threshold must be at least 1")
    report = build_report(args)
    rendered = (
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if args.format == "json"
        else render_markdown(report)
    )
    if str(args.output) == "-":
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
