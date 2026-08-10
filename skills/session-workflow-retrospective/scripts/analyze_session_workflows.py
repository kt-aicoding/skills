#!/usr/bin/env python3
"""Aggregate private local session history into workflow and tooling signals."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import re
import shutil
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CATEGORY_DEFINITIONS = {
    "iterative-review": (
        r"继续|复核|再看|还有|完善|优化|检查|continue|review|audit|verify",
        ("implementation-workflow", "investigate", "review", "checkpoint"),
    ),
    "workspace-organization": (
        r"整理|归类|归档|索引|目录|工作区|workspace|inventory|catalog",
        ("project-workspace-triage", "workspace-noise-cleanup"),
    ),
    "skill-governance": (
        r"\bskill(?:s)?\b|技能|工作流|workflow|经验|沉淀",
        ("skill-creator", "kt-aicoding-registry"),
    ),
    "cli-mcp-tooling": (
        r"\bcli\b|\bmcp\b|命令行|工具|安装|插件|plugin",
        ("cli-tooling-inventory", "cli-tooling-governance", "mcp-surface-governance"),
    ),
    "web-ui": (
        r"网站|网页|前端|页面|\bhtml\b|\breact\b|next\.js|\bvite\b|frontend|responsive",
        ("frontend-design", "web-design-guidelines", "design-review"),
    ),
    "research-reference": (
        r"调研|研究|查找|查询|搜索|资料|官方|文档|research|search|look\s+up|documentation",
        ("source-backed-research",),
    ),
    "test-verification": (
        r"测试|验证|复现|\btest(?:s|ing)?\b|verify|typecheck|\blint\b|\bbuild\b|smoke",
        ("implementation-workflow", "investigate", "vercel:verification"),
    ),
    "deploy-cloud": (
        r"部署|发布|上线|\bdeploy|production|\bvercel\b|\bsupabase\b|cloudbase|cloudflare",
        ("deploy-to-vercel", "land-and-deploy", "wrangler", "supabase:supabase"),
    ),
    "git-delivery": (
        r"\bcommit\b|提交|\bpush\b|\bpull request\b|\bpr\b|\bmerge\b|合并|\bgithub\b",
        ("implementation-workflow", "github:yeet", "github:github"),
    ),
    "media-production": (
        r"图片|图像|视频|音频|字幕|image|video|audio|media|subtitle",
        ("media-production-pipeline",),
    ),
}

CATEGORY_SUPPORT = {
    "research-reference": ("browse", "openai-docs"),
    "media-production": ("anycap-cli", "imagegen"),
}

CLI_NAMES = (
    "act",
    "actionlint",
    "adb",
    "anycap",
    "bats",
    "bun",
    "claude",
    "clawhub",
    "cloudbase-mcp",
    "codex",
    "context7-mcp",
    "curl",
    "docker",
    "ffmpeg",
    "ffprobe",
    "flutter",
    "flyctl",
    "gh",
    "git",
    "gitleaks",
    "go",
    "jq",
    "lark-cli",
    "lhci",
    "lychee",
    "markdownlint-cli2",
    "mcporter",
    "mcp-inspector",
    "mcp-suite-verify",
    "mvn",
    "netlify",
    "node",
    "npm",
    "npx",
    "openclaw",
    "osv-scanner",
    "pipx",
    "playwright",
    "playwright-mcp",
    "pnpm",
    "python",
    "railway",
    "rg",
    "ruff",
    "semgrep",
    "serve",
    "shellcheck",
    "shfmt",
    "supabase",
    "tcb",
    "trivy",
    "tsc",
    "tsx",
    "ty",
    "uv",
    "vercel",
    "wrangler",
    "xcodebuild",
    "yq",
)

HANDOFF_CONCEPTS = {
    "resume-entry": re.compile(r"恢复|继续|resume|from here", re.IGNORECASE),
    "current-state": re.compile(r"当前|状态|current|state", re.IGNORECASE),
    "completed-decisions": re.compile(r"完成|结论|决定|completed|decision|done", re.IGNORECASE),
    "verification-evidence": re.compile(r"验证|证据|资料|来源|validation|evidence|checks", re.IGNORECASE),
    "remaining-next": re.compile(r"仍需|剩余|待办|后续|下一|pending|remaining|next", re.IGNORECASE),
    "risk-blocker": re.compile(r"风险|阻塞|注意|blocker|risk", re.IGNORECASE),
    "files-git-state": re.compile(r"文件|git|branch|commit|artifact", re.IGNORECASE),
}

HANDOFF_FILE_RE = re.compile(r"(?:session.*(?:handoff|summary)|handoff|checkpoint)", re.IGNORECASE)
CACHE_VERSION = 1

PUBLIC_MCP_PROVIDERS = {
    "context7",
    "github",
    "openaiDeveloperDocs",
    "playwright",
    "supabase",
    "vercel",
}


@dataclass
class ParseStats:
    files: int = 0
    records: int = 0
    malformed_lines: int = 0
    cached_files: int = 0


@dataclass
class PatternStats:
    prompts: Counter[str] = field(default_factory=Counter)
    sessions: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    dates: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    total_prompts: int = 0
    distinct_sessions: set[str] = field(default_factory=set)
    window_start: datetime | None = None
    window_end: datetime | None = None


@dataclass
class ToolStats:
    calls: Counter[str] = field(default_factory=Counter)
    sessions: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    surfaces: Counter[str] = field(default_factory=Counter)
    surface_sessions: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))


def opaque_id(provider: str, value: object) -> str:
    raw = f"{provider}:{value or 'unknown'}".encode()
    return hashlib.sha256(raw).hexdigest()


def cache_key(provider: str, path: Path) -> str:
    return opaque_id(provider, path.resolve())


def load_tool_cache(path: Path) -> dict[str, dict[str, object]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(payload, dict) or payload.get("version") != CACHE_VERSION:
        return {}
    entries = payload.get("entries")
    return entries if isinstance(entries, dict) else {}


def save_tool_cache(path: Path, entries: dict[str, dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.with_suffix(path.suffix + ".lock")
    with lock_path.open("a", encoding="utf-8") as lock:
        lock_path.chmod(0o600)
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        merged_entries = load_tool_cache(path)
        merged_entries.update(entries)
        temporary: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=path.parent,
                prefix=f".{path.name}.",
                suffix=".tmp",
                delete=False,
            ) as handle:
                json.dump(
                    {"version": CACHE_VERSION, "entries": merged_entries},
                    handle,
                    sort_keys=True,
                )
                temporary = Path(handle.name)
            temporary.chmod(0o600)
            temporary.replace(path)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def cached_file_evidence(
    provider: str,
    path: Path,
    entries: dict[str, dict[str, object]] | None,
) -> tuple[str, dict[str, object]] | None:
    if entries is None:
        return None
    key = cache_key(provider, path)
    evidence = entries.get(key)
    if not isinstance(evidence, dict):
        return None
    try:
        stat = path.stat()
    except OSError:
        return None
    if evidence.get("size") != stat.st_size or evidence.get("mtime_ns") != stat.st_mtime_ns:
        return None
    return key, evidence


def apply_file_evidence(tools: ToolStats, stats: ParseStats, evidence: dict[str, object]) -> bool:
    stats.files += 1
    stats.records += int(evidence.get("records", 0))
    stats.malformed_lines += int(evidence.get("malformed_lines", 0))
    stats.cached_files += 1
    if not evidence.get("primary"):
        return False
    session = str(evidence.get("session") or "unknown")
    calls = evidence.get("calls")
    if isinstance(calls, dict):
        for name, count in calls.items():
            tools.calls[str(name)] += int(count)
            tools.sessions[str(name)].add(session)
    surfaces = evidence.get("surfaces")
    if isinstance(surfaces, dict):
        for name, count in surfaces.items():
            tools.surfaces[str(name)] += int(count)
            tools.surface_sessions[str(name)].add(session)
    return True


def merge_tool_stats_into(target: ToolStats, source: ToolStats) -> None:
    target.calls.update(source.calls)
    target.surfaces.update(source.surfaces)
    for name, sessions in source.sessions.items():
        target.sessions[name].update(sessions)
    for name, sessions in source.surface_sessions.items():
        target.surface_sessions[name].update(sessions)


def file_evidence(
    path: Path,
    before: object,
    primary: bool,
    session: str,
    tools: ToolStats,
    records: int,
    malformed_lines: int,
) -> dict[str, object] | None:
    try:
        after = path.stat()
    except OSError:
        return None
    if after.st_size != before.st_size or after.st_mtime_ns != before.st_mtime_ns:
        return None
    return {
        "size": after.st_size,
        "mtime_ns": after.st_mtime_ns,
        "primary": primary,
        "session": session,
        "calls": dict(tools.calls),
        "surfaces": dict(tools.surfaces),
        "records": records,
        "malformed_lines": malformed_lines,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Aggregate recurring workflow and tool signals without emitting prompts, "
            "commands, outputs, paths, or session identifiers."
        )
    )
    parser.add_argument(
        "--codex-sessions",
        type=Path,
        default=Path.home() / ".codex" / "sessions",
    )
    parser.add_argument(
        "--codex-history",
        type=Path,
        default=Path.home() / ".codex" / "history.jsonl",
    )
    parser.add_argument(
        "--claude-projects",
        type=Path,
        default=Path.home() / ".claude" / "projects",
    )
    parser.add_argument(
        "--claude-history",
        type=Path,
        default=Path.home() / ".claude" / "history.jsonl",
    )
    parser.add_argument(
        "--skill-root",
        action="append",
        type=Path,
        help="Installed Skill root. Repeat as needed.",
    )
    parser.add_argument(
        "--handoff-root",
        action="append",
        type=Path,
        default=[],
        help="Root containing handoff/summary Markdown files. Repeat as needed.",
    )
    parser.add_argument(
        "--tool-inventory",
        type=Path,
        help="Optional Markdown inventory used to flag undocumented referenced CLIs.",
    )
    parser.add_argument(
        "--since",
        type=str,
        help="Only include evidence on or after YYYY-MM-DD.",
    )
    parser.add_argument(
        "--candidate-threshold",
        type=int,
        default=3,
        help="Minimum primary sessions for a promotion signal (default: 3).",
    )
    parser.add_argument(
        "--cache",
        type=Path,
        default=Path.home()
        / ".cache"
        / "session-workflow-retrospective"
        / "tool-evidence-v1.json",
        help="Local aggregate tool-evidence cache used for unchanged session files.",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Read every session file and do not update the aggregate cache.",
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=str, default="-", help="Output path or '-' for stdout.")
    return parser.parse_args()


def parse_since(value: str | None) -> datetime | None:
    if not value:
        return None
    parsed = datetime.strptime(value, "%Y-%m-%d")
    return parsed.replace(tzinfo=timezone.utc)


def parse_timestamp(value: object) -> datetime | None:
    if isinstance(value, (int, float)):
        seconds = float(value)
        if seconds > 10_000_000_000:
            seconds /= 1000
        return datetime.fromtimestamp(seconds, tz=timezone.utc)
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def iter_jsonl(path: Path, stats: ParseStats) -> Iterable[dict]:
    stats.files += 1
    try:
        handle = path.open(encoding="utf-8", errors="replace")
    except OSError:
        return
    with handle:
        for line in handle:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                stats.malformed_lines += 1
                continue
            if isinstance(record, dict):
                stats.records += 1
                yield record


def on_or_after(timestamp: datetime | None, since: datetime | None) -> bool:
    if since is None or timestamp is None:
        return True
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    return timestamp >= since


def add_prompt(
    patterns: PatternStats,
    provider: str,
    session_id: object,
    text: object,
    timestamp: object,
    since: datetime | None,
) -> None:
    if not isinstance(text, str) or not text.strip():
        return
    parsed_time = parse_timestamp(timestamp)
    if not on_or_after(parsed_time, since):
        return
    session = f"{provider}:{session_id or 'unknown'}"
    date = parsed_time.date().isoformat() if parsed_time else "unknown"
    patterns.total_prompts += 1
    patterns.distinct_sessions.add(session)
    if parsed_time is not None:
        patterns.window_start = min(patterns.window_start or parsed_time, parsed_time)
        patterns.window_end = max(patterns.window_end or parsed_time, parsed_time)
    for name, (pattern, _) in CATEGORY_DEFINITIONS.items():
        if re.search(pattern, text, re.IGNORECASE):
            patterns.prompts[name] += 1
            patterns.sessions[name].add(session)
            patterns.dates[name].add(date)


def scan_histories(args: argparse.Namespace, since: datetime | None) -> tuple[PatternStats, ParseStats]:
    patterns = PatternStats()
    stats = ParseStats()
    if args.codex_history.is_file():
        for record in iter_jsonl(args.codex_history, stats):
            add_prompt(
                patterns,
                "codex",
                record.get("session_id"),
                record.get("text"),
                record.get("ts"),
                since,
            )
    if args.claude_history.is_file():
        for record in iter_jsonl(args.claude_history, stats):
            add_prompt(
                patterns,
                "claude",
                record.get("sessionId"),
                record.get("display"),
                record.get("timestamp"),
                since,
            )
    return patterns, stats


def flatten_strings(value: object) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from flatten_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from flatten_strings(item)


def add_tool_call(tool_stats: ToolStats, session: str, name: str, value: object) -> None:
    provider = mcp_provider(name)
    safe_name = f"mcp__{provider}__tool" if provider is not None else "other-tool"
    tool_stats.surfaces[safe_name] += 1
    tool_stats.surface_sessions[safe_name].add(session)
    searchable = "\n".join(flatten_strings(value)).lower()
    for cli in CLI_NAMES:
        token = r"python(?:3(?:\.\d+)?)?" if cli == "python" else re.escape(cli)
        if re.search(rf"(?<![a-z0-9_-]){token}(?![a-z0-9_-])", searchable, re.IGNORECASE):
            tool_stats.calls[cli] += 1
            tool_stats.sessions[cli].add(session)


def scan_codex_tools(
    root: Path,
    since: datetime | None,
    cache_entries: dict[str, dict[str, object]] | None = None,
    next_cache: dict[str, dict[str, object]] | None = None,
) -> tuple[ToolStats, ParseStats, int]:
    tools = ToolStats()
    stats = ParseStats()
    primary_sessions = 0
    if not root.is_dir():
        return tools, stats, primary_sessions
    for path in sorted(root.glob("**/*.jsonl")):
        cached = cached_file_evidence("codex", path, cache_entries)
        if cached is not None:
            key, evidence = cached
            if apply_file_evidence(tools, stats, evidence):
                primary_sessions += 1
            if next_cache is not None:
                next_cache[key] = evidence
            continue
        try:
            before = path.stat()
        except OSError:
            continue
        records_before = stats.records
        malformed_before = stats.malformed_lines
        session_id = path.stem
        session_time = None
        is_subagent = False
        calls: list[tuple[str, object]] = []
        for record in iter_jsonl(path, stats):
            if record.get("type") == "session_meta":
                payload = record.get("payload")
                if isinstance(payload, dict):
                    session_id = str(payload.get("session_id") or payload.get("id") or session_id)
                    session_time = parse_timestamp(
                        payload.get("timestamp") or record.get("timestamp")
                    )
                    source = payload.get("source")
                    is_subagent = isinstance(source, dict) and "subagent" in source
                continue
            if record.get("type") != "response_item":
                continue
            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue
            payload_type = payload.get("type")
            if payload_type not in {"function_call", "custom_tool_call"}:
                continue
            name = str(payload.get("name") or payload_type)
            value = payload.get("arguments", payload.get("input", {}))
            calls.append((name, value))
        primary = not is_subagent and on_or_after(session_time, since) and bool(calls)
        session = opaque_id("codex", session_id)
        file_tools = ToolStats()
        if primary:
            primary_sessions += 1
            for name, value in calls:
                add_tool_call(file_tools, session, name, value)
            merge_tool_stats_into(tools, file_tools)
        if next_cache is not None:
            evidence = file_evidence(
                path,
                before,
                primary,
                session,
                file_tools,
                stats.records - records_before,
                stats.malformed_lines - malformed_before,
            )
            if evidence is not None:
                next_cache[cache_key("codex", path)] = evidence
    return tools, stats, primary_sessions


def scan_claude_tools(
    root: Path,
    since: datetime | None,
    cache_entries: dict[str, dict[str, object]] | None = None,
    next_cache: dict[str, dict[str, object]] | None = None,
) -> tuple[ToolStats, ParseStats, int]:
    tools = ToolStats()
    stats = ParseStats()
    primary_sessions = 0
    if not root.is_dir():
        return tools, stats, primary_sessions
    for path in sorted(root.glob("**/*.jsonl")):
        if "subagents" in path.parts:
            continue
        cached = cached_file_evidence("claude", path, cache_entries)
        if cached is not None:
            key, evidence = cached
            if apply_file_evidence(tools, stats, evidence):
                primary_sessions += 1
            if next_cache is not None:
                next_cache[key] = evidence
            continue
        try:
            before = path.stat()
        except OSError:
            continue
        records_before = stats.records
        malformed_before = stats.malformed_lines
        session = opaque_id("claude", path.stem)
        included = False
        calls: list[tuple[str, object]] = []
        for record in iter_jsonl(path, stats):
            timestamp = parse_timestamp(record.get("timestamp"))
            if not on_or_after(timestamp, since):
                continue
            if record.get("type") != "assistant":
                continue
            message = record.get("message")
            if not isinstance(message, dict):
                continue
            content = message.get("content")
            if not isinstance(content, list):
                continue
            for item in content:
                if isinstance(item, dict) and item.get("type") == "tool_use":
                    included = True
                    calls.append((str(item.get("name") or "tool_use"), item.get("input", {})))
        file_tools = ToolStats()
        if included:
            primary_sessions += 1
            for name, value in calls:
                add_tool_call(file_tools, session, name, value)
            merge_tool_stats_into(tools, file_tools)
        if next_cache is not None:
            evidence = file_evidence(
                path,
                before,
                included,
                session,
                file_tools,
                stats.records - records_before,
                stats.malformed_lines - malformed_before,
            )
            if evidence is not None:
                next_cache[cache_key("claude", path)] = evidence
    return tools, stats, primary_sessions


def merge_tool_stats(*items: ToolStats) -> ToolStats:
    merged = ToolStats()
    for item in items:
        merged.calls.update(item.calls)
        merged.surfaces.update(item.surfaces)
        for name, sessions in item.sessions.items():
            merged.sessions[name].update(sessions)
        for name, sessions in item.surface_sessions.items():
            merged.surface_sessions[name].update(sessions)
    return merged


def installed_skills(roots: list[Path]) -> set[str]:
    names: set[str] = set()
    frontmatter_name = re.compile(r"^name:\s*[\"']?([^\"'\s]+)", re.MULTILINE)
    for root in roots:
        if not root.is_dir():
            continue
        paths = set(root.glob("**/SKILL.md"))
        paths.update(root.glob("*/SKILL.md"))
        for path in paths:
            try:
                head = path.read_text(encoding="utf-8", errors="replace")[:4096]
            except OSError:
                continue
            match = frontmatter_name.search(head)
            if match:
                names.add(match.group(1))
    return names


def documented_tools(path: Path | None) -> set[str]:
    if path is None or not path.is_file():
        return set()
    text = path.read_text(encoding="utf-8", errors="replace")
    return {name for name in CLI_NAMES if re.search(rf"`{re.escape(name)}`", text)}


def mcp_provider(name: str) -> str | None:
    if name.startswith("mcp__"):
        parts = name.split("__", 2)
        provider = parts[1] if len(parts) >= 2 else ""
        return provider if provider in PUBLIC_MCP_PROVIDERS else "custom"
    if "mcp" in name.lower():
        return "custom"
    return None


def scan_handoffs(roots: list[Path]) -> dict[str, object]:
    concepts: Counter[str] = Counter()
    documents = 0
    malformed = 0
    seen: set[Path] = set()
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.glob("**/*.md"):
            if path in seen or not HANDOFF_FILE_RE.search(path.stem):
                continue
            if any(part in {".git", "node_modules", "vendor", "dist"} for part in path.parts):
                continue
            seen.add(path)
            try:
                headings = [
                    line.lstrip("#").strip()
                    for line in path.read_text(encoding="utf-8", errors="replace").splitlines()
                    if re.match(r"^#{1,6}\s+", line)
                ]
            except OSError:
                malformed += 1
                continue
            documents += 1
            heading_text = "\n".join(headings)
            for name, pattern in HANDOFF_CONCEPTS.items():
                if pattern.search(heading_text):
                    concepts[name] += 1
    return {"documents": documents, "unreadable": malformed, "concepts": dict(concepts)}


def build_report(args: argparse.Namespace) -> dict[str, object]:
    since = parse_since(args.since)
    patterns, history_stats = scan_histories(args, since)
    use_cache = since is None and not getattr(args, "no_cache", True)
    cache_path = getattr(
        args,
        "cache",
        Path.home()
        / ".cache"
        / "session-workflow-retrospective"
        / "tool-evidence-v1.json",
    )
    cache_entries = load_tool_cache(cache_path) if use_cache else None
    next_cache: dict[str, dict[str, object]] | None = (
        dict(cache_entries or {}) if use_cache else None
    )
    codex_tools, codex_stats, codex_sessions = scan_codex_tools(
        args.codex_sessions,
        since,
        cache_entries,
        next_cache,
    )
    if use_cache and next_cache is not None:
        save_tool_cache(cache_path, next_cache)
    claude_tools, claude_stats, claude_sessions = scan_claude_tools(
        args.claude_projects,
        since,
        cache_entries,
        next_cache,
    )
    if use_cache and next_cache is not None:
        save_tool_cache(cache_path, next_cache)
    tools = merge_tool_stats(codex_tools, claude_tools)
    roots = args.skill_root or [Path.home() / ".agents" / "skills", Path.home() / ".codex" / "skills"]
    skills = installed_skills(roots)
    documented = documented_tools(args.tool_inventory)
    handoffs = scan_handoffs(args.handoff_root)

    categories: list[dict[str, object]] = []
    for name, (_, owners) in CATEGORY_DEFINITIONS.items():
        coverage = sorted(set(owners) & skills)
        support = sorted(set(CATEGORY_SUPPORT.get(name, ())) & skills)
        sessions = len(patterns.sessions[name])
        dates = len(patterns.dates[name] - {"unknown"})
        if coverage:
            decision = "reuse-or-improve"
        elif sessions >= args.candidate_threshold and dates >= 2:
            decision = "review-skill-gap"
        else:
            decision = "insufficient-evidence"
        categories.append(
            {
                "name": name,
                "prompts": patterns.prompts[name],
                "sessions": sessions,
                "dates": dates,
                "coverage": coverage,
                "support": support,
                "decision": decision,
            }
        )
    categories.sort(key=lambda item: (-int(item["sessions"]), str(item["name"])))

    cli_rows = []
    for name, calls in tools.calls.most_common():
        sessions = len(tools.sessions[name])
        cli_rows.append(
            {
                "name": name,
                "calls": calls,
                "sessions": sessions,
                "available": shutil.which(name) is not None or (name == "python" and shutil.which("python3") is not None),
                "documented": name in documented if args.tool_inventory else None,
            }
        )

    mcp_calls: Counter[str] = Counter()
    mcp_sessions: dict[str, set[str]] = defaultdict(set)
    for name, calls in tools.surfaces.most_common():
        provider = mcp_provider(name)
        if provider is None:
            continue
        mcp_calls[provider] += calls
        mcp_sessions[provider].update(tools.surface_sessions[name])
    mcp_rows = [
        {"name": name, "calls": calls, "sessions": len(mcp_sessions[name])}
        for name, calls in mcp_calls.most_common()
    ]

    return {
        "privacy": "aggregate-only; no prompt, command, output, path, or session identifier emitted",
        "summary": {
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "history_prompts": patterns.total_prompts,
            "history_sessions": len(patterns.distinct_sessions),
            "history_files": history_stats.files,
            "window_start": patterns.window_start.isoformat() if patterns.window_start else None,
            "window_end": patterns.window_end.isoformat() if patterns.window_end else None,
            "codex_session_files": codex_stats.files,
            "codex_primary_tool_sessions": codex_sessions,
            "claude_session_files": claude_stats.files,
            "claude_primary_tool_sessions": claude_sessions,
            "session_cache_hits": codex_stats.cached_files + claude_stats.cached_files,
            "handoff_documents": handoffs["documents"],
            "installed_skills": len(skills),
            "malformed_jsonl_lines": history_stats.malformed_lines
            + codex_stats.malformed_lines
            + claude_stats.malformed_lines,
            "since": args.since,
        },
        "categories": categories,
        "cli_tools": cli_rows,
        "mcp_providers": mcp_rows,
        "handoffs": handoffs,
    }


def yes_no(value: object) -> str:
    if value is None:
        return "not-checked"
    return "yes" if value else "no"


def render_markdown(report: dict[str, object]) -> str:
    summary = report["summary"]
    assert isinstance(summary, dict)
    lines = [
        "# Session Workflow Retrospective",
        "",
        f"Privacy: {report['privacy']}.",
        "",
        "## Evidence",
        "",
        f"- Generated at: {summary['generated_at']}",
        f"- User-history window: {summary['window_start']} to {summary['window_end']}",
        f"- User-history prompts: {summary['history_prompts']}",
        f"- Distinct history sessions: {summary['history_sessions']}",
        f"- History files scanned: {summary['history_files']}",
        (
            f"- Codex session files scanned: {summary['codex_session_files']}; "
            f"primary sessions with tool calls: {summary['codex_primary_tool_sessions']}"
        ),
        (
            f"- Claude primary session files scanned: {summary['claude_session_files']}; "
            f"sessions with tool calls: {summary['claude_primary_tool_sessions']}"
        ),
        f"- Unchanged session files served from local aggregate cache: {summary['session_cache_hits']}",
        f"- Handoff/summary documents: {summary['handoff_documents']}",
        f"- Installed Skills discovered: {summary['installed_skills']}",
        f"- Malformed JSONL lines skipped: {summary['malformed_jsonl_lines']}",
        "",
        "## Workflow Patterns",
        "",
        "| Category | Prompts | Sessions | Dates | Workflow coverage | Supporting skills | Decision |",
        "| --- | ---: | ---: | ---: | --- | --- | --- |",
    ]
    categories = report["categories"]
    assert isinstance(categories, list)
    for row in categories:
        coverage = ", ".join(f"`{name}`" for name in row["coverage"]) or "-"
        support = ", ".join(f"`{name}`" for name in row["support"]) or "-"
        lines.append(
            f"| `{row['name']}` | {row['prompts']} | {row['sessions']} | {row['dates']} | "
            f"{coverage} | {support} | `{row['decision']}` |"
        )

    lines.extend(
        [
            "",
            "## Referenced CLIs",
            "",
            "Counts are tool-call references, not proof that a command completed successfully.",
            "",
            "| CLI | Tool calls | Sessions | Available now | In supplied inventory |",
            "| --- | ---: | ---: | --- | --- |",
        ]
    )
    cli_tools = report["cli_tools"]
    assert isinstance(cli_tools, list)
    for row in cli_tools:
        lines.append(
            f"| `{row['name']}` | {row['calls']} | {row['sessions']} | "
            f"{yes_no(row['available'])} | {yes_no(row['documented'])} |"
        )

    lines.extend(
        [
            "",
            "## Observed MCP Providers",
            "",
            "Historical provider usage does not imply that an MCP is currently enabled.",
            "",
            "| Provider | Calls | Sessions |",
            "| --- | ---: | ---: |",
        ]
    )
    mcp_providers = report["mcp_providers"]
    assert isinstance(mcp_providers, list)
    if mcp_providers:
        for row in mcp_providers:
            lines.append(f"| `{row['name']}` | {row['calls']} | {row['sessions']} |")
    else:
        lines.append("| - | 0 | 0 |")

    handoffs = report["handoffs"]
    assert isinstance(handoffs, dict)
    concepts = handoffs["concepts"]
    assert isinstance(concepts, dict)
    lines.extend(
        [
            "",
            "## Handoff Schema Signals",
            "",
            "| Concept | Documents |",
            "| --- | ---: |",
        ]
    )
    for name in HANDOFF_CONCEPTS:
        lines.append(f"| `{name}` | {concepts.get(name, 0)} |")

    missing = [
        row
        for row in cli_tools
        if int(row["sessions"]) >= 3 and not bool(row["available"])
    ]
    undocumented = [
        row
        for row in cli_tools
        if int(row["sessions"]) >= 3 and row["documented"] is False
    ]
    gaps = [row for row in categories if row["decision"] == "review-skill-gap"]
    lines.extend(["", "## Promotion Signals", ""])
    lines.append(
        "- Skill gaps requiring review: "
        + (", ".join(f"`{row['name']}`" for row in gaps) if gaps else "none")
        + "."
    )
    lines.append(
        "- Frequently referenced CLIs missing now: "
        + (", ".join(f"`{row['name']}`" for row in missing) if missing else "none")
        + "."
    )
    lines.append(
        "- Frequently referenced CLIs absent from the supplied inventory: "
        + (", ".join(f"`{row['name']}`" for row in undocumented) if undocumented else "none")
        + "."
    )
    handoff_documents = int(handoffs["documents"])
    remaining_next = int(concepts.get("remaining-next", 0))
    risk_blocker = int(concepts.get("risk-blocker", 0))
    lines.append(
        "- Handoff schema coverage: "
        f"concrete next work in {remaining_next}/{handoff_documents} documents; "
        f"risk or blocker state in {risk_blocker}/{handoff_documents}."
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    report = build_report(args)
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n" if args.format == "json" else render_markdown(report)
    if args.output == "-":
        print(rendered, end="")
    else:
        output = Path(args.output).expanduser()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
