---
name: implementation-workflow
description: Write implementation plans, execute existing plans, or finish verified branches with safe commit, PR, merge, and handoff choices.
---

# Implementation Workflow

Run a complete implementation lifecycle without forcing every request through every phase.

## Select the Phase

- **Plan:** Requirements exist, but no implementation plan exists.
- **Execute:** A written plan or ordered task list exists and work remains.
- **Finish:** Implementation is complete and needs an evidence audit or Git handoff.

Run only the phase the user requested. Continue into the next phase only when the request clearly
includes it. Use `references/templates.md` when writing a persistent plan or delegating work.

## Guardrails

1. Read the nearest `AGENTS.md`, then relevant project docs and current git state.
2. Preserve unrelated dirty-worktree changes. Never reset, overwrite, stage, or commit them.
3. Use the built-in plan for execution tracking. Mark a task complete only after its evidence passes.
4. Prefer the narrowest meaningful test after each slice, then broader checks at integration points.
5. Do not commit, push, create a PR, merge, deploy, or delete work unless the user requested that
   action or explicitly selects it during the Finish phase.
6. Stop for a material product choice, destructive action, missing authority, or repeated verification
   failure. Continue through ordinary implementation details using repository evidence.

## Plan Phase

1. Inspect the requirements and the code paths they affect. Identify existing patterns, tests,
   dependencies, and project-specific commands before proposing file changes.
2. Lock the intended file responsibilities and data flow. Avoid unrelated restructuring.
3. Split the work into ordered vertical slices. Each task must state:
   - outcome and acceptance criteria;
   - exact create/modify/test paths when they are knowable;
   - dependencies and ownership boundaries;
   - implementation notes needed to avoid rediscovery;
   - exact verification commands or observable checks.
4. Keep tasks independently verifiable. Prefer slices that take roughly 15–60 minutes for an agent;
   use smaller steps only for fragile migrations or test-first behavior.
5. Include explicit failing-test steps only when behavior is risky enough to justify TDD. Do not
   invent code snippets or expected errors that have not been grounded in the repository.
6. Save the plan when the user requested a durable artifact or execution will continue later. Follow
   the repository convention; otherwise use `docs/plans/YYYY-MM-DD-<slug>.md`.
7. Self-review the plan for requirement coverage, unsupported assumptions, missing validation,
   conflicting names or types, and placeholders. Fix the plan before handoff.

## Execute Phase

1. Read the complete plan, current instructions, current diff, and recent relevant changes.
2. Challenge the plan against the current repository. Fix small stale details in the plan; stop for
   material scope or architecture changes that alter the requested outcome.
3. Translate plan tasks into the built-in plan and execute in dependency order.
4. Choose the execution mode:
   - **Inline:** use for tightly coupled work, one or two tasks, shared files, or changes needing one
     continuous mental model.
   - **Delegated:** use when two or more bounded tasks are genuinely independent and subagents are
     available. This skill explicitly authorizes subagents for those bounded implementation or
     read-only review tasks.
5. When delegating, remember all agents share the same filesystem. Assign non-overlapping write
   scopes, name exact files, and never let two implementers edit the same surface concurrently.
   Keep shared-file integration with the primary agent.
6. Give each implementer the full task text, relevant context, allowed paths, acceptance criteria,
   validation command, and explicit non-goals. Do not make it reconstruct the plan from scratch.
7. For every task:
   - record the pre-task state;
   - implement only the specified slice;
   - run its targeted verification;
   - inspect the actual diff;
   - report `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, or `NEEDS_CONTEXT`;
   - resolve open concerns before marking the task complete.
8. Use separate spec-compliance and code-quality reviews for security-sensitive, high-risk, or broad
   changes. For routine slices, use one independent review or a primary-agent diff review instead of
   spending three agents on mechanical work.
9. Re-run integration checks after dependent tasks meet. Do not continue past repeated failures by
   weakening tests or silently changing acceptance criteria.

## Finish Phase

1. Inspect `git status`, the full task-related diff, the plan, and every promised deliverable.
2. Run the authoritative targeted and integration checks. Record commands and outcomes.
3. Audit requirement coverage, documentation impact, migrations, generated artifacts, secrets,
   unrelated changes, and remaining blockers.
4. If the user asked only for implementation, stop with a handoff: completed work, validation,
   remaining risks, branch state, and uncommitted files.
5. If the user requested Git integration, offer only applicable safe choices:
   - keep the branch and worktree as-is;
   - commit task-related changes and stop;
   - push and create or update a PR;
   - merge locally into the confirmed base branch.
6. Never offer discard as a routine choice. Perform deletion only after the user explicitly requests
   it, list the exact branch, commits, worktree, and uncommitted files affected, and receive explicit
   confirmation.
7. Re-run verification after a merge. Remove a worktree only when its changes are safely integrated
   or the user explicitly approved deletion.

## Completion Report

Report:

- phase and tasks completed;
- files or systems changed;
- verification commands and results;
- branch, commit, PR, or deployment state when applicable;
- unresolved risks, blockers, and unrelated dirty-worktree changes.

Never claim completion from an implementer report alone. Verify the actual artifacts and evidence.
