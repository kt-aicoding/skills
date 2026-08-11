from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT / "skills/session-workflow-retrospective/scripts/analyze_session_workflows.py"
)


def load_script():
    spec = importlib.util.spec_from_file_location(
        "session_workflow_retrospective", SCRIPT
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load retrospective analyzer")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


analyzer = load_script()


class SessionWorkflowRetrospectiveTests(unittest.TestCase):
    def test_cache_writes_merge_instead_of_pruning_existing_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "cache.json"
            analyzer.save_tool_cache(path, {"first": {"size": 1}})
            analyzer.save_tool_cache(path, {"second": {"size": 2}})

            self.assertEqual(
                set(analyzer.load_tool_cache(path)),
                {"first", "second"},
            )

    def test_installed_skills_include_top_level_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            installed = root / "installed"
            source = root / "source" / "linked-skill"
            installed.mkdir()
            source.mkdir(parents=True)
            (source / "SKILL.md").write_text(
                "---\nname: linked-skill\ndescription: Test.\n---\n",
                encoding="utf-8",
            )
            (installed / "linked-skill").symlink_to(source, target_is_directory=True)

            self.assertIn("linked-skill", analyzer.installed_skills([installed]))

    def test_cli_writes_aggregate_report_to_requested_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            codex_sessions = root / "codex-sessions"
            claude_projects = root / "claude-projects"
            skills = root / "skills"
            codex_sessions.mkdir()
            claude_projects.mkdir()
            skills.mkdir()
            codex_history = root / "codex-history.jsonl"
            codex_history.write_text(
                json.dumps(
                    {
                        "session_id": "PRIVATE_SESSION",
                        "text": "复盘重复工作流 PRIVATE_PROMPT",
                        "ts": 1_800_000_000,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            claude_history = root / "claude-history.jsonl"
            claude_history.write_text("", encoding="utf-8")
            output = root / "reports" / "retrospective.md"

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--codex-sessions",
                    str(codex_sessions),
                    "--codex-history",
                    str(codex_history),
                    "--claude-projects",
                    str(claude_projects),
                    "--claude-history",
                    str(claude_history),
                    "--skill-root",
                    str(skills),
                    "--output",
                    str(output),
                ],
                capture_output=True,
                check=False,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output.is_file())
            rendered = output.read_text(encoding="utf-8")
            self.assertIn("# Session Workflow Retrospective", rendered)
            self.assertIn("## Promotion Signals", rendered)
            self.assertNotIn("PRIVATE_SESSION", rendered)
            self.assertNotIn("PRIVATE_PROMPT", rendered)
            self.assertNotIn(temporary_directory, rendered)

    def test_aggregate_report_excludes_private_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            codex_sessions = root / "codex-sessions"
            claude_projects = root / "claude-projects"
            skills = root / "skills"
            handoffs = root / "handoffs"
            codex_sessions.mkdir()
            claude_projects.mkdir()
            handoffs.mkdir()
            skill = skills / "cli-tooling-governance"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: cli-tooling-governance\ndescription: Test.\n---\n",
                encoding="utf-8",
            )
            research_skill = skills / "source-backed-research"
            research_skill.mkdir(parents=True)
            (research_skill / "SKILL.md").write_text(
                "---\nname: source-backed-research\ndescription: Test.\n---\n",
                encoding="utf-8",
            )

            codex_history = root / "codex-history.jsonl"
            codex_history.write_text(
                json.dumps(
                    {
                        "session_id": "PRIVATE_SESSION",
                        "text": "继续检查 CLI 和 MCP，PRIVATE_PROMPT",
                        "ts": 1_800_000_000,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            claude_history = root / "claude-history.jsonl"
            claude_history.write_text(
                json.dumps(
                    {
                        "sessionId": "PRIVATE_CLAUDE_SESSION",
                        "display": "安装 CLI 并验证，PRIVATE_CLAUDE_PROMPT",
                        "timestamp": 1_800_000_000_000,
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            codex_records = [
                {
                    "type": "session_meta",
                    "payload": {
                        "session_id": "PRIVATE_SESSION",
                        "timestamp": "2027-01-15T00:00:00Z",
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "function_call",
                        "name": "exec_command",
                        "arguments": json.dumps(
                            {"cmd": "vercel --version", "token": "PRIVATE_TOKEN"}
                        ),
                    },
                },
            ]
            (codex_sessions / "rollout.jsonl").write_text(
                "\n".join(json.dumps(record) for record in codex_records)
                + "\nBROKEN\n",
                encoding="utf-8",
            )

            claude_records = [
                {
                    "type": "assistant",
                    "timestamp": "2027-01-16T00:00:00Z",
                    "message": {
                        "content": [
                            {
                                "type": "tool_use",
                                "name": "Bash",
                                "input": {
                                    "command": "supabase --version PRIVATE_COMMAND"
                                },
                            }
                        ]
                    },
                }
            ]
            (claude_projects / "session.jsonl").write_text(
                "\n".join(json.dumps(record) for record in claude_records) + "\n",
                encoding="utf-8",
            )
            (handoffs / "SESSION_HANDOFF.md").write_text(
                "# PRIVATE TITLE\n## 从这里恢复\n## 已完成验证\n## 仍需处理\n",
                encoding="utf-8",
            )
            generated_handoffs = handoffs / "node_modules"
            generated_handoffs.mkdir()
            (generated_handoffs / "SESSION_HANDOFF.md").write_text(
                "# Generated dependency handoff\n",
                encoding="utf-8",
            )
            inventory = root / "inventory.md"
            inventory.write_text("| `vercel` | installed |\n", encoding="utf-8")

            args = SimpleNamespace(
                codex_sessions=codex_sessions,
                codex_history=codex_history,
                claude_projects=claude_projects,
                claude_history=claude_history,
                skill_root=[skills],
                handoff_root=[handoffs],
                tool_inventory=inventory,
                since=None,
                candidate_threshold=1,
                cache=root / "tool-cache.json",
                no_cache=False,
            )
            report = analyzer.build_report(args)
            rendered = analyzer.render_markdown(report)
            cached_report = analyzer.build_report(args)

            cli_rows = {row["name"]: row for row in report["cli_tools"]}
            category_rows = {row["name"]: row for row in report["categories"]}
            self.assertEqual(cli_rows["vercel"]["sessions"], 1)
            self.assertEqual(cli_rows["supabase"]["sessions"], 1)
            self.assertTrue(cli_rows["vercel"]["documented"])
            self.assertEqual(category_rows["cli-mcp-tooling"]["sessions"], 2)
            self.assertEqual(
                category_rows["research-reference"]["coverage"],
                ["source-backed-research"],
            )
            self.assertEqual(category_rows["research-reference"]["support"], [])
            self.assertEqual(report["handoffs"]["documents"], 1)
            self.assertEqual(
                report["handoff_improvements"],
                [
                    {
                        "name": "explicit-risk-blocker-state",
                        "covered": 0,
                        "documents": 1,
                        "missing": 1,
                        "owner": "implementation-workflow",
                    }
                ],
            )
            self.assertEqual(report["summary"]["malformed_jsonl_lines"], 1)
            self.assertEqual(report["summary"]["history_files"], 2)
            self.assertEqual(report["summary"]["codex_session_files"], 1)
            self.assertEqual(report["summary"]["claude_session_files"], 1)
            self.assertEqual(report["summary"]["session_cache_hits"], 0)
            self.assertEqual(cached_report["summary"]["session_cache_hits"], 2)
            self.assertNotIn(
                temporary_directory, args.cache.read_text(encoding="utf-8")
            )
            self.assertEqual(
                report["summary"]["window_start"],
                "2027-01-15T08:00:00+00:00",
            )
            self.assertIn(
                "concrete next work in 1/1 documents",
                rendered,
            )
            self.assertIn(
                "`explicit-risk-blocker-state` missing in 1 document(s) -> "
                "`implementation-workflow`",
                rendered,
            )
            for private_value in (
                "PRIVATE_SESSION",
                "PRIVATE_PROMPT",
                "PRIVATE_CLAUDE_PROMPT",
                "PRIVATE_TOKEN",
                "PRIVATE_COMMAND",
                "PRIVATE TITLE",
                temporary_directory,
            ):
                self.assertNotIn(private_value, rendered)

    def test_subagent_sessions_do_not_count_as_codex_tool_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            record = {
                "type": "session_meta",
                "payload": {
                    "session_id": "subagent",
                    "timestamp": "2027-01-15T00:00:00Z",
                    "source": {"subagent": {}},
                },
            }
            call = {
                "type": "response_item",
                "payload": {
                    "type": "function_call",
                    "name": "exec_command",
                    "arguments": "gh --version",
                },
            }
            (root / "rollout.jsonl").write_text(
                json.dumps(record) + "\n" + json.dumps(call) + "\n",
                encoding="utf-8",
            )

            tools, _, sessions = analyzer.scan_codex_tools(root, None)

            self.assertEqual(sessions, 0)
            self.assertEqual(tools.calls, {})

    def test_object_source_without_subagent_marker_counts_as_primary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            records = [
                {
                    "type": "session_meta",
                    "payload": {
                        "session_id": "primary",
                        "timestamp": "2027-01-15T00:00:00Z",
                        "source": {"client": "cli"},
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "function_call",
                        "name": "exec_command",
                        "arguments": "gh --version",
                    },
                },
            ]
            (root / "rollout.jsonl").write_text(
                "\n".join(json.dumps(record) for record in records) + "\n",
                encoding="utf-8",
            )

            tools, _, sessions = analyzer.scan_codex_tools(root, None)

            self.assertEqual(sessions, 1)
            self.assertEqual(tools.calls["gh"], 1)

    def test_private_mcp_provider_name_is_aggregated(self) -> None:
        self.assertEqual(analyzer.mcp_provider("mcp__github__search"), "github")
        self.assertEqual(
            analyzer.mcp_provider("mcp__PRIVATE_ACCOUNT__search"), "custom"
        )
        self.assertEqual(analyzer.mcp_provider("private-mcp-tool"), "custom")

        tools = analyzer.ToolStats()
        analyzer.add_tool_call(
            tools,
            "opaque-session",
            "mcp__PRIVATE_ACCOUNT__search",
            {"cmd": "gh --version"},
        )
        self.assertEqual(tools.surfaces, {"mcp__custom__tool": 1})

    def test_cli_tokens_are_counted_once_per_tool_call(self) -> None:
        tools = analyzer.ToolStats()

        analyzer.add_tool_call(
            tools,
            "opaque-session",
            "exec_command",
            {"cmd": "python3 script.py && gh api /user && gh --version"},
        )

        self.assertEqual(tools.calls["python"], 1)
        self.assertEqual(tools.calls["gh"], 1)


if __name__ == "__main__":
    unittest.main()
