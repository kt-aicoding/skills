#!/usr/bin/env python3
"""Compare active Claude Code and Codex skills without reading source prompts aloud."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType


SLASH_COMMAND_RE = re.compile(r"(?<!\S)/([a-zA-Z0-9:_-]+)")


@dataclass(frozen=True)
class ClaudeSkill:
    name: str
    folder: str
    path: Path
    description: str
    declared_name: bool
    sha256: str
    body_sha256: str


def parse_args() -> argparse.Namespace:
    repository = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Audit Claude Code to Codex skill parity and migration decisions."
    )
    parser.add_argument(
        "--claude-root",
        type=Path,
        default=Path.home() / ".claude",
        help="Claude Code user directory.",
    )
    parser.add_argument(
        "--codex-root",
        action="append",
        type=Path,
        help="Codex skill root. Repeat for multiple roots.",
    )
    parser.add_argument(
        "--codex-config",
        type=Path,
        default=Path.home() / ".codex" / "config.toml",
    )
    parser.add_argument(
        "--mapping",
        type=Path,
        default=repository / "config" / "claude-to-codex-skill-map.json",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repository / "reports" / "CC_CODEX_SKILL_PARITY.md",
        help="Output file. Use '-' for stdout.",
    )
    return parser.parse_args()


def load_audit_module() -> ModuleType:
    path = Path(__file__).resolve().with_name("audit-codex-skills.py")
    spec = importlib.util.spec_from_file_location("codex_skill_audit_for_parity", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load audit module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def body_hash(text: str) -> str:
    lines = text.splitlines()
    body = text
    if lines and lines[0].strip() == "---":
        for index, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                body = "\n".join(lines[index + 1 :])
                break
    normalized = "\n".join(line.rstrip() for line in body.strip().splitlines())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def scan_claude_skills(root: Path, audit_module: ModuleType) -> tuple[list[ClaudeSkill], list[str]]:
    skills_root = root / "skills"
    skills: list[ClaudeSkill] = []
    for path in sorted(skills_root.glob("*/SKILL.md")):
        try:
            text = path.read_text(encoding="utf-8")
            values, _ = audit_module.parse_frontmatter(text)
        except (OSError, UnicodeError, ValueError):
            continue
        declared_name = bool(values.get("name", "").strip())
        name = values.get("name", "").strip() or path.parent.name
        skills.append(
            ClaudeSkill(
                name=name,
                folder=path.parent.name,
                path=path,
                description=values.get("description", "").strip(),
                declared_name=declared_name,
                sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
                body_sha256=body_hash(text),
            )
        )
    broken = sorted(
        entry.name
        for entry in skills_root.iterdir()
        if entry.is_symlink() and not entry.exists()
    ) if skills_root.is_dir() else []
    return skills, broken


def claude_explicit_usage(history: Path, known_names: set[str]) -> dict[str, dict[str, int]]:
    sessions: dict[str, set[str]] = defaultdict(set)
    invocations: Counter[str] = Counter()
    if not history.is_file():
        return {}
    for line in history.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(row, dict):
            continue
        text = str(row.get("display", ""))
        session_id = str(row.get("sessionId", ""))
        for raw_name in SLASH_COMMAND_RE.findall(text):
            name = raw_name.rsplit(":", 1)[-1]
            if name not in known_names:
                continue
            invocations[name] += 1
            sessions[name].add(session_id)
    return {
        name: {"sessions": len(sessions[name]), "invocations": invocations[name]}
        for name in sorted(invocations)
    }


def plugin_summary(claude_root: Path) -> dict[str, object]:
    installed_path = claude_root / "plugins" / "installed_plugins.json"
    settings_path = claude_root / "settings.json"
    try:
        installed_data = json.loads(installed_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        installed_data = {}
    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        settings = {}
    plugins = installed_data.get("plugins", {}) if isinstance(installed_data, dict) else {}
    enabled_map = settings.get("enabledPlugins", {}) if isinstance(settings, dict) else {}
    installed_names = sorted(plugins) if isinstance(plugins, dict) else []
    enabled_names = sorted(
        name
        for name in installed_names
        if isinstance(enabled_map, dict) and enabled_map.get(name) is True
    )
    return {
        "installed": len(installed_names),
        "enabled": len(enabled_names),
        "disabled": len(installed_names) - len(enabled_names),
        "enabled_names": enabled_names,
    }


def build_report(args: argparse.Namespace) -> dict:
    audit_module = load_audit_module()
    codex_roots = args.codex_root or [
        Path.home() / ".agents" / "skills",
        Path.home() / ".codex" / "skills",
    ]
    codex_report = audit_module.audit(codex_roots, args.codex_config, False, 140)
    codex_skills = codex_report["skills"]
    codex_by_name = {skill["name"]: skill for skill in codex_skills}

    claude_skills, broken = scan_claude_skills(args.claude_root, audit_module)
    claude_by_name: dict[str, list[ClaudeSkill]] = defaultdict(list)
    for skill in claude_skills:
        claude_by_name[skill.name].append(skill)

    mapping = json.loads(args.mapping.read_text(encoding="utf-8"))
    shared_names = sorted(set(claude_by_name) & set(codex_by_name))
    shared: list[dict[str, object]] = []
    for name in shared_names:
        codex = codex_by_name[name]
        matches = claude_by_name[name]
        if any(skill.sha256 == codex["sha256"] for skill in matches):
            parity = "exact"
        else:
            codex_text = Path(codex["path"]).read_text(encoding="utf-8")
            parity = (
                "same-body"
                if any(skill.body_sha256 == body_hash(codex_text) for skill in matches)
                else "modified"
            )
        shared.append({"name": name, "parity": parity})

    claude_only_names = sorted(set(claude_by_name) - set(codex_by_name))
    missing_mapping = sorted(set(claude_only_names) - set(mapping))
    stale_mapping = sorted(set(mapping) - set(claude_only_names))
    decisions = []
    for name in claude_only_names:
        item = mapping.get(
            name,
            {"decision": "unmapped", "targets": [], "notes": "Needs a migration decision."},
        )
        decisions.append({"name": name, **item})

    command_files = [
        path
        for path in (args.claude_root / "commands").glob("*.md")
        if path.stem != "README"
    ]
    agent_files = list((args.claude_root / "agents").glob("*.md"))
    known_usage_names = set(claude_by_name) | {path.stem for path in command_files}
    usage = claude_explicit_usage(args.claude_root / "history.jsonl", known_usage_names)

    duplicate_names = [
        {"name": name, "folders": sorted(skill.folder for skill in skills)}
        for name, skills in sorted(claude_by_name.items())
        if len(skills) > 1
    ]
    missing_declared_name = sorted(
        skill.folder for skill in claude_skills if not skill.declared_name
    )
    parity_counts = Counter(str(item["parity"]) for item in shared)
    decision_counts = Counter(str(item["decision"]) for item in decisions)
    return {
        "summary": {
            "claude_skill_entries": len(claude_skills),
            "claude_unique_skills": len(claude_by_name),
            "codex_active_skills": len(codex_skills),
            "shared_names": len(shared_names),
            "claude_only": len(claude_only_names),
            "codex_only": len(set(codex_by_name) - set(claude_by_name)),
            "claude_commands": len(command_files),
            "claude_subagents": len(agent_files),
            "parity": dict(sorted(parity_counts.items())),
            "decisions": dict(sorted(decision_counts.items())),
            "missing_mapping": missing_mapping,
            "stale_mapping": stale_mapping,
        },
        "plugins": plugin_summary(args.claude_root),
        "claude_metadata": {
            "duplicate_names": duplicate_names,
            "missing_declared_name": missing_declared_name,
            "broken_symlinks": broken,
        },
        "claude_explicit_usage": usage,
        "shared": shared,
        "claude_only": decisions,
        "codex_only": sorted(set(codex_by_name) - set(claude_by_name)),
    }


def table(headers: list[str], rows: list[list[object]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(str(cell) for cell in row) + " |" for row in rows)
    return lines


def render_markdown(report: dict) -> str:
    summary = report["summary"]
    plugins = report["plugins"]
    metadata = report["claude_metadata"]
    usage_rows = sorted(
        (
            [name, values["sessions"], values["invocations"]]
            for name, values in report["claude_explicit_usage"].items()
        ),
        key=lambda row: (-int(row[1]), -int(row[2]), str(row[0])),
    )
    lines = [
        "# Claude Code and Codex Skill Parity",
        "",
        "This report compares active top-level Claude Code skills with enabled Codex skills. "
        "It stores names and aggregate counts only; it does not include prompts or credentials.",
        "",
        "## Summary",
        "",
        f"- Claude skill entries: {summary['claude_skill_entries']}",
        f"- Claude unique skill names: {summary['claude_unique_skills']}",
        f"- Codex enabled skills: {summary['codex_active_skills']}",
        f"- Shared names: {summary['shared_names']}",
        f"- Claude-only names: {summary['claude_only']}",
        f"- Codex-only names: {summary['codex_only']}",
        f"- Claude commands: {summary['claude_commands']}",
        f"- Claude subagents: {summary['claude_subagents']}",
        f"- Claude plugins: {plugins['installed']} installed, {plugins['enabled']} enabled, {plugins['disabled']} disabled",
        "",
        "A full Claude-to-Codex migration is unsafe here because it would overwrite shared "
        "Codex skills that already have native policy and metadata. Use the decisions below "
        "instead of copying the entire Claude directory.",
        "",
        "## Shared skill parity",
        "",
    ]
    parity_rows = [[key, value] for key, value in summary["parity"].items()]
    lines.extend(table(["Parity", "Skills"], parity_rows))

    lines.extend(["", "## Claude explicit usage evidence", ""])
    lines.extend(
        table(["Skill", "Sessions", "Invocations"], usage_rows)
        if usage_rows
        else ["No matching explicit skill invocations were found in retained Claude history."]
    )

    for decision in ("covered", "native", "defer", "retire", "unmapped"):
        rows = [item for item in report["claude_only"] if item["decision"] == decision]
        if not rows:
            continue
        lines.extend(["", f"## Claude-only: {decision}", ""])
        lines.extend(
            table(
                ["Claude Skill", "Codex target", "Decision notes"],
                [
                    [
                        item["name"],
                        ", ".join(item["targets"]) if item["targets"] else "—",
                        item["notes"],
                    ]
                    for item in rows
                ],
            )
        )

    lines.extend(["", "## Claude metadata findings", ""])
    lines.append(
        f"- Missing declared `name` (directory fallback used): "
        f"{', '.join(metadata['missing_declared_name']) or 'none'}"
    )
    lines.append(
        f"- Broken top-level symlinks: {', '.join(metadata['broken_symlinks']) or 'none'}"
    )
    duplicate_text = "; ".join(
        f"{item['name']} ({', '.join(item['folders'])})"
        for item in metadata["duplicate_names"]
    )
    lines.append(f"- Duplicate Claude names: {duplicate_text or 'none'}")

    lines.extend(["", "## Codex-only skills", ""])
    lines.append(", ".join(f"`{name}`" for name in report["codex_only"]))
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
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
    missing = report["summary"]["missing_mapping"]
    stale = report["summary"]["stale_mapping"]
    if missing or stale:
        if missing:
            print("Missing mappings: " + ", ".join(missing))
        if stale:
            print("Stale mappings: " + ", ".join(stale))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
