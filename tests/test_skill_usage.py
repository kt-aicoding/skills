from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]


def load_script(module_name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / relative_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {relative_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


usage_audit = load_script("audit_codex_skill_usage", "scripts/audit-codex-skill-usage.py")


class SkillUsagePrivacyTests(unittest.TestCase):
    def test_report_contains_counts_without_session_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            skills_root = temporary / "skills"
            for name in ("alpha", "beta"):
                skill = skills_root / name
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(
                    f"---\nname: {name}\ndescription: {name.title()} test skill.\n---\n",
                    encoding="utf-8",
                )

            sessions_root = temporary / "sessions"
            sessions_root.mkdir()
            records = [
                {
                    "type": "session_meta",
                    "payload": {
                        "session_id": "private-session-id",
                        "timestamp": "2026-07-12T00:00:00Z",
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": "Use $alpha with PRIVATE_PROMPT_CONTENT",
                            }
                        ],
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "function_call",
                        "input": {
                            "path": "/private/work/beta/SKILL.md",
                            "token": "PRIVATE_TOOL_INPUT",
                        },
                    },
                },
            ]
            (sessions_root / "rollout.jsonl").write_text(
                "\n".join(json.dumps(record) for record in records) + "\n",
                encoding="utf-8",
            )

            args = SimpleNamespace(
                root=[skills_root],
                config=temporary / "missing-config.toml",
                sessions_root=sessions_root,
                frequent_threshold=2,
            )
            report = usage_audit.build_report(args)
            rendered = usage_audit.render_markdown(report)
            rows = {row["name"]: row for row in report["skills"]}

            self.assertEqual(rows["alpha"]["explicit_sessions"], 1)
            self.assertEqual(rows["beta"]["file_read_sessions"], 1)
            self.assertEqual(rows["alpha"]["sessions"], 1)
            self.assertEqual(rows["beta"]["sessions"], 1)
            for private_value in (
                "private-session-id",
                "PRIVATE_PROMPT_CONTENT",
                "PRIVATE_TOOL_INPUT",
                "/private/work",
            ):
                self.assertNotIn(private_value, rendered)


if __name__ == "__main__":
    unittest.main()
