from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_script(module_name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / relative_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {relative_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


manager = load_script("manage_codex_skill_policy", "scripts/manage-codex-skill-policy.py")
auditor = load_script("audit_codex_skills", "scripts/audit-codex-skills.py")


class PolicyTextTests(unittest.TestCase):
    def test_add_update_and_restore_policy(self) -> None:
        original = "interface:\n  display_name: Example\n"
        explicit = manager.set_explicit_only(original)

        self.assertEqual(manager.policy_value(explicit), False)
        self.assertEqual(manager.set_explicit_only(explicit), explicit)
        self.assertEqual(manager.restore_implicit(explicit), original)

    def test_preserve_other_policy_keys_when_restoring(self) -> None:
        original = "policy:\n  allow_implicit_invocation: true\n  network: false\n"
        explicit = manager.set_explicit_only(original)

        self.assertIn("allow_implicit_invocation: false", explicit)
        self.assertEqual(
            manager.restore_implicit(explicit),
            "policy:\n  network: false\n",
        )


class DiscoveryTests(unittest.TestCase):
    def test_discover_skill_through_directory_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            source = temporary / "source" / "example"
            source.mkdir(parents=True)
            (source / "SKILL.md").write_text(
                "---\nname: example\ndescription: Example skill.\n---\n",
                encoding="utf-8",
            )
            root = temporary / "skills"
            root.mkdir()
            (root / "example").symlink_to(source, target_is_directory=True)

            locations = manager.discover([root], {"example"})

            self.assertEqual(locations["example"].directory, root / "example")


class AuditPolicyTests(unittest.TestCase):
    def test_read_explicit_only_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skill = Path(temporary_directory)
            (skill / "agents").mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: example\ndescription: Example skill.\n---\n",
                encoding="utf-8",
            )
            (skill / "agents" / "openai.yaml").write_text(
                "policy:\n  allow_implicit_invocation: false\n",
                encoding="utf-8",
            )

            self.assertFalse(auditor.allows_implicit_invocation(skill / "SKILL.md"))


if __name__ == "__main__":
    unittest.main()
