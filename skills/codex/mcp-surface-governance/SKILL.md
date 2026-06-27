---
name: mcp-surface-governance
description: Decide whether an AI coding capability should be exposed as an MCP server and design safe, small MCP tool surfaces. Use when updating kt-aicoding/mcp-servers, creating or reviewing MCP servers, deciding CLI versus MCP, defining MCP tool names/schemas/outputs/errors/auth, or pruning broad/default MCP surfaces.
---

# MCP Surface Governance

Use this skill to keep MCP servers narrow, explicit, and useful to coding agents.

## Workflow

1. Decide whether MCP is warranted.
2. Prefer CLI when the workflow is cloud deployment, billing/resource inspection, GitHub operations, database administration, or deterministic batch work.
3. Use MCP only when an agent needs live tool access during reasoning, such as current docs, browser automation, code context, search, or project indexing.
4. Design a small tool surface: clear verb-object names, typed inputs, structured outputs, scoped auth, and explicit failure modes.
5. Keep global/default MCP small. Enable rare or broad provider MCPs only for task-specific reasons.
6. Keep public examples sanitized: no tokens, keys, cookies, private paths, account secrets, or private project context.

## Default Boundary

- Default MCPs may include current documentation retrieval and browser automation.
- Provider MCPs for GitHub, Vercel, Supabase, and Cloudflare should not be default-enabled when mature CLIs cover the workflow.
- Filesystem, memory, sequential-thinking, and broad security MCPs should stay disabled unless a concrete workflow justifies them.

Read `references/tool-surface-scorecard.md` when designing, reviewing, or deciding whether to promote an MCP server.

## Required Checks

Before committing MCP governance or server changes:

- Confirm the tool surface is smaller than the underlying API.
- Confirm auth is scoped, revocable, and documented.
- Confirm outputs are structured enough for agent use.
- Run a secret/path scan for public docs and examples.
- Run `git diff --check`.
- If server code is added, run the smallest local startup or tool-list validation.
