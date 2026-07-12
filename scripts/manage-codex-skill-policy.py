#!/usr/bin/env python3
"""Manage Codex explicit-only skill policy from a versioned manifest."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


SKIP_DIRECTORIES = {".git", "__pycache__", "node_modules"}
POLICY_KEY = "allow_implicit_invocation"


@dataclass(frozen=True)
class SkillLocation:
    name: str
    directory: Path

    @property
    def metadata_path(self) -> Path:
        return self.directory / "agents" / "openai.yaml"


def parse_args() -> argparse.Namespace:
    repository = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Keep selected Codex skills explicit-only without disabling them."
    )
    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        "--apply",
        action="store_true",
        help="Set policy.allow_implicit_invocation=false for manifest entries.",
    )
    action.add_argument(
        "--restore",
        action="store_true",
        help="Remove the managed explicit-only policy from manifest entries.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=repository / "config" / "codex-explicit-only-skills.txt",
        help="Newline-delimited skill names. Blank lines and comments are ignored.",
    )
    parser.add_argument(
        "--root",
        action="append",
        type=Path,
        help="Skill root to scan. Repeat for multiple roots.",
    )
    return parser.parse_args()


def iter_skill_files(root: Path) -> Iterator[Path]:
    """Walk a skill root, following directory symlinks without cycling."""

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


def skill_name(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None
    match = re.search(r"(?m)^name:\s*['\"]?([^'\"\n]+)['\"]?\s*$", text)
    return match.group(1).strip() if match else None


def discover(roots: list[Path], selected: set[str]) -> dict[str, SkillLocation]:
    locations: dict[str, SkillLocation] = {}
    duplicates: set[str] = set()
    for root in roots:
        for path in iter_skill_files(root.expanduser().absolute()):
            name = skill_name(path)
            if not name or name not in selected:
                continue
            if name in locations and locations[name].directory != path.parent:
                duplicates.add(name)
                continue
            locations[name] = SkillLocation(name=name, directory=path.parent)
    if duplicates:
        names = ", ".join(sorted(duplicates))
        raise RuntimeError(f"duplicate skill names across roots: {names}")
    return locations


def read_manifest(path: Path) -> list[str]:
    names: list[str] = []
    seen: set[str] = set()
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        name = raw_line.split("#", 1)[0].strip()
        if not name:
            continue
        if name in seen:
            raise RuntimeError(f"duplicate manifest entry: {name}")
        seen.add(name)
        names.append(name)
    return names


def policy_value(text: str) -> bool | None:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not re.match(r"^policy:\s*(?:#.*)?$", line):
            continue
        for child in lines[index + 1 :]:
            if child and not child[0].isspace():
                break
            match = re.match(rf"^\s+{POLICY_KEY}:\s*(true|false)\s*(?:#.*)?$", child)
            if match:
                return match.group(1) == "true"
    return None


def set_explicit_only(text: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not re.match(r"^policy:\s*(?:#.*)?$", line):
            continue
        end = index + 1
        while end < len(lines) and (not lines[end] or lines[end][0].isspace()):
            match = re.match(rf"^(\s+){POLICY_KEY}:\s*(?:true|false)\s*(?:#.*)?$", lines[end])
            if match:
                lines[end] = f"{match.group(1)}{POLICY_KEY}: false"
                return "\n".join(lines).rstrip() + "\n"
            end += 1
        lines.insert(index + 1, f"  {POLICY_KEY}: false")
        return "\n".join(lines).rstrip() + "\n"

    if lines and lines[-1]:
        lines.append("")
    lines.extend(["policy:", f"  {POLICY_KEY}: false"])
    return "\n".join(lines).rstrip() + "\n"


def restore_implicit(text: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not re.match(r"^policy:\s*(?:#.*)?$", line):
            continue
        end = index + 1
        removed = False
        while end < len(lines) and (not lines[end] or lines[end][0].isspace()):
            if re.match(rf"^\s+{POLICY_KEY}:\s*false\s*(?:#.*)?$", lines[end]):
                del lines[end]
                removed = True
                break
            end += 1
        if not removed:
            return text
        next_index = index + 1
        while next_index < len(lines) and not lines[next_index]:
            next_index += 1
        if next_index >= len(lines) or not lines[next_index][0].isspace():
            del lines[index]
        return "\n".join(lines).rstrip() + "\n"
    return text


def main() -> int:
    args = parse_args()
    roots = args.root or [Path.home() / ".agents" / "skills", Path.home() / ".codex" / "skills"]
    names = read_manifest(args.manifest)
    locations = discover(roots, set(names))
    missing = [name for name in names if name not in locations]
    if missing:
        print("Missing skills:")
        for name in missing:
            print(f"  - {name}")
        return 1

    changed = 0
    noncompliant: list[str] = []
    for name in names:
        path = locations[name].metadata_path
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        if args.apply:
            updated = set_explicit_only(text)
        elif args.restore:
            updated = restore_implicit(text)
        else:
            updated = text
            if policy_value(text) is not False:
                noncompliant.append(name)
                continue
        if updated == text:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(updated, encoding="utf-8")
        changed += 1

    if not args.apply and not args.restore:
        print(f"Manifest skills: {len(names)}")
        print(f"Explicit-only: {len(names) - len(noncompliant)}")
        print(f"Needs update: {len(noncompliant)}")
        for name in noncompliant:
            print(f"  - {name}")
        return 1 if noncompliant else 0

    action = "Applied" if args.apply else "Restored"
    print(f"{action}: {changed}")
    print(f"Unchanged: {len(names) - changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
