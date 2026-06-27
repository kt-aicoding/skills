---
name: kt-aicoding-registry
description: Route AI coding assets to the correct kt-aicoding repository and keep registry/catalog documentation consistent. Use when adding, moving, or classifying skills, CLI tools, MCP servers, agent workflows, configuration kits, migration candidates, README/catalog entries, or organization-level governance docs in kt-aicoding.
---

# KT AI Coding Registry

Use this skill to maintain the organization boundary and keep cross-repository indexes consistent.

## Workflow

1. Classify the asset before editing.
2. Choose the canonical repository:
   - `kt-aicoding/skills`: reusable agent instructions, workflows, and checklists
   - `kt-aicoding/cli-tools`: command-line utilities and CLI governance docs
   - `kt-aicoding/mcp-servers`: MCP server implementations and MCP surface governance docs
   - `kt-aicoding/agent-workflows`: multi-agent orchestration and automation templates
   - `kt-aicoding/claudecode-codex-config`: Claude Code and Codex configuration kit
   - `kt-aicoding/registry`: cross-category index, migration candidates, and organization boundaries
3. Keep implementation details in the category repository. Keep `registry` as an index, not a duplicate source of truth.
4. Update README/catalog links when canonical documents move.
5. Keep public docs sanitized: no tokens, keys, cookies, private paths, account secrets, or private project context.

## Decision Rules

- Use `registry` to answer "where should this live?"
- Use category repositories to answer "how does this work?"
- Promote mature assets into standalone repositories only after there are independent users, versioning needs, and clear ownership.
- Keep broad apps, creative demos, and generic AI experiments outside `kt-aicoding` unless they directly serve AI coding infrastructure.

Read `references/repository-placement.md` when classifying assets, updating catalogs, or deciding whether to migrate a project.

## Required Checks

Before committing registry changes:

- Confirm each link points to the canonical repository.
- Confirm category docs do not duplicate full content from another repo.
- Update both English and Chinese indexes when present.
- Run a secret/path scan for public docs.
- Run `git diff --check`.
