# CLI Tooling Governance Reference

## Placement Matrix

| Capability shape | Best home | Reason |
| --- | --- | --- |
| Repeatable command sequence with clear inputs and outputs | CLI tool | Easy to test, compose, document, and run outside an agent |
| Project-local one-off automation | Project script | Keeps context and assumptions local |
| Agent behavior, review checklist, operating procedure | Skill | Value is instruction and judgment |
| Agent-native access to external context or browser state | MCP server | Value is live access inside the agent loop |
| Cloud deployment, billing/resource inspection, env management | Provider CLI | Mature CLIs are more deterministic and auditable |

## Maturity Model

| Stage | Form | Promotion condition |
| --- | --- | --- |
| Record | `docs/` operating note | Repeated use and clear command sequence |
| Prototype | `tools/<tool-name>/` script | `--help`, error handling, and minimal validation |
| Tool | Installable/versioned CLI | README, examples, release notes, stable arguments |
| Standalone project | Separate repository | Independent users, roadmap, and maintenance boundary |

## Upgrade Policy

| Tool class | Policy |
| --- | --- |
| Agent CLI patch updates | Low risk; verify `codex doctor --json` and `codex mcp list` |
| Package manager major versions | Do not auto-upgrade; can affect lockfiles and scripts |
| Provider CLIs | Monthly version check; upgrade only for task need or security fix |
| Railway CLI | Upgrade/authenticate only when Railway resource checks or deployments are needed |

## Anti-Patterns

| Anti-pattern | Preferred approach |
| --- | --- |
| Wrapping every provider CLI in custom scripts | Use provider CLI directly until repetition is proven |
| Enabling provider MCPs by default | Keep provider MCPs task-specific |
| Global upgrades without a project need | Upgrade during maintenance windows with verification |
| Storing machine-local state in public docs | Keep public docs sanitized and private inventory local |
| Building a tool before writing the command sequence | Document the manual sequence first, then automate |

## Reference Checklist

- The tool has a specific AI coding workflow purpose.
- It does not duplicate a mature existing CLI without a reason.
- It has a documented command surface.
- It avoids committed secrets, private paths, and personal machine state.
- It can be verified with a small deterministic command.
- It has a promotion path: docs -> script -> CLI -> standalone repository.
