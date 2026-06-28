---
name: goal-prompt-builder
description: Create durable, verifiable goal prompts for long-running Codex/agent work. Use when the user asks to design, refine, summarize, or generate a goal/objective prompt; convert a broad request into an active-goal objective; make a task resumable across context compaction; define completion criteria, blockers, validation evidence, or project-by-project execution loops.
---

# Goal Prompt Builder

## Purpose

Turn a broad work request into a goal prompt that an agent can execute for hours, resume safely, verify objectively, and close only when evidence proves completion.

For detailed templates and examples, read `references/goal-prompt-patterns.md`.

## Workflow

1. Identify the real finish line.
   - Name the concrete state that must be true at the end.
   - Prefer deliverables and observable behavior over activity words like "improve", "continue", or "handle".
   - Preserve the user's full scope; do not shrink it to the easiest passing subset.

2. Define the working surface.
   - Include root directories, repositories, branches, domains, services, docs, dashboards, issue/PR links, and required access prerequisites.
   - Say which files or systems must be read before continuing after a resume.
   - Refer to secret names, environment variable names, or secret-manager entries only. Do not ask the agent to read, print, summarize, or commit raw credentials.

3. Decompose into repeatable loops.
   - For multi-project work, use one complete loop per project or module.
   - A strong loop has inventory, targeted reads, implementation, local validation, live validation when applicable, commit/push or artifact publication, and ledger update.
   - State selection priority so the agent can choose the next item without asking.

4. Write evidence-based completion criteria.
   - List exact commands, checks, API calls, browser flows, remote refs, rendered outputs, or review states that prove success.
   - Require a completion audit before marking the goal complete.
   - Treat missing, indirect, narrow, or stale evidence as incomplete.

5. Add blocker policy.
   - Define which blockers are external and acceptable to record.
   - Require the agent to finish safe local work, record the blocker, then continue other items.
   - Reserve "blocked" for true impasse, not inconvenience.

6. Add change-safety rules.
   - Protect user work in dirty repositories.
   - Stage and commit only goal-related files.
   - For deployment work, prefer deploying the exact commit that was pushed.
   - Never output or commit secrets.

7. Specify final reporting.
   - Require a concise per-item summary with repo, branch, commit, deployment target, validation results, unresolved blockers, and dirty-worktree notes.
   - Include ledger/audit file paths updated during the run.

## Goal Prompt Quality Bar

A generated goal prompt should answer:

- What concrete outcome must be true?
- What artifacts, repos, services, or environments are in scope?
- What evidence proves each requirement?
- What repeatable loop should the agent run for each item?
- What must happen after context compaction or interruption?
- What may be skipped, deferred, or recorded as blocked?
- What must never happen, such as leaking secrets or reverting user work?
- What exact condition allows `complete`?

## Anti-Patterns

Avoid these weak goal shapes:

- "Make progress on X."
- "Keep working until it looks done."
- "Fix all issues" without an issue source, validator, or stop condition.
- "Deploy everything" without naming environments or verification.
- "Use best judgment" without guardrails for dirty worktrees, secrets, or blockers.
- "Mark complete when tests pass" when the scope also includes deployment, docs, or live behavior.

## Output Shape

When the user asks for a goal prompt, output:

1. A durable instruction file path and content when the full goal is complex.
2. A paste-ready short `/goal` command under 4,000 characters.
3. A compact `create_goal` objective string when useful.
4. Material assumptions and pause conditions that affect scope or validation.

When the user asks to install or publish the skill, create a standard skill folder with `SKILL.md`, optional `references/`, `agents/openai.yaml`, run validation, then commit and push.
