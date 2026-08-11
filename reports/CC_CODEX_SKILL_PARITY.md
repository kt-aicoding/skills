# Claude Code and Codex Skill Parity

This report compares active top-level Claude Code skills with enabled Codex skills. It stores names and aggregate counts only; it does not include prompts or credentials.

## Summary

- Claude skill entries: 137
- Claude unique skill names: 135
- Codex enabled skills: 156
- Shared names: 97
- Claude-only names: 38
- Codex-only names: 59
- Claude commands: 15
- Claude subagents: 15
- Claude plugins: 18 installed, 0 enabled, 18 disabled

A full Claude-to-Codex migration is unsafe here because it would overwrite shared Codex skills that already have native policy and metadata. Use the decisions below instead of copying the entire Claude directory.

## Shared skill parity

| Parity | Skills |
| --- | --- |
| exact | 62 |
| modified | 35 |

## Claude explicit usage evidence

| Skill | Sessions | Invocations |
| --- | --- | --- |
| frontend-design | 17 | 33 |
| design-flow | 2 | 2 |
| kimi-project-launch | 1 | 1 |

## Claude-only: covered

| Claude Skill | Codex target | Decision notes |
| --- | --- | --- |
| context-restore | checkpoint | Codex checkpoint owns resumable working-state capture and restore. |
| context-save | checkpoint | Codex checkpoint owns resumable working-state capture and restore. |
| diagram | skill-image | Use the Codex visual-tool router before adding another diagram workflow. |
| document-generate | document-release, repo-readme-release | Existing Codex documentation workflows cover project and release documentation. |
| executing-plans | implementation-workflow | Merged into the Codex-native plan, execute, verify, and handoff workflow. |
| finishing-a-development-branch | implementation-workflow | Merged into the Codex-native branch handoff phase. |
| make-pdf | pdf | The Codex PDF Skill owns creation and layout verification. |
| receiving-code-review | gh-address-comments, implementation-workflow | Use evidence-based comment handling and verified implementation handoff. |
| requesting-code-review | review, find-bugs | Existing Codex review Skills cover pre-landing review and defect finding. |
| scrape | firecrawl-build-scrape, browse | Use product-integrated scraping or browser extraction according to the task. |
| ship | implementation-workflow, land-and-deploy | Split safe branch handoff from explicit landing and deployment. |
| skillify | skill-creator | Create durable browser workflows through the Codex Skill authoring process. |
| spec | implementation-workflow | The Codex-native workflow starts with requirements and implementation planning. |
| subagent-driven-development | implementation-workflow | Merged as the optional bounded-subagent execution mode. |
| systematic-debugging | investigate | The Codex investigate Skill preserves root-cause-first debugging. |
| test-driven-development | implementation-workflow | Testing and false-positive review are integrated into the Codex implementation workflow. |
| using-git-worktrees | implementation-workflow | Worktrees are optional isolation, not a mandatory standalone workflow. |
| verification-before-completion | implementation-workflow | Evidence-based verification is a required implementation phase. |
| writing-plans | implementation-workflow | Merged into the Codex-native planning phase. |
| writing-skills | skill-creator | The built-in Codex Skill creator owns authoring and validation. |

## Claude-only: native

| Claude Skill | Codex target | Decision notes |
| --- | --- | --- |
| dispatching-parallel-agents | Codex subagents | Codex provides native bounded subagent delegation. |

## Claude-only: defer

| Claude Skill | Codex target | Decision notes |
| --- | --- | --- |
| benchmark-models | — | Cross-model gstack benchmarking has no retained explicit use and no direct Codex equivalent. |
| create-colleague | — | Requires a privacy and connector redesign for Feishu or DingTalk data. |
| ios-clean | — | Specialized gstack DebugBridge cleanup has no retained usage evidence. |
| ios-design-review | ios-design-guidelines | Keep the platform guideline Skill; migrate live-device tooling only when iOS work resumes. |
| ios-fix | ios-design-guidelines | Autonomous device fixing needs a current iOS toolchain validation before migration. |
| ios-qa | ios-design-guidelines | Live-device QA needs a current iOS toolchain validation before migration. |
| research | — | Redesign the five-part Claude agent pipeline as one Codex-native research workflow only when reused. |
| research-add-fields | — | Part of the unused Claude-specific research pipeline. |
| research-add-items | — | Part of the unused Claude-specific research pipeline. |
| research-deep | — | Depends on Claude Task semantics and a fixed web-search agent prompt. |
| research-report | — | Part of the unused Claude-specific research pipeline. |

## Claude-only: retire

| Claude Skill | Codex target | Decision notes |
| --- | --- | --- |
| ios-sync | — | Synchronizes Claude-oriented gstack DebugBridge templates. |
| kimi-project-launch | deploy-to-vercel, volcengine-ark-migration | Contains stale GLM defaults and obsolete workspace paths; use current deployment and provider Skills. |
| landing-report | — | Dashboard is coupled to the disabled Claude-oriented gstack ship workflow. |
| plan-tune | — | Internal gstack psychographic tuning is not needed for Codex routing. |
| setup-gbrain | — | Claude/gstack brain bootstrap is not part of the current Codex setup. |
| sync-gbrain | — | Claude/gstack brain synchronization is not part of the current Codex setup. |

## Claude metadata findings

- Missing declared `name` (directory fallback used): research, research-add-fields, research-add-items, research-deep, research-report
- Broken top-level symlinks: none
- Duplicate Claude names: gstack (_gstack-command, gstack); open-gstack-browser (connect-chrome, open-gstack-browser)

## Codex-only skills

`agent-productization`, `anycap-ai-tool-seo`, `anycap-blog-production`, `anycap-cli`, `anycap-deepresearch`, `anycap-gemini-omni-video-edit`, `anycap-human-interaction`, `anycap-media-production`, `anycap-social-meme-workflows`, `anycap-worldcup-predict`, `chatgpt-apps`, `checkpoint`, `cli-creator`, `cli-tooling-governance`, `cli-tooling-inventory`, `codex-mcp-profiles`, `configure-custom-domain`, `define-goal`, `gh-address-comments`, `gh-fix-ci`, `goal-prompt`, `gstack-openclaw-ceo-review`, `gstack-openclaw-investigate`, `gstack-openclaw-office-hours`, `gstack-openclaw-retro`, `imagegen`, `implementation-workflow`, `jd-shopping`, `jupyter-notebook`, `kevinten10-supabase`, `kt-aicoding-registry`, `mcp-server-release`, `mcp-surface-governance`, `media-production-pipeline`, `migrate-to-codex`, `openai-docs`, `pdf`, `playwright`, `playwright-interactive`, `plugin-creator`, `print-hp-m1005-usb`, `project-workspace-triage`, `repo-readme-release`, `screenshot`, `security-best-practices`, `security-ownership-map`, `security-threat-model`, `session-workflow-retrospective`, `skill-creator`, `skill-image`, `skill-installer`, `source-backed-research`, `speech`, `submit-12315-complaint`, `taobao-shopping`, `transcribe`, `volcengine-ark-migration`, `wechat-local-history`, `workspace-noise-cleanup`
