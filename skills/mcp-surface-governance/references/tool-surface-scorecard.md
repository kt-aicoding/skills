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
| Outputs | Structured actionable fields with bounded previews/logs | Long unbounded logs or inline media |
| Permissions | Narrow, scoped, revocable | Broad account access by default |
| Failure mode | Clear error category and retry guidance | Silent or ambiguous failures |
| State | Explicit and inspectable | Hidden session assumptions |
| File writes | Format-matching new targets; in-place behavior is explicit | Silent overwrite or extension/content mismatch |
| Resource use | Schema and runtime agree on count, size, dimensions, and timeouts | Bounds exist only in docs or only in schema |

## File-Producing Tools

- Validate the final extension against the actual encoded format.
- Refuse an existing target by default. Allow overwrite or in-place mutation only when the tool name, description, and result make that behavior explicit.
- Validate all inputs and target collisions before expensive generation, decoding, rendering, or subprocess work.
- For external converters, generate in an isolated temporary directory, verify the expected artifact exists, then publish it to the already-validated final path.
- Return the saved path and concise metadata. Inline only bounded previews; direct the agent to the saved file for large media.

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
| Trusting JSON Schema as the only validation | Enforce the same limits at the runtime boundary |
| Letting converters write directly over final targets | Convert in isolation, verify, then publish a new file |
| Storing secrets in MCP examples | Use placeholders and explicit setup instructions |
