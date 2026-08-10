# Capability Promotion Rubric

Use this rubric only after the aggregate report identifies recurrence. Do not promote raw conversation content.

## Evidence Gate

A candidate is strong when it appears in at least three primary sessions, spans at least two dates, has a stable desired outcome, and still requires repeated rediscovery or correction. Lower-frequency candidates need stronger risk or reliability evidence.

## Placement

| Artifact | Choose when | Do not choose when |
| --- | --- | --- |
| Existing Skill update | The workflow already has a clear owner but misses a gate, decision rule, or recurring edge case. | The change is only personal session context. |
| New Skill | The reusable value is judgment, sequencing, validation, or agent behavior across projects. | An installed Skill already owns the same trigger. |
| Bundled script | A Skill repeatedly needs deterministic parsing, aggregation, transformation, or validation. | The operation is broadly useful outside that Skill. |
| Project script | Assumptions and inputs belong to one repository. | Multiple unrelated projects need the same command. |
| CLI | The operation is deterministic, auditable, portable, and useful outside agent sessions. | The value is mainly decision-making or live agent context. |
| MCP server | An agent needs typed live access inside its reasoning loop and scoped MCP access is safer or materially more capable. | A mature CLI, local filesystem access, or browser automation already covers the task. |
| Playbook/reference | The material is explanatory or provider-specific and changes independently from the core workflow. | A deterministic repeated operation should be scripted. |

## Promotion Checks

1. Search installed and repository Skills for overlapping descriptions and triggers.
2. Identify the canonical repository before editing.
3. Define one observable success case and one failure/stop condition.
4. Add the narrowest deterministic test or dry run.
5. Keep examples generic and sanitized.
6. Re-run the retrospective and record whether the candidate is covered, deferred, or rejected.
