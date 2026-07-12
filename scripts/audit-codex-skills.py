#!/usr/bin/env python3
"""Audit Codex user skills without modifying the installation."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterator


ALLOWED_FRONTMATTER_KEYS = {
    "allowed-tools",
    "description",
    "license",
    "metadata",
    "name",
}
SKIP_DIRECTORIES = {".git", "__pycache__", "node_modules"}


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    path: str
    root: str
    allow_implicit_invocation: bool
    sha256: str
    frontmatter_keys: tuple[str, ...]
    unsupported_keys: tuple[str, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit discovered Codex skills for conflicts and compatibility issues."
    )
    parser.add_argument(
        "--root",
        action="append",
        type=Path,
        help="Skill root to scan. Repeat to scan multiple roots.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path.home() / ".codex" / "config.toml",
        help="Codex config used to identify disabled skills.",
    )
    parser.add_argument(
        "--include-disabled",
        action="store_true",
        help="Include skills disabled through [[skills.config]].",
    )
    parser.add_argument(
        "--max-description",
        type=int,
        default=140,
        help="Recommended maximum description length (default: 140).",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print every finding instead of the first ten in each category.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 when conflicts, invalid metadata, or long descriptions are found.",
    )
    return parser.parse_args()


def iter_skill_files(root: Path) -> Iterator[Path]:
    """Walk a root while following skill-directory symlinks and avoiding cycles."""

    def walk(directory: Path, ancestors: frozenset[tuple[int, int]]) -> Iterator[Path]:
        try:
            stat = directory.stat()
        except OSError:
            return
        identity = (stat.st_dev, stat.st_ino)
        if identity in ancestors:
            return
        ancestors = ancestors | {identity}

        try:
            entries = sorted(directory.iterdir(), key=lambda item: item.name)
        except OSError:
            return
        for entry in entries:
            if entry.name in SKIP_DIRECTORIES:
                continue
            if entry.name == "SKILL.md" and entry.is_file():
                yield entry
            elif entry.is_dir():
                yield from walk(entry, ancestors)

    if root.is_dir():
        yield from walk(root, frozenset())


def decode_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        try:
            decoded = ast.literal_eval(value)
            return decoded if isinstance(decoded, str) else value
        except (SyntaxError, ValueError):
            pass
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, str], tuple[str, ...]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter delimiter")
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("missing closing frontmatter delimiter") from exc

    body = lines[1:end]
    values: dict[str, str] = {}
    keys: list[str] = []
    index = 0
    while index < len(body):
        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", body[index])
        if not match:
            index += 1
            continue
        key, raw_value = match.group(1), match.group(2) or ""
        keys.append(key)
        if raw_value in {"", "|", "|-", ">", ">-"}:
            block: list[str] = []
            index += 1
            while index < len(body) and (not body[index] or body[index][0].isspace()):
                block.append(body[index].strip())
                index += 1
            values[key] = " ".join(part for part in block if part)
            continue
        values[key] = decode_scalar(raw_value)
        index += 1
    return values, tuple(keys)


def disabled_skill_paths(config: Path) -> set[Path]:
    if not config.is_file():
        return set()
    text = config.read_text(encoding="utf-8", errors="replace")
    disabled: set[Path] = set()
    for section in text.split("[[skills.config]]")[1:]:
        section = section.split("[[", 1)[0]
        path_match = re.search(r'^path\s*=\s*(.+)$', section, re.MULTILINE)
        enabled_match = re.search(r'^enabled\s*=\s*(true|false)\s*$', section, re.MULTILINE)
        if not path_match or not enabled_match or enabled_match.group(1) != "false":
            continue
        try:
            raw_path = ast.literal_eval(path_match.group(1).strip())
        except (SyntaxError, ValueError):
            continue
        if isinstance(raw_path, str):
            disabled.add(Path(os.path.expandvars(os.path.expanduser(raw_path))).absolute())
    return disabled


def allows_implicit_invocation(skill_file: Path) -> bool:
    """Read the Codex-native invocation policy beside a skill, defaulting to true."""

    metadata = skill_file.parent / "agents" / "openai.yaml"
    if not metadata.is_file():
        return True
    try:
        lines = metadata.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return True
    for index, line in enumerate(lines):
        if not re.match(r"^policy:\s*(?:#.*)?$", line):
            continue
        for child in lines[index + 1 :]:
            if child and not child[0].isspace():
                break
            match = re.match(
                r"^\s+allow_implicit_invocation:\s*(true|false)\s*(?:#.*)?$",
                child,
            )
            if match:
                return match.group(1) == "true"
    return True


def find_broken_symlinks(roots: list[Path]) -> list[str]:
    broken: list[str] = []
    for root in roots:
        if not root.is_dir():
            continue
        try:
            entries = root.iterdir()
        except OSError:
            continue
        for entry in entries:
            if entry.is_symlink() and not entry.exists():
                broken.append(str(entry.absolute()))
    return sorted(broken)


def audit(roots: list[Path], config: Path, include_disabled: bool, max_description: int) -> dict:
    disabled = disabled_skill_paths(config)
    skills: list[Skill] = []
    invalid: list[dict[str, str]] = []

    for root in roots:
        root = root.expanduser().absolute()
        for path in iter_skill_files(root):
            absolute = path.absolute()
            if not include_disabled and absolute in disabled:
                continue
            try:
                text = path.read_text(encoding="utf-8")
                values, keys = parse_frontmatter(text)
                name = values.get("name", "").strip()
                description = values.get("description", "").strip()
                if not name or not description:
                    raise ValueError("frontmatter must contain name and description")
            except (OSError, UnicodeError, ValueError) as exc:
                invalid.append({"path": str(absolute), "error": str(exc)})
                continue
            skills.append(
                Skill(
                    name=name,
                    description=description,
                    path=str(absolute),
                    root=str(root),
                    allow_implicit_invocation=allows_implicit_invocation(path),
                    sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    frontmatter_keys=keys,
                    unsupported_keys=tuple(sorted(set(keys) - ALLOWED_FRONTMATTER_KEYS)),
                )
            )

    names: dict[str, list[str]] = defaultdict(list)
    hashes: dict[str, list[str]] = defaultdict(list)
    unsupported: list[dict[str, object]] = []
    long_descriptions: list[dict[str, object]] = []
    for skill in skills:
        names[skill.name].append(skill.path)
        hashes[skill.sha256].append(skill.path)
        if skill.unsupported_keys:
            unsupported.append(
                {"name": skill.name, "path": skill.path, "keys": list(skill.unsupported_keys)}
            )
        if len(skill.description) > max_description:
            long_descriptions.append(
                {"name": skill.name, "path": skill.path, "length": len(skill.description)}
            )

    duplicate_names = [
        {"name": name, "paths": paths}
        for name, paths in sorted(names.items())
        if len(paths) > 1
    ]
    exact_duplicates = [
        {"sha256": digest, "paths": paths}
        for digest, paths in sorted(hashes.items())
        if len(paths) > 1
    ]
    root_counts = Counter(skill.root for skill in skills)
    implicit_skills = [skill for skill in skills if skill.allow_implicit_invocation]
    explicit_only_skills = [skill for skill in skills if not skill.allow_implicit_invocation]
    return {
        "summary": {
            "active_skills": len(skills) + len(invalid),
            "valid_skills": len(skills),
            "implicit_skills": len(implicit_skills),
            "explicit_only_skills": len(explicit_only_skills),
            "implicit_description_chars": sum(
                len(skill.description) for skill in implicit_skills
            ),
            "disabled_skills": len(disabled),
            "invalid_skills": len(invalid),
            "duplicate_name_groups": len(duplicate_names),
            "exact_duplicate_groups": len(exact_duplicates),
            "unsupported_frontmatter_skills": len(unsupported),
            "descriptions_over_limit": len(long_descriptions),
            "max_description": max_description,
        },
        "root_counts": dict(sorted(root_counts.items())),
        "broken_symlinks": find_broken_symlinks(roots),
        "invalid_skills": invalid,
        "duplicate_names": duplicate_names,
        "exact_duplicates": exact_duplicates,
        "unsupported_frontmatter": unsupported,
        "explicit_only_skills": [
            {
                "name": skill.name,
                "path": skill.path,
                "metadata_path": str(Path(skill.path).parent / "agents" / "openai.yaml"),
            }
            for skill in sorted(explicit_only_skills, key=lambda item: (item.name, item.path))
        ],
        "long_descriptions": sorted(
            long_descriptions, key=lambda item: (-int(item["length"]), str(item["name"]))
        ),
        "skills": [
            asdict(skill) for skill in sorted(skills, key=lambda item: (item.name, item.path))
        ],
    }


def print_human(report: dict, verbose: bool) -> None:
    summary = report["summary"]
    print("Codex skills audit")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    for root, count in report["root_counts"].items():
        print(f"  root: {root} ({count})")

    sections = (
        ("broken symlinks", report["broken_symlinks"]),
        ("invalid skills", report["invalid_skills"]),
        ("duplicate names", report["duplicate_names"]),
        ("exact duplicates", report["exact_duplicates"]),
        ("unsupported frontmatter", report["unsupported_frontmatter"]),
        ("explicit-only skills", report["explicit_only_skills"]),
        ("long descriptions", report["long_descriptions"]),
    )
    for label, entries in sections:
        if not entries:
            continue
        print(f"\n{label} ({len(entries)}):")
        visible_entries = entries if verbose else entries[:10]
        for entry in visible_entries:
            if isinstance(entry, str):
                print(f"  - {entry}")
            else:
                print(f"  - {json.dumps(entry, ensure_ascii=False, sort_keys=True)}")
        if len(entries) > len(visible_entries):
            print(f"  ... {len(entries) - len(visible_entries)} more; rerun with --verbose")


def has_strict_failures(report: dict) -> bool:
    summary = report["summary"]
    return bool(
        report["broken_symlinks"]
        or summary["invalid_skills"]
        or summary["duplicate_name_groups"]
        or summary["exact_duplicate_groups"]
        or summary["unsupported_frontmatter_skills"]
        or summary["descriptions_over_limit"]
    )


def main() -> int:
    args = parse_args()
    roots = args.root or [Path.home() / ".agents" / "skills", Path.home() / ".codex" / "skills"]
    report = audit(roots, args.config, args.include_disabled, args.max_description)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print_human(report, args.verbose)
    return 1 if args.strict and has_strict_failures(report) else 0


if __name__ == "__main__":
    raise SystemExit(main())
