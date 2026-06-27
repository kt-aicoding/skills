# KT AI Coding Registry Reference

## Placement Matrix

| Asset shape | Preferred repository | Why |
| --- | --- | --- |
| Reusable agent instruction, workflow, checklist | `kt-aicoding/skills` | Value is behavior and judgment |
| CLI tool, installer, migration script | `kt-aicoding/cli-tools` | Value is executable command-line operation |
| Agent-callable external tool surface | `kt-aicoding/mcp-servers` | Value is live tool access in reasoning loop |
| Multi-agent review/debug/release flow | `kt-aicoding/agent-workflows` | Value is orchestration across agents/stages |
| Claude Code and Codex config kit | `kt-aicoding/claudecode-codex-config` | Value is installable config package |
| Cross-category navigation and migration candidates | `kt-aicoding/registry` | Value is discovery and governance |
| Mature single-purpose product | Dedicated repository | Independent users and release cadence |

## Migration Checklist

- Does it directly serve AI coding infrastructure?
- Does it have one clear category?
- Can it be publicly documented without private paths, accounts, or secrets?
- Does it have a minimum README, directory structure, and maintenance boundary?
- Should it be a catalog entry, monorepo item, or standalone repository?

## Registry Hygiene

- Keep registry pages short and link to canonical docs.
- Avoid copying long CLI/MCP/skill policy into registry when category repositories own it.
- Keep English and Chinese README/catalog entries aligned.
- Mark candidates as `candidate`, `evaluate`, `reference`, or `created`.
- Remove stale links when repositories are renamed.
