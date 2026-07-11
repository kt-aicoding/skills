# MCP Surface Governance Reference

## MCP Decision Framework

| Question | If yes | If no |
| --- | --- | --- |
| Does the agent need this tool during reasoning? | MCP may be appropriate | Prefer CLI or docs |
| Is this already covered by a mature CLI? | Use CLI unless MCP adds unique value | MCP may be useful |
| Can the tool surface be small and explicit? | Continue design | Do not expose broad APIs |
| Can auth be scoped and explained safely? | Continue design | Do not default-enable |
| Are outputs deterministic enough for agent use? | Continue design | Keep manual or CLI-based |

## Tool Surface Scorecard

| Criterion | Good | Risky |
| --- | --- | --- |
| Tool name | Verb-object and domain-specific | Generic `run` or `execute` |
| Inputs | Small typed schema | Free-form blobs without constraints |
| Outputs | Structured actionable fields | Long unbounded logs |
| Permissions | Narrow, scoped, revocable | Broad account access by default |
| Failure mode | Clear error category and retry guidance | Silent or ambiguous failures |
| State | Explicit and inspectable | Hidden session assumptions |

## Maturity Model

| Stage | Form | Promotion condition |
| --- | --- | --- |
| Design note | `docs/` MCP boundary or design | Clear tool surface and permission boundary |
| Prototype | `servers/<server-name>/` experiment | Runs locally with minimal client config |
| Usable server | Install/config/tool docs complete | Stable inputs/outputs and predictable errors |
| Standalone server | Separate repository | Independent users, versioning, and maintenance plan |

## Anti-Patterns

| Anti-pattern | Preferred approach |
| --- | --- |
| Turning every API into MCP | Start with one narrow workflow |
| Duplicating mature provider CLIs | Use provider CLI and document commands |
| Long-lived global MCPs for rare tasks | Enable task-specific tools only when needed |
| Returning unbounded raw logs | Return structured summaries and links to logs |
| Storing secrets in MCP examples | Use placeholders and explicit setup instructions |
