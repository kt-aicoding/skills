from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_script():
    path = ROOT / "scripts" / "manage-codex-skill-descriptions.py"
    spec = importlib.util.spec_from_file_location("manage_codex_skill_descriptions", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


manager = load_script()


class DescriptionOverrideTests(unittest.TestCase):
    def test_discovery_ignores_codex_disabled_duplicate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            root = temporary / "skills"
            enabled = root / "enabled" / "SKILL.md"
            disabled = root / "disabled" / "SKILL.md"
            for path in (enabled, disabled):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    "---\nname: duplicate\ndescription: Example.\n---\n",
                    encoding="utf-8",
                )
            config = temporary / "config.toml"
            config.write_text(
                "[[skills.config]]\n"
                f'path = "{disabled}"\n'
                "enabled = false\n",
                encoding="utf-8",
            )

            paths = manager.installed_paths([root], {"duplicate"}, config)

            self.assertEqual(paths, {"duplicate": enabled})

    def test_replaces_description_and_is_idempotent(self) -> None:
        original = (
            "---\n"
            "name: example\n"
            "description: A long original description.\n"
            "license: MIT\n"
            "---\n\n"
            "# Example\n"
        )
        updated = manager.replace_description(original, "A concise trigger description.")

        self.assertIn('description: "A concise trigger description."', updated)
        self.assertIn("license: MIT", updated)
        self.assertEqual(
            manager.replace_description(updated, "A concise trigger description."),
            updated,
        )

    def test_replaces_multiline_description(self) -> None:
        original = (
            "---\n"
            "name: example\n"
            "description: >-\n"
            "  A multiline\n"
            "  description.\n"
            "version: 1\n"
            "---\n"
        )
        updated = manager.replace_description(original, "Concise.")

        self.assertIn('description: "Concise."', updated)
        self.assertNotIn("A multiline", updated)
        self.assertIn("version: 1", updated)

    def test_removes_selected_installed_frontmatter_key(self) -> None:
        original = (
            "---\n"
            "name: example\n"
            "description: Example.\n"
            "metadata:\n"
            "  version: 1\n"
            "compatibility: Requires a CLI.\n"
            "---\n"
        )
        updated = manager.remove_frontmatter_keys(original, {"compatibility"})

        self.assertNotIn("compatibility:", updated)
        self.assertIn("metadata:\n  version: 1", updated)


if __name__ == "__main__":
    unittest.main()
