---
name: session-workflow-retrospective
description: Analyze local Codex/Claude sessions and handoffs to identify repeated workflows, Skill coverage, and evidence-backed CLI or MCP gaps.
---

# Session Workflow Retrospective

Turn retained local work history into reusable capabilities without copying private prompts into reports or public Skills.

## Workflow

1. Establish the evidence boundary. Use retained Codex and Claude histories, primary-session logs, and explicitly selected handoff roots. Exclude subagents from frequency decisions unless the user asks otherwise.
2. Run the bundled analyzer. Keep its report local and review aggregate counts, never raw transcript excerpts:

   ```bash
   python3 scripts/analyze_session_workflows.py \
     --handoff-root /path/to/projects \
     --tool-inventory /path/to/tool-inventory.md \
     --output /tmp/session-workflow-retrospective.md
   ```

   Unchanged tool-session files are read from a local aggregate cache under `~/.cache/session-workflow-retrospective/`. Use `--no-cache` for a deliberate full rescan. The cache contains only hashed file/session identifiers and aggregate counters.

3. Compare high-frequency categories with installed Skills. Reuse or improve an existing Skill when it already owns the workflow.
4. Classify each genuine gap using `references/promotion-rubric.md`. Prefer a bundled script for deterministic private-data aggregation, a CLI for portable deterministic operations, and MCP only for agent-native live tool access.
5. Implement one evidence-backed improvement at a time. Keep private counts and project context out of public Skill bodies and repository catalogs.
6. Validate the artifact through its canonical repository, then rerun the analyzer to confirm that the gap is now covered or intentionally deferred.

## Interpretation Rules

- Frequency is a discovery signal, not proof that a new capability is needed.
- Require recurrence across multiple sessions and dates; one long session is not a reusable workflow.
- Distinguish workflow ownership from supporting tools. A browser, provider Skill, CLI, or MCP can enable a task without defining its evidence, sequencing, or completion gates.
- Repeated corrective prompts usually indicate an existing workflow needs clearer gates before they justify a new Skill.
- Repeated handoff-schema gaps belong in the existing implementation or checkpoint workflow unless the retained evidence shows a distinct trigger and owner.
- A referenced but missing executable is only an installation candidate after confirming that an existing CLI cannot cover it.
- Do not install or enable an MCP server merely because its name appears in history. Require a live, typed, agent-loop use case that is not better served by CLI or browser tooling.
- Never emit prompts, command arguments, tool outputs, session IDs, working directories, tokens, or account identifiers in the aggregate report.

## Required Checks

- Inspect current installed Skill roots before proposing a new name.
- Verify candidate CLIs with `command -v` and a non-mutating version/help command.
- Verify MCP configuration separately; transcript evidence only proves historical use, not current availability.
- Run the analyzer tests and the Skill validator after changes.
- Scan generated/public artifacts for private paths and secrets.
