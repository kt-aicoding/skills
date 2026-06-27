---
name: cli-tooling-governance
description: Decide, organize, document, and maintain CLI tools for KT AI Coding. Use when a task asks whether something should be a CLI, script, skill, MCP server, standalone repo, or documentation; when updating kt-aicoding/cli-tools; when designing CLI maturity, upgrade, verification, provider CLI, or command governance; or when reviewing AI coding command-line tooling.
---

# CLI Tooling Governance

Use this skill to keep CLI decisions consistent across KT AI Coding repositories.

## Workflow

1. Classify the capability: CLI, project script, skill, MCP server, docs, or standalone repo.
2. Check repository placement before editing:
   - CLI utilities and CLI operating docs: `kt-aicoding/cli-tools`
   - MCP server surfaces: `kt-aicoding/mcp-servers`
   - Agent behavior rules and workflows: `kt-aicoding/skills`
   - Cross-category navigation: `kt-aicoding/registry`
3. Prefer mature provider CLIs for cloud/source-control/database work unless there is clear agent-native value in another interface.
4. Require a minimal verification path for every CLI tool: `--help`, `doctor`, dry-run, version check, or a deterministic no-op command.
5. Keep public docs sanitized: no tokens, keys, cookies, private paths, account secrets, or private project context.

## Decision Rules

- Prefer a CLI when the work is deterministic, scriptable, auditable, and useful outside an agent session.
- Prefer a project-local script when assumptions are local to one repository.
- Prefer a skill when the value is judgment, process, checklist, or agent behavior.
- Prefer an MCP server only when an agent needs live tool access inside its reasoning loop.
- Promote a tool to a standalone repository only when it has independent users, release cadence, installation docs, and maintenance boundaries.

Read `references/decision-framework.md` when the task involves placement, maturity, upgrade policy, or anti-pattern review.

## Required Checks

Before committing CLI governance changes:

- Confirm links point to the canonical repository.
- Confirm README/docs do not duplicate canonical skill text unnecessarily.
- Run a secret/path scan for public docs.
- Run `git diff --check`.
- If a script or CLI implementation is added, run its smallest meaningful validation.
