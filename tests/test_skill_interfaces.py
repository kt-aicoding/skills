from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_script():
    path = ROOT / "scripts" / "manage-codex-skill-interfaces.py"
    spec = importlib.util.spec_from_file_location("manage_codex_skill_interfaces", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


manager = load_script()


class SkillInterfaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.values = {
            "display_name": "Example Skill",
            "short_description": "Perform a focused example workflow",
            "default_prompt": "Use $example to complete this focused workflow.",
        }

    def test_add_interface_and_preserve_policy(self) -> None:
        original = "policy:\n  allow_implicit_invocation: false\n"
        updated = manager.set_interface(original, self.values)

        self.assertIn('display_name: "Example Skill"', updated)
        self.assertIn('default_prompt: "Use $example', updated)
        self.assertIn("allow_implicit_invocation: false", updated)
        self.assertEqual(manager.set_interface(updated, self.values), updated)

    def test_update_interface_and_preserve_optional_fields(self) -> None:
        original = (
            "interface:\n"
            '  display_name: "Old"\n'
            '  icon_small: "./assets/icon.svg"\n'
        )
        updated = manager.set_interface(original, self.values)

        self.assertIn('display_name: "Example Skill"', updated)
        self.assertIn('icon_small: "./assets/icon.svg"', updated)
        self.assertIn("short_description:", updated)
        self.assertIn("default_prompt:", updated)

    def test_config_requires_skill_name_in_default_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "config.json"
            values = dict(self.values)
            values["default_prompt"] = "Complete this workflow."
            path.write_text(json.dumps({"example": values}), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "must mention \\$example"):
                manager.read_config(path)


if __name__ == "__main__":
    unittest.main()
