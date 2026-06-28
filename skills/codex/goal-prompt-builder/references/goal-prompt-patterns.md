# Goal Prompt Patterns

Use this reference when generating a durable goal prompt, especially for long-running repo, deployment, migration, QA, audit, or documentation work.

## Research Basis

- OpenAI prompt guidance: give clear instructions, define output shape, and provide context that removes ambiguity.
- OpenAI eval practice: define observable success criteria before relying on a result.
- SMART goals: make goals specific and measurable; use the idea without forcing artificial deadlines.
- Implementation intentions: encode blocker and continuation behavior with "if this happens, then do that" rules.
- Long-running agent practice: store state in files, verify from current state after resumes, and avoid relying on chat memory.

Useful public references:

- OpenAI Prompt Engineering Guide: https://platform.openai.com/docs/guides/prompt-engineering
- OpenAI Evals Guide: https://platform.openai.com/docs/guides/evals
- SMART criteria overview: https://en.wikipedia.org/wiki/SMART_criteria
- Implementation intentions overview: https://en.wikipedia.org/wiki/Implementation_intention

## Full Goal Prompt Skeleton

```text
Goal:
Complete <concrete outcome> across <scope>. Work item by item until every in-scope item is either completed with evidence or recorded with a specific external blocker and next action.

Workdir:
<absolute path or repo root>

Must read before continuing:
1. <objective/spec file>
2. <playbook/skill path>
3. <checklist/ledger path>
4. <completion audit path, if it exists>
5. <secret/env path, if needed; do not output secrets>

Scope:
- In scope: <projects/modules/environments>
- Out of scope: <explicit exclusions>
- Priority: <which items first and why>

Core rules:
1. Preserve the original scope; do not redefine success around partial progress.
2. Work one item at a time and close the loop before moving on.
3. Protect dirty worktrees: identify existing changes, stage only related files, never revert user work unless explicitly asked.
4. Never output or commit secrets.
5. Prefer existing project patterns, scripts, and deployment workflows.

Per-item loop:
1. Inventory the item: repo, branch, remote, runtime entrypoints, docs, env examples, deployment, domains.
2. Read the targeted files needed for this item.
3. Implement the smallest complete change that satisfies the goal.
4. Run local validators: <lint/test/typecheck/build/scan commands>.
5. Run functional smoke tests using real integrations where safe.
6. Deploy or publish if the item has a deployment surface.
7. Verify live behavior by API/browser/CLI and inspect errors.
8. Commit and push only related files.
9. Update <ledger/checklist> with evidence and blockers.

Blocker policy:
- If <external auth/platform/domain/service> blocks completion, finish safe local work, record the blocker, required permission, next command, and continue another item.
- Do not stop the whole goal because one item is blocked.
- Mark the goal blocked only when no meaningful item can progress and the same blocker has repeated under the configured blocked audit rule.

Completion audit:
Before marking complete:
1. Derive every explicit requirement from this goal and referenced files.
2. For each requirement, identify authoritative evidence.
3. Inspect current-state evidence: files, command output, tests, remote refs, deployment state, browser/API behavior.
4. Treat weak, stale, or narrow evidence as incomplete.
5. Update the completion audit file.
6. Mark complete only when all requirements are completed or recorded as acceptable external blockers under this goal.

Final report:
- List completed items.
- For each item include repo/branch/commit, deployment/domain, changes, validators, live verification, blockers, and unrelated dirty work.
- State any remaining non-goal cleanup separately.
```

## `create_goal` Objective Shape

Use a compact objective when a tool accepts only a single objective string:

```text
Complete <outcome> across <scope>; for each item run <loop>; verify with <commands/live checks>; commit/push or publish related changes; update <ledger>; protect dirty work and secrets; record external blockers with next actions and continue; mark complete only after a current-state completion audit proves every requirement is done or acceptably blocked.
```

## Batch Project Goal Pattern

Use this when a user has many repositories or sites:

```text
Process repositories under <root> one at a time. Prioritize <P0 criteria>. For each repo, scan, identify runtime/docs/deploy surfaces, make scoped changes, run existing validators, run real smoke tests, verify live domain when present, commit/push to the tracked branch, confirm remote ref, and update <checklist>. If a repo is blocked by platform auth, missing schema, unavailable hardware, or paid external operation, record the exact blocker and continue the next repo.
```

## Completion Audit Checklist

```text
- [ ] Objective/spec files reread after the latest resume.
- [ ] All in-scope items enumerated from current state, not memory.
- [ ] Each item has a status: completed, not applicable, or externally blocked.
- [ ] Completed items have validation evidence.
- [ ] Pushed items have remote refs matching local commits.
- [ ] Deployed items have live verification evidence.
- [ ] Root ledgers/checklists are updated.
- [ ] Secret scans or sensitive-output checks passed when relevant.
- [ ] Remaining findings are explicitly classified as non-goal, docs-only, optional provider, historical, or external blocker.
```

## Example: Long Migration Goal

```text
Complete the remaining provider migration for all projects under /path/to/projects. Use the local migration skill and checklist. For each project, scan old provider usage, migrate runtime configuration, update deployment secrets, run local validators and real smoke tests, verify the live domain when present, commit/push to GitHub, and update the migration checklist. Do not output or commit real API keys. If platform login, database schema, special model capability, or unavailable local tooling blocks an item, record the blocker and continue the next project. Mark complete only after a current-state audit proves no unrecorded production runtime dependency remains and all P0/P1 projects are completed, not applicable, or externally blocked with next actions.
```
