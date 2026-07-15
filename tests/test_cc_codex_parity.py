from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]


def load_script():
    path = ROOT / "scripts" / "audit-cc-codex-skills.py"
    spec = importlib.util.spec_from_file_location("audit_cc_codex_skills", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


parity_audit = load_script()


class CrossPlatformParityTests(unittest.TestCase):
    def test_parity_report_is_tolerant_and_privacy_preserving(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            claude = temporary / ".claude"
            codex = temporary / "codex-skills"
            for root in (claude / "skills" / "alpha", codex / "alpha"):
                root.mkdir(parents=True)
                (root / "SKILL.md").write_text(
                    "---\nname: alpha\ndescription: Shared skill.\n---\n\nDo the work.\n",
                    encoding="utf-8",
                )

            beta = claude / "skills" / "beta"
            beta.mkdir(parents=True)
            (beta / "SKILL.md").write_text(
                "---\ndescription: Claude-only skill.\n---\n\nPRIVATE_SKILL_BODY\n",
                encoding="utf-8",
            )
            (claude / "skills" / "broken").symlink_to(temporary / "missing")

            (claude / "commands").mkdir()
            (claude / "commands" / "deploy.md").write_text("command", encoding="utf-8")
            (claude / "agents").mkdir()
            (claude / "agents" / "reviewer.md").write_text("agent", encoding="utf-8")
            (claude / "plugins").mkdir()
            (claude / "plugins" / "installed_plugins.json").write_text(
                json.dumps({"plugins": {"example@market": [{}]}}),
                encoding="utf-8",
            )
            (claude / "settings.json").write_text(
                json.dumps({"enabledPlugins": {}}),
                encoding="utf-8",
            )
            (claude / "history.jsonl").write_text(
                json.dumps(
                    {
                        "display": "/beta PRIVATE_PROMPT",
                        "sessionId": "PRIVATE_SESSION",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            mapping = temporary / "mapping.json"
            mapping.write_text(
                json.dumps(
                    {
                        "beta": {
                            "decision": "covered",
                            "targets": ["alpha"],
                            "notes": "Covered in the test fixture.",
                        }
                    }
                ),
                encoding="utf-8",
            )
            args = SimpleNamespace(
                claude_root=claude,
                codex_root=[codex],
                codex_config=temporary / "missing-config.toml",
                mapping=mapping,
            )

            report = parity_audit.build_report(args)
            rendered = parity_audit.render_markdown(report)

        self.assertEqual(report["summary"]["shared_names"], 1)
        self.assertEqual(report["summary"]["claude_only"], 1)
        self.assertEqual(report["summary"]["parity"], {"exact": 1})
        self.assertEqual(report["claude_metadata"]["missing_declared_name"], ["beta"])
        self.assertEqual(report["claude_metadata"]["broken_symlinks"], ["broken"])
        self.assertEqual(report["claude_explicit_usage"]["beta"]["sessions"], 1)
        self.assertNotIn("PRIVATE_PROMPT", rendered)
        self.assertNotIn("PRIVATE_SESSION", rendered)
        self.assertNotIn("PRIVATE_SKILL_BODY", rendered)


if __name__ == "__main__":
    unittest.main()
