# Workflow Templates

Use only the template needed for the active phase.

## Persistent Plan

```markdown
# <Feature> Implementation Plan

**Outcome:** <observable finished state>
**Scope:** <repositories, packages, or services>
**Constraints:** <safety, compatibility, and non-goals>

## Task 1: <vertical slice>

**Outcome:** <what becomes true>
**Files:**
- Create: `<path>`
- Modify: `<path>`
- Test: `<path>`

**Implementation notes:**
- <repository-grounded decisions and interfaces>

**Acceptance criteria:**
- <observable behavior>

**Verification:**
- `<exact command>` -> <expected signal>

## Completion audit

- [ ] Every requirement maps to a completed task.
- [ ] Targeted and integration checks pass.
- [ ] Documentation and migration impact is resolved.
- [ ] Git state and remaining blockers are reported.
- [ ] Incomplete work has an authoritative resume source and a concrete first next action.
```

## Implementer Request

Provide:

```text
Task: <name and full task text>
Context: <why this slice exists and its dependencies>
Write scope: <exact files or directory; no other edits>
Acceptance criteria: <complete list>
Verification: <exact command or observable check>
Non-goals: <explicit exclusions>
Git policy: <whether commits are allowed; default no>

Ask before starting if a requirement, dependency, or boundary is unclear.
When finished, report:
- Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
- Files changed
- Verification and result
- Self-review findings
- Remaining concerns
```

## Resume / Handoff

Use for incomplete work, multi-session work, or a durable implementation handoff. Keep every
heading; write `None` rather than omitting an empty risk or blocker section.

```markdown
# <Task> Handoff

## Current State
<what is true now and which artifact is authoritative>

## Completed Decisions And Work
- <completed item or accepted decision>

## Verification Evidence
- `<command or check>` -> <result>

## Remaining Work And First Next Action
- Remaining: <specific incomplete outcome or None>
- First next action: `<exact command or concrete action>`
- Resume source: `<plan, report, issue, or file>`

## Risks And Blockers
- Risks: <known risk or None>
- Blocker: <blocking condition or None>
- Needed input or state change: <exact requirement or None>

## Files And Git State
- Changed or authoritative files: <paths>
- Branch/commit/PR/deployment: <state>
- Unrelated dirty worktree changes: <paths or None>
```

## Spec-Compliance Review

```text
Review the actual implementation against the task requirements. Treat the implementer's report as
an unverified claim. Read the changed code and tests. Report missing behavior, extra scope, and
misinterpreted requirements with file and line evidence. Return PASS only when the implementation
matches the requested slice exactly. Do not edit files.
```

## Code-Quality Review

Run only after spec compliance passes.

```text
Review the verified task diff for correctness, security, regressions, maintainability, and false-
positive tests. Lead with concrete findings ordered by severity and include file and line evidence.
Ignore style-only preferences. Return PASS when no material issue remains. Do not edit files.
```
