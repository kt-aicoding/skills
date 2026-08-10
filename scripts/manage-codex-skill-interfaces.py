#!/usr/bin/env python3
"""Check or apply versioned Codex Skill interface metadata."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from types import ModuleType


INTERFACE_FIELDS = ("display_name", "short_description", "default_prompt")


def parse_args() -> argparse.Namespace:
    repository = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Keep selected installed Skill UI metadata complete and consistent."
    )
    parser.add_argument("--apply", action="store_true", help="Write metadata updates.")
    parser.add_argument(
        "--config",
        type=Path,
        default=repository / "config" / "codex-skill-interface-overrides.json",
    )
    parser.add_argument(
        "--root",
        action="append",
        type=Path,
        help="Codex Skill root. Repeat for multiple roots.",
    )
    parser.add_argument(
        "--codex-config",
        type=Path,
        default=Path.home() / ".codex" / "config.toml",
        help="Codex config used to exclude disabled compatibility copies.",
    )
    return parser.parse_args()


def load_description_manager() -> ModuleType:
    path = Path(__file__).resolve().with_name("manage-codex-skill-descriptions.py")
    spec = importlib.util.spec_from_file_location("codex_skill_description_manager", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load description manager: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_config(path: Path) -> dict[str, dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("interface override config must be an object")
    for name, item in data.items():
        if not isinstance(item, dict):
            raise ValueError(f"{name}: interface config must be an object")
        missing = [field for field in INTERFACE_FIELDS if not isinstance(item.get(field), str)]
        if missing:
            raise ValueError(f"{name}: missing string fields: {', '.join(missing)}")
        extra = set(item) - set(INTERFACE_FIELDS)
        if extra:
            raise ValueError(f"{name}: unsupported fields: {', '.join(sorted(extra))}")
        if not item["display_name"].strip():
            raise ValueError(f"{name}: display_name must not be empty")
        short_length = len(item["short_description"].strip())
        if not 25 <= short_length <= 64:
            raise ValueError(
                f"{name}: short_description has {short_length} characters; expected 25-64"
            )
        if f"${name}" not in item["default_prompt"]:
            raise ValueError(f"{name}: default_prompt must mention ${name}")
    return data


def set_interface(text: str, values: dict[str, str]) -> str:
    lines = text.splitlines()
    start = next(
        (index for index, line in enumerate(lines) if re.match(r"^interface:\s*(?:#.*)?$", line)),
        None,
    )
    rendered = {
        field: f"  {field}: {json.dumps(values[field], ensure_ascii=False)}"
        for field in INTERFACE_FIELDS
    }
    if start is None:
        block = ["interface:", *(rendered[field] for field in INTERFACE_FIELDS)]
        if lines:
            block.extend(["", *lines])
        return "\n".join(block).rstrip() + "\n"

    end = start + 1
    while end < len(lines) and (not lines[end] or lines[end][0].isspace()):
        end += 1
    for field in INTERFACE_FIELDS:
        matches = [
            index
            for index in range(start + 1, end)
            if re.match(rf"^\s+{re.escape(field)}:", lines[index])
        ]
        if len(matches) > 1:
            raise ValueError(f"duplicate interface field: {field}")
        if matches:
            lines[matches[0]] = rendered[field]
            continue
        lines.insert(end, rendered[field])
        end += 1
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    config = read_config(args.config)
    roots = args.root or [Path.home() / ".agents" / "skills", Path.home() / ".codex" / "skills"]
    manager = load_description_manager()
    installed = manager.installed_paths(roots, set(config), args.codex_config)
    missing = sorted(set(config) - set(installed))
    if missing:
        print("Missing installed skills: " + ", ".join(missing))
        return 1

    changed = 0
    mismatches: list[str] = []
    for name, values in sorted(config.items()):
        path = installed[name].parent / "agents" / "openai.yaml"
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        updated = set_interface(text, values)
        if updated == text:
            continue
        if not args.apply:
            mismatches.append(f"{name}: {path}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(updated, encoding="utf-8")
        changed += 1

    if not args.apply:
        print(f"Configured skills: {len(config)}")
        print(f"Complete interfaces: {len(config) - len(mismatches)}")
        print(f"Needs update: {len(mismatches)}")
        for mismatch in mismatches:
            print(f"  - {mismatch}")
        return 1 if mismatches else 0

    print(f"Updated files: {changed}")
    print(f"Unchanged files: {len(config) - changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
