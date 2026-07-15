#!/usr/bin/env python3
"""Apply concise, versioned descriptions to selected installed Codex skills."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from types import ModuleType


DESCRIPTION_RE = re.compile(r"^description:\s*(.*)$")


def parse_args() -> argparse.Namespace:
    repository = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Check or apply concise Codex skill description overrides."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Update installed skills and configured source files.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=repository / "config" / "codex-skill-description-overrides.json",
    )
    parser.add_argument(
        "--root",
        action="append",
        type=Path,
        help="Codex skill root. Repeat for multiple roots.",
    )
    parser.add_argument(
        "--codex-config",
        type=Path,
        default=Path.home() / ".codex" / "config.toml",
        help="Codex config used to exclude disabled compatibility copies.",
    )
    parser.add_argument(
        "--max-description",
        type=int,
        default=140,
    )
    return parser.parse_args()


def load_audit_module() -> ModuleType:
    path = Path(__file__).resolve().with_name("audit-codex-skills.py")
    spec = importlib.util.spec_from_file_location("codex_skill_audit_for_descriptions", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load audit module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def replace_description(text: str, description: str) -> str:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter delimiter")
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("missing closing frontmatter delimiter") from exc

    matches = [index for index in range(1, end) if DESCRIPTION_RE.match(lines[index])]
    if len(matches) != 1:
        raise ValueError(f"expected one description field, found {len(matches)}")
    index = matches[0]
    raw_value = DESCRIPTION_RE.match(lines[index]).group(1).strip()
    if raw_value in {"", "|", "|-", ">", ">-"}:
        block_end = index + 1
        while block_end < end and (
            not lines[block_end] or lines[block_end][0].isspace()
        ):
            block_end += 1
        lines[index:block_end] = [
            "description: " + json.dumps(description, ensure_ascii=False)
        ]
    else:
        lines[index] = "description: " + json.dumps(description, ensure_ascii=False)
    return "\n".join(lines).rstrip() + "\n"


def remove_frontmatter_keys(text: str, keys: set[str]) -> str:
    if not keys:
        return text
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter delimiter")
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("missing closing frontmatter delimiter") from exc

    index = 1
    while index < end:
        match = re.match(r"^([A-Za-z0-9_-]+):", lines[index])
        if not match or match.group(1) not in keys:
            index += 1
            continue
        block_end = index + 1
        while block_end < end and (
            not lines[block_end] or lines[block_end][0].isspace()
        ):
            block_end += 1
        del lines[index:block_end]
        end -= block_end - index
    return "\n".join(lines).rstrip() + "\n"


def read_config(path: Path, max_description: int) -> dict[str, dict[str, object]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("description override config must be an object")
    for name, item in data.items():
        if not isinstance(item, dict) or not isinstance(item.get("description"), str):
            raise ValueError(f"{name}: description must be a string")
        description = item["description"].strip()
        if not description:
            raise ValueError(f"{name}: description must not be empty")
        if len(description) > max_description:
            raise ValueError(
                f"{name}: description has {len(description)} characters; max is {max_description}"
            )
        source_paths = item.get("source_paths", [])
        if not isinstance(source_paths, list) or not all(
            isinstance(source, str) for source in source_paths
        ):
            raise ValueError(f"{name}: source_paths must be a list of strings")
        remove_installed_keys = item.get("remove_installed_keys", [])
        if not isinstance(remove_installed_keys, list) or not all(
            isinstance(key, str) and key for key in remove_installed_keys
        ):
            raise ValueError(f"{name}: remove_installed_keys must be a list of strings")
    return data


def installed_paths(
    roots: list[Path], names: set[str], codex_config: Path | None = None
) -> dict[str, Path]:
    audit_module = load_audit_module()
    disabled = (
        audit_module.disabled_skill_paths(codex_config)
        if codex_config is not None
        else set()
    )
    paths: dict[str, Path] = {}
    duplicates: set[str] = set()
    for root in roots:
        for skill_file in audit_module.iter_skill_files(root.expanduser().absolute()):
            if skill_file.absolute() in disabled:
                continue
            try:
                text = skill_file.read_text(encoding="utf-8")
                values, _ = audit_module.parse_frontmatter(text)
            except (OSError, UnicodeError, ValueError):
                continue
            name = values.get("name", "").strip()
            if name not in names:
                continue
            if name in paths and paths[name] != skill_file:
                duplicates.add(name)
            paths[name] = skill_file
    if duplicates:
        raise RuntimeError("duplicate selected skills: " + ", ".join(sorted(duplicates)))
    return paths


def main() -> int:
    args = parse_args()
    repository = Path(__file__).resolve().parent.parent
    config = read_config(args.config, args.max_description)
    roots = args.root or [Path.home() / ".agents" / "skills", Path.home() / ".codex" / "skills"]
    installed = installed_paths(roots, set(config), args.codex_config)
    missing = sorted(set(config) - set(installed))
    if missing:
        print("Missing installed skills: " + ", ".join(missing))
        return 1

    changed = 0
    mismatches: list[str] = []
    checked_files = 0
    for name, item in sorted(config.items()):
        description = str(item["description"])
        targets = [
            (installed[name], set(item.get("remove_installed_keys", [])))
        ]
        targets.extend(
            (repository / source, set()) for source in item.get("source_paths", [])
        )
        for path, remove_keys in targets:
            checked_files += 1
            if not path.is_file():
                raise FileNotFoundError(f"{name}: configured source does not exist: {path}")
            text = path.read_text(encoding="utf-8")
            try:
                updated = replace_description(text, description)
                updated = remove_frontmatter_keys(updated, remove_keys)
            except ValueError as exc:
                raise ValueError(f"{name}: {path}: {exc}") from exc
            if updated == text:
                continue
            if not args.apply:
                mismatches.append(f"{name}: {path}")
                continue
            path.write_text(updated, encoding="utf-8")
            changed += 1

    if not args.apply:
        print(f"Configured skills: {len(config)}")
        print(f"Checked files: {checked_files}")
        print(f"Needs update: {len(mismatches)}")
        for mismatch in mismatches:
            print(f"  - {mismatch}")
        return 1 if mismatches else 0

    print(f"Updated files: {changed}")
    print(f"Unchanged files: {checked_files - changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
