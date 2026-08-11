---
name: mcp-surface-governance
description: Choose MCP versus CLI, then design narrow MCP tools with typed inputs, structured outputs, scoped auth, and clear errors.
---

# MCP Surface Governance

Use this skill to keep MCP servers narrow, explicit, and useful to coding agents.

## Workflow

1. Decide whether MCP is warranted.
2. Prefer CLI when the workflow is cloud deployment, billing/resource inspection, GitHub operations, database administration, or deterministic batch work.
3. Use MCP only when an agent needs live tool access during reasoning, such as current docs, browser automation, code context, search, or project indexing.
4. Design a small tool surface: clear verb-object names, typed inputs, structured outputs, scoped auth, and explicit failure modes.
5. For tools that read or write files, define accepted formats, size/count limits, overwrite semantics, and whether the operation is in-place. Write external-converter output to an isolated temporary location before publishing a new final file.
6. For provider-controlled downloads, check declared size when available, enforce the same byte limit while streaming, use exclusive output files, and remove partial files on failure. Never echo signed URLs or query-string credentials from transport exceptions.
7. For local file and Base64 inputs, reject unsupported formats and oversize metadata before reading or decoding, then re-check streamed/read/decoded bytes to cover races and misleading metadata.
8. Keep global/default MCP small. Enable rare or broad provider MCPs only for task-specific reasons.
9. Keep public examples sanitized: no tokens, keys, cookies, private paths, account secrets, or private project context.

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
- Confirm schemas and runtime validation enforce justified string, item-count, byte-size, dimension, timeout, and output-log bounds.
- Confirm file-producing tools require format-matching extensions and refuse existing targets unless overwrite or in-place mutation is the tool's explicit contract.
- Confirm remote responses are streamed under runtime byte limits, partial output is cleaned up, and transport errors cannot expose credential-bearing URLs.
- Confirm local files are bounded before and during access, and Base64 inputs are size-estimated before strict decoding with an actual decoded-size check.
- Run a secret/path scan for public docs and examples.
- Run `git diff --check`.
- If server code is added, run the smallest local startup or tool-list validation.
