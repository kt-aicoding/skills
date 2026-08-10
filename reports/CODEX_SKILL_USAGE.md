# Codex Skill Usage Audit

Evidence window: `2026-02-17T11:16:10.544Z` to `2026-08-10T01:43:06.138Z`. Retained sessions: **116** (105 primary, 11 subagent).

This report stores aggregate session counts only. It does not include prompts, tool output, working directories, or session identifiers. A session counts as usage when the user explicitly mentions `$skill` or Codex reads that skill's `SKILL.md`. `no-evidence` means no match in retained logs, not that the skill was never used.

## Summary

- Installed and enabled skills: 148
- Implicit skills: 53
- Explicit-only skills: 95
- Implicit description characters: 8506
- Used implicit bodies over 500 lines: 8
- Implicit skills with at least 2 retained sessions missing complete UI metadata: 0
- Frequent threshold: 5 sessions
- Intentional implicit keep list: 7
- frequent: 23
- no-evidence: 79
- rare: 22
- used: 24

## Frequent skills

| Skill | Sessions | Primary | Explicit | Reads | Policy | Owner | Description | Signal |
| --- | ---: | ---: | ---: | ---: | --- | --- | ---: | --- |
| anycap-cli | 50 | 50 | 0 | 50 | implicit | user | 138 | keep |
| frontend-design | 43 | 43 | 0 | 43 | implicit | shared | 134 | keep |
| playwright | 35 | 35 | 0 | 35 | implicit | user | 135 | keep |
| web-design-guidelines | 26 | 26 | 0 | 26 | implicit | shared | 138 | keep |
| imagegen | 25 | 25 | 0 | 25 | implicit | system | 570 | system-managed-description |
| browse | 19 | 19 | 0 | 19 | implicit | shared | 133 | keep |
| project-workspace-triage | 16 | 16 | 0 | 16 | implicit | user | 133 | keep |
| careful | 13 | 13 | 0 | 13 | implicit | shared | 134 | keep |
| cli-tooling-inventory | 13 | 13 | 0 | 13 | implicit | user | 343 | shorten-used-description |
| goal-prompt | 10 | 10 | 9 | 3 | implicit | shared | 135 | keep |
| workspace-noise-cleanup | 10 | 10 | 0 | 10 | implicit | user | 130 | keep |
| implementation-workflow | 9 | 9 | 0 | 9 | implicit | shared | 129 | keep |
| skill-creator | 8 | 8 | 0 | 8 | implicit | system | 225 | system-managed-description |
| cli-tooling-governance | 7 | 7 | 0 | 7 | implicit | shared | 128 | keep |
| mcp-surface-governance | 7 | 7 | 0 | 7 | implicit | shared | 121 | keep |
| pdf | 7 | 7 | 0 | 7 | implicit | user | 133 | keep |
| investigate | 6 | 6 | 0 | 6 | implicit | shared | 137 | keep |
| kt-aicoding-registry | 6 | 6 | 0 | 6 | implicit | shared | 132 | keep |
| openai-docs | 6 | 6 | 0 | 6 | implicit | system | 447 | system-managed-description |
| configure-custom-domain | 5 | 5 | 0 | 5 | implicit | user | 131 | keep |
| deploy-to-vercel | 5 | 5 | 0 | 5 | implicit | shared | 130 | keep |
| gstack-upgrade | 5 | 5 | 0 | 5 | implicit | shared | 131 | keep |
| skill-image | 5 | 5 | 0 | 5 | implicit | shared | 138 | keep |

## Review signals

### Implicit descriptions over 140 chars with at least 1 retained session

| Skill | Sessions | Primary | Explicit | Reads | Policy | Owner | Description | Signal |
| --- | ---: | ---: | ---: | ---: | --- | --- | ---: | --- |
| cli-tooling-inventory | 13 | 13 | 0 | 13 | implicit | user | 343 | shorten-used-description |

### Frequently used explicit-only skills

No explicit-only skill crossed the frequent threshold.

### System-managed long descriptions

| Skill | Sessions | Primary | Explicit | Reads | Policy | Owner | Description | Signal |
| --- | ---: | ---: | ---: | ---: | --- | --- | ---: | --- |
| imagegen | 25 | 25 | 0 | 25 | implicit | system | 570 | system-managed-description |
| skill-creator | 8 | 8 | 0 | 8 | implicit | system | 225 | system-managed-description |
| openai-docs | 6 | 6 | 0 | 6 | implicit | system | 447 | system-managed-description |
| skill-installer | 2 | 2 | 0 | 2 | implicit | system | 225 | system-managed-description |
| plugin-creator | 1 | 1 | 0 | 1 | implicit | system | 471 | system-managed-description |

### Intentional implicit capabilities without retained evidence

| Skill | Sessions | Primary | Explicit | Reads | Policy | Owner | Description | Signal |
| --- | ---: | ---: | ---: | ---: | --- | --- | ---: | --- |
| chatgpt-apps | 0 | 0 | 0 | 0 | implicit | user | 133 | keep-implicit-capability |
| figma-implement-design | 0 | 0 | 0 | 0 | implicit | shared | 137 | keep-implicit-capability |
| fixing-accessibility | 0 | 0 | 0 | 0 | implicit | shared | 140 | keep-implicit-capability |

### Implicit skills with no retained evidence requiring review

None.

## Structure signals

### Used implicit bodies over 500 lines

| Skill | Sessions | Owner | Body lines | Body words | Body chars | UI fields |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| anycap-cli | 50 | user | 690 | 4438 | 31257 | 3/3 |
| web-design-guidelines | 26 | shared | 1446 | 5253 | 38544 | 3/3 |
| browse | 19 | shared | 745 | 4760 | 33454 | 3/3 |
| investigate | 6 | shared | 741 | 5455 | 38129 | 3/3 |
| open-gstack-browser | 3 | shared | 754 | 5473 | 37513 | 3/3 |
| land-and-deploy | 2 | shared | 1570 | 11512 | 77779 | 3/3 |
| wrangler | 2 | shared | 913 | 2385 | 17775 | 3/3 |
| review | 1 | shared | 1447 | 10684 | 75131 | 0/3 |

### Implicit skills with at least 2 retained sessions missing complete UI metadata

None.

## Complete inventory

| Skill | Sessions | Primary | Explicit | Reads | Policy | Owner | Description | Signal |
| --- | ---: | ---: | ---: | ---: | --- | --- | ---: | --- |
| anycap-cli | 50 | 50 | 0 | 50 | implicit | user | 138 | keep |
| frontend-design | 43 | 43 | 0 | 43 | implicit | shared | 134 | keep |
| playwright | 35 | 35 | 0 | 35 | implicit | user | 135 | keep |
| web-design-guidelines | 26 | 26 | 0 | 26 | implicit | shared | 138 | keep |
| imagegen | 25 | 25 | 0 | 25 | implicit | system | 570 | system-managed-description |
| browse | 19 | 19 | 0 | 19 | implicit | shared | 133 | keep |
| project-workspace-triage | 16 | 16 | 0 | 16 | implicit | user | 133 | keep |
| careful | 13 | 13 | 0 | 13 | implicit | shared | 134 | keep |
| cli-tooling-inventory | 13 | 13 | 0 | 13 | implicit | user | 343 | shorten-used-description |
| goal-prompt | 10 | 10 | 9 | 3 | implicit | shared | 135 | keep |
| workspace-noise-cleanup | 10 | 10 | 0 | 10 | implicit | user | 130 | keep |
| implementation-workflow | 9 | 9 | 0 | 9 | implicit | shared | 129 | keep |
| skill-creator | 8 | 8 | 0 | 8 | implicit | system | 225 | system-managed-description |
| cli-tooling-governance | 7 | 7 | 0 | 7 | implicit | shared | 128 | keep |
| mcp-surface-governance | 7 | 7 | 0 | 7 | implicit | shared | 121 | keep |
| pdf | 7 | 7 | 0 | 7 | implicit | user | 133 | keep |
| investigate | 6 | 6 | 0 | 6 | implicit | shared | 137 | keep |
| kt-aicoding-registry | 6 | 6 | 0 | 6 | implicit | shared | 132 | keep |
| openai-docs | 6 | 6 | 0 | 6 | implicit | system | 447 | system-managed-description |
| configure-custom-domain | 5 | 5 | 0 | 5 | implicit | user | 131 | keep |
| deploy-to-vercel | 5 | 5 | 0 | 5 | implicit | shared | 130 | keep |
| gstack-upgrade | 5 | 5 | 0 | 5 | implicit | shared | 131 | keep |
| skill-image | 5 | 5 | 0 | 5 | implicit | shared | 138 | keep |
| design-review | 4 | 4 | 0 | 4 | implicit | shared | 140 | keep |
| kevinten10-supabase | 4 | 4 | 0 | 4 | implicit | user | 138 | keep |
| session-workflow-retrospective | 4 | 4 | 0 | 4 | implicit | shared | 133 | keep |
| vercel-react-best-practices | 4 | 4 | 0 | 4 | implicit | shared | 134 | keep |
| agent-productization | 3 | 3 | 0 | 3 | implicit | user | 132 | keep |
| codex-mcp-profiles | 3 | 3 | 0 | 3 | implicit | user | 125 | keep |
| mcp-server-release | 3 | 3 | 0 | 3 | implicit | user | 129 | keep |
| media-production-pipeline | 3 | 3 | 0 | 3 | implicit | user | 134 | keep |
| open-gstack-browser | 3 | 3 | 0 | 3 | implicit | shared | 135 | keep |
| repo-readme-release | 3 | 3 | 0 | 3 | implicit | user | 131 | keep |
| security-best-practices | 3 | 3 | 0 | 3 | implicit | user | 128 | keep |
| wechat-local-history | 3 | 3 | 0 | 3 | explicit-only | user | 200 | keep |
| brief-to-tasks | 2 | 2 | 0 | 2 | implicit | shared | 138 | keep |
| find-bugs | 2 | 2 | 0 | 2 | implicit | shared | 140 | keep |
| gh-fix-ci | 2 | 2 | 0 | 2 | implicit | user | 125 | keep |
| jd-shopping | 2 | 2 | 0 | 2 | explicit-only | shared | 140 | keep |
| land-and-deploy | 2 | 2 | 0 | 2 | implicit | shared | 136 | keep |
| modern-python | 2 | 2 | 0 | 2 | implicit | shared | 135 | keep |
| screenshot | 2 | 2 | 0 | 2 | implicit | user | 128 | keep |
| setup-browser-cookies | 2 | 2 | 0 | 2 | explicit-only | shared | 300 | keep |
| skill-installer | 2 | 2 | 0 | 2 | implicit | system | 225 | system-managed-description |
| source-backed-research | 2 | 2 | 0 | 2 | implicit | shared | 137 | keep |
| volcengine-ark-migration | 2 | 2 | 0 | 2 | explicit-only | user | 359 | keep |
| wrangler | 2 | 2 | 0 | 2 | implicit | shared | 132 | keep |
| audit-context-building | 1 | 1 | 0 | 1 | explicit-only | shared | 123 | keep |
| checkpoint | 1 | 1 | 0 | 1 | explicit-only | shared | 444 | keep |
| cli-creator | 1 | 1 | 0 | 1 | implicit | user | 129 | keep |
| document-release | 1 | 1 | 0 | 1 | explicit-only | shared | 379 | keep |
| fixing-metadata | 1 | 1 | 0 | 1 | implicit | shared | 127 | keep |
| gstack | 1 | 1 | 0 | 1 | explicit-only | shared | 356 | keep |
| gstack-openclaw-ceo-review | 1 | 1 | 0 | 1 | explicit-only | shared | 403 | keep |
| gstack-openclaw-investigate | 1 | 1 | 0 | 1 | explicit-only | shared | 343 | keep |
| gstack-openclaw-office-hours | 1 | 1 | 0 | 1 | explicit-only | shared | 446 | keep |
| impeccable | 1 | 1 | 0 | 1 | implicit | shared | 137 | keep |
| migrate-to-codex | 1 | 1 | 0 | 1 | implicit | user | 104 | keep |
| plugin-creator | 1 | 1 | 0 | 1 | implicit | system | 471 | system-managed-description |
| print-hp-m1005-usb | 1 | 1 | 0 | 1 | explicit-only | user | 481 | keep |
| retro | 1 | 1 | 0 | 1 | explicit-only | shared | 373 | keep |
| review | 1 | 1 | 0 | 1 | implicit | shared | 136 | keep |
| speech | 1 | 1 | 0 | 1 | explicit-only | user | 309 | keep |
| submit-12315-complaint | 1 | 1 | 0 | 1 | explicit-only | user | 305 | keep |
| taobao-shopping | 1 | 1 | 0 | 1 | explicit-only | shared | 135 | keep |
| transcribe | 1 | 1 | 0 | 1 | explicit-only | user | 216 | keep |
| unfreeze | 1 | 1 | 0 | 1 | explicit-only | shared | 242 | keep |
| vercel-composition-patterns | 1 | 1 | 0 | 1 | implicit | shared | 132 | keep |
| visionos-design-guidelines | 1 | 1 | 0 | 1 | explicit-only | shared | 241 | keep |
| agents-sdk | 0 | 0 | 0 | 0 | explicit-only | shared | 358 | keep |
| android-design-guidelines | 0 | 0 | 0 | 0 | explicit-only | shared | 281 | keep |
| autoplan | 0 | 0 | 0 | 0 | explicit-only | shared | 662 | keep |
| baseline-ui | 0 | 0 | 0 | 0 | explicit-only | shared | 261 | keep |
| benchmark | 0 | 0 | 0 | 0 | explicit-only | shared | 402 | keep |
| canary | 0 | 0 | 0 | 0 | explicit-only | shared | 336 | keep |
| canvas-design | 0 | 0 | 0 | 0 | explicit-only | shared | 289 | keep |
| chatgpt-apps | 0 | 0 | 0 | 0 | implicit | user | 133 | keep-implicit-capability |
| codex | 0 | 0 | 0 | 0 | explicit-only | shared | 487 | keep |
| color-expert | 0 | 0 | 0 | 0 | explicit-only | shared | 455 | keep |
| cso | 0 | 0 | 0 | 0 | explicit-only | shared | 615 | keep |
| define-goal | 0 | 0 | 0 | 0 | explicit-only | user | 380 | keep |
| design-brief | 0 | 0 | 0 | 0 | explicit-only | shared | 268 | keep |
| design-consultation | 0 | 0 | 0 | 0 | explicit-only | shared | 521 | keep |
| design-flow | 0 | 0 | 0 | 0 | explicit-only | shared | 290 | keep |
| design-html | 0 | 0 | 0 | 0 | explicit-only | shared | 720 | keep |
| design-shotgun | 0 | 0 | 0 | 0 | explicit-only | shared | 400 | keep |
| design-taste-frontend | 0 | 0 | 0 | 0 | explicit-only | shared | 202 | keep |
| design-tokens | 0 | 0 | 0 | 0 | explicit-only | shared | 316 | keep |
| devex-review | 0 | 0 | 0 | 0 | explicit-only | shared | 667 | keep |
| durable-objects | 0 | 0 | 0 | 0 | explicit-only | shared | 382 | keep |
| extract-design-system | 0 | 0 | 0 | 0 | explicit-only | shared | 98 | keep |
| figma-implement-design | 0 | 0 | 0 | 0 | implicit | shared | 137 | keep-implicit-capability |
| firecrawl-build-scrape | 0 | 0 | 0 | 0 | explicit-only | shared | 270 | keep |
| firecrawl-build-search | 0 | 0 | 0 | 0 | explicit-only | shared | 254 | keep |
| fixing-accessibility | 0 | 0 | 0 | 0 | implicit | shared | 140 | keep-implicit-capability |
| fixing-motion-performance | 0 | 0 | 0 | 0 | explicit-only | shared | 223 | keep |
| freeze | 0 | 0 | 0 | 0 | explicit-only | shared | 327 | keep |
| frontend-design-principles | 0 | 0 | 0 | 0 | explicit-only | shared | 215 | keep |
| full-output-enforcement | 0 | 0 | 0 | 0 | explicit-only | shared | 203 | keep |
| gh-address-comments | 0 | 0 | 0 | 0 | explicit-only | user | 168 | keep |
| grill-me | 0 | 0 | 0 | 0 | explicit-only | shared | 254 | keep |
| gstack-openclaw-retro | 0 | 0 | 0 | 0 | explicit-only | shared | 297 | keep |
| guard | 0 | 0 | 0 | 0 | explicit-only | shared | 363 | keep |
| health | 0 | 0 | 0 | 0 | explicit-only | shared | 311 | keep |
| high-end-visual-design | 0 | 0 | 0 | 0 | explicit-only | shared | 234 | keep |
| industrial-brutalist-ui | 0 | 0 | 0 | 0 | explicit-only | shared | 286 | keep |
| information-architecture | 0 | 0 | 0 | 0 | explicit-only | shared | 306 | keep |
| ios-design-guidelines | 0 | 0 | 0 | 0 | explicit-only | shared | 237 | keep |
| ipados-design-guidelines | 0 | 0 | 0 | 0 | explicit-only | shared | 276 | keep |
| jupyter-notebook | 0 | 0 | 0 | 0 | explicit-only | user | 237 | keep |
| layout | 0 | 0 | 0 | 0 | explicit-only | shared | 260 | keep |
| learn | 0 | 0 | 0 | 0 | explicit-only | shared | 307 | keep |
| macos-design-guidelines | 0 | 0 | 0 | 0 | explicit-only | shared | 237 | keep |
| minimalist-ui | 0 | 0 | 0 | 0 | explicit-only | shared | 145 | keep |
| office-hours | 0 | 0 | 0 | 0 | explicit-only | shared | 756 | keep |
| optimize | 0 | 0 | 0 | 0 | explicit-only | shared | 228 | keep |
| overdrive | 0 | 0 | 0 | 0 | explicit-only | shared | 250 | keep |
| pair-agent | 0 | 0 | 0 | 0 | explicit-only | shared | 592 | keep |
| plan-ceo-review | 0 | 0 | 0 | 0 | explicit-only | shared | 570 | keep |
| plan-design-review | 0 | 0 | 0 | 0 | explicit-only | shared | 425 | keep |
| plan-devex-review | 0 | 0 | 0 | 0 | explicit-only | shared | 690 | keep |
| plan-eng-review | 0 | 0 | 0 | 0 | explicit-only | shared | 546 | keep |
| playwright-interactive | 0 | 0 | 0 | 0 | explicit-only | user | 94 | keep |
| polish | 0 | 0 | 0 | 0 | explicit-only | shared | 239 | keep |
| qa | 0 | 0 | 0 | 0 | explicit-only | shared | 665 | keep |
| qa-only | 0 | 0 | 0 | 0 | explicit-only | shared | 470 | keep |
| quieter | 0 | 0 | 0 | 0 | explicit-only | shared | 227 | keep |
| redesign-existing-projects | 0 | 0 | 0 | 0 | explicit-only | shared | 225 | keep |
| replicate | 0 | 0 | 0 | 0 | explicit-only | shared | 58 | keep |
| security-ownership-map | 0 | 0 | 0 | 0 | explicit-only | user | 532 | keep |
| security-review | 0 | 0 | 0 | 0 | explicit-only | shared | 312 | keep |
| security-threat-model | 0 | 0 | 0 | 0 | explicit-only | user | 412 | keep |
| setup-deploy | 0 | 0 | 0 | 0 | explicit-only | shared | 418 | keep |
| shape | 0 | 0 | 0 | 0 | explicit-only | shared | 264 | keep |
| sharp-edges | 0 | 0 | 0 | 0 | explicit-only | shared | 376 | keep |
| sleek-design-mobile-apps | 0 | 0 | 0 | 0 | explicit-only | shared | 259 | keep |
| sred-work-summary | 0 | 0 | 0 | 0 | explicit-only | shared | 152 | keep |
| stitch-design-taste | 0 | 0 | 0 | 0 | explicit-only | shared | 257 | keep |
| tailwind-css-patterns | 0 | 0 | 0 | 0 | explicit-only | shared | 320 | keep |
| tailwind-design-system | 0 | 0 | 0 | 0 | explicit-only | shared | 210 | keep |
| theme-factory | 0 | 0 | 0 | 0 | explicit-only | shared | 262 | keep |
| transformers-js | 0 | 0 | 0 | 0 | explicit-only | shared | 425 | keep |
| tvos-design-guidelines | 0 | 0 | 0 | 0 | explicit-only | shared | 233 | keep |
| typeset | 0 | 0 | 0 | 0 | explicit-only | shared | 248 | keep |
| ui-animation | 0 | 0 | 0 | 0 | explicit-only | shared | 413 | keep |
| vercel-cli-with-tokens | 0 | 0 | 0 | 0 | explicit-only | shared | 236 | keep |
| vercel-react-view-transitions | 0 | 0 | 0 | 0 | explicit-only | shared | 664 | keep |
| watchos-design-guidelines | 0 | 0 | 0 | 0 | explicit-only | shared | 222 | keep |
