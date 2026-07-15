# Codex Skill Usage Audit

Evidence window: `2026-02-17T11:16:10.544Z` to `2026-07-13T01:36:00.838Z`. Retained sessions: **69** (58 primary, 11 subagent).

This report stores aggregate session counts only. It does not include prompts, tool output, working directories, or session identifiers. A session counts as usage when the user explicitly mentions `$skill` or Codex reads that skill's `SKILL.md`. `no-evidence` means no match in retained logs, not that the skill was never used.

## Summary

- Installed and enabled skills: 144
- Implicit skills: 51
- Explicit-only skills: 93
- Implicit description characters: 8027
- Frequent threshold: 5 sessions
- Intentional implicit keep list: 6
- frequent: 10
- no-evidence: 87
- rare: 28
- used: 19

## Frequent skills

| Skill | Sessions | Primary | Explicit | Reads | Policy | Owner | Description | Signal |
| --- | ---: | ---: | ---: | ---: | --- | --- | ---: | --- |
| project-workspace-triage | 13 | 13 | 0 | 13 | implicit | user | 133 | keep |
| goal-prompt | 10 | 10 | 9 | 3 | implicit | shared | 135 | keep |
| workspace-noise-cleanup | 10 | 10 | 0 | 10 | implicit | user | 130 | keep |
| playwright | 7 | 7 | 0 | 7 | implicit | user | 135 | keep |
| anycap-cli | 6 | 6 | 0 | 6 | implicit | user | 138 | keep |
| cli-tooling-governance | 6 | 6 | 0 | 6 | implicit | shared | 128 | keep |
| cli-tooling-inventory | 6 | 6 | 0 | 6 | implicit | user | 134 | keep |
| mcp-surface-governance | 6 | 6 | 0 | 6 | implicit | shared | 121 | keep |
| careful | 5 | 5 | 0 | 5 | implicit | shared | 134 | keep |
| kt-aicoding-registry | 5 | 5 | 0 | 5 | implicit | shared | 132 | keep |

## Review signals

### Implicit descriptions over 140 chars with at least 1 retained sessions

No non-system implicit description at or above the review threshold exceeds 140 characters.

### Frequently used explicit-only skills

No explicit-only skill crossed the frequent threshold.

### System-managed long descriptions

| Skill | Sessions | Primary | Explicit | Reads | Policy | Owner | Description | Signal |
| --- | ---: | ---: | ---: | ---: | --- | --- | ---: | --- |
| skill-creator | 3 | 3 | 0 | 3 | implicit | system | 225 | system-managed-description |
| openai-docs | 2 | 2 | 0 | 2 | implicit | system | 447 | system-managed-description |
| plugin-creator | 1 | 1 | 0 | 1 | implicit | system | 471 | system-managed-description |
| skill-installer | 1 | 1 | 0 | 1 | implicit | system | 225 | system-managed-description |

### Intentional implicit capabilities without retained evidence

| Skill | Sessions | Primary | Explicit | Reads | Policy | Owner | Description | Signal |
| --- | ---: | ---: | ---: | ---: | --- | --- | ---: | --- |
| chatgpt-apps | 0 | 0 | 0 | 0 | implicit | user | 133 | keep-implicit-capability |
| figma-implement-design | 0 | 0 | 0 | 0 | implicit | shared | 137 | keep-implicit-capability |
| fixing-accessibility | 0 | 0 | 0 | 0 | implicit | shared | 140 | keep-implicit-capability |
| imagegen | 0 | 0 | 0 | 0 | implicit | system | 570 | keep-implicit-capability |
| screenshot | 0 | 0 | 0 | 0 | implicit | user | 128 | keep-implicit-capability |

### Implicit skills with no retained evidence requiring review

None.

## Complete inventory

| Skill | Sessions | Primary | Explicit | Reads | Policy | Owner | Description | Signal |
| --- | ---: | ---: | ---: | ---: | --- | --- | ---: | --- |
| project-workspace-triage | 13 | 13 | 0 | 13 | implicit | user | 133 | keep |
| goal-prompt | 10 | 10 | 9 | 3 | implicit | shared | 135 | keep |
| workspace-noise-cleanup | 10 | 10 | 0 | 10 | implicit | user | 130 | keep |
| playwright | 7 | 7 | 0 | 7 | implicit | user | 135 | keep |
| anycap-cli | 6 | 6 | 0 | 6 | implicit | user | 138 | keep |
| cli-tooling-governance | 6 | 6 | 0 | 6 | implicit | shared | 128 | keep |
| cli-tooling-inventory | 6 | 6 | 0 | 6 | implicit | user | 134 | keep |
| mcp-surface-governance | 6 | 6 | 0 | 6 | implicit | shared | 121 | keep |
| careful | 5 | 5 | 0 | 5 | implicit | shared | 134 | keep |
| kt-aicoding-registry | 5 | 5 | 0 | 5 | implicit | shared | 132 | keep |
| browse | 4 | 4 | 0 | 4 | implicit | shared | 133 | keep |
| configure-custom-domain | 4 | 4 | 0 | 4 | implicit | user | 131 | keep |
| investigate | 4 | 4 | 0 | 4 | implicit | shared | 137 | keep |
| gstack-upgrade | 3 | 3 | 0 | 3 | implicit | shared | 131 | keep |
| mcp-server-release | 3 | 3 | 0 | 3 | implicit | user | 129 | keep |
| repo-readme-release | 3 | 3 | 0 | 3 | implicit | user | 131 | keep |
| skill-creator | 3 | 3 | 0 | 3 | implicit | system | 225 | system-managed-description |
| skill-image | 3 | 3 | 0 | 3 | implicit | shared | 138 | keep |
| codex-mcp-profiles | 2 | 2 | 0 | 2 | implicit | user | 125 | keep |
| gh-fix-ci | 2 | 2 | 0 | 2 | implicit | user | 125 | keep |
| implementation-workflow | 2 | 2 | 0 | 2 | implicit | shared | 129 | keep |
| jd-shopping | 2 | 2 | 0 | 2 | explicit-only | shared | 140 | keep |
| kevinten10-supabase | 2 | 2 | 0 | 2 | implicit | user | 138 | keep |
| media-production-pipeline | 2 | 2 | 0 | 2 | implicit | user | 134 | keep |
| open-gstack-browser | 2 | 2 | 0 | 2 | implicit | shared | 135 | keep |
| openai-docs | 2 | 2 | 0 | 2 | implicit | system | 447 | system-managed-description |
| pdf | 2 | 2 | 0 | 2 | implicit | user | 133 | keep |
| vercel-react-best-practices | 2 | 2 | 0 | 2 | implicit | shared | 134 | keep |
| volcengine-ark-migration | 2 | 2 | 0 | 2 | explicit-only | user | 359 | keep |
| agent-productization | 1 | 1 | 0 | 1 | implicit | user | 132 | keep |
| brief-to-tasks | 1 | 1 | 0 | 1 | implicit | shared | 138 | keep |
| cli-creator | 1 | 1 | 0 | 1 | implicit | user | 129 | keep |
| deploy-to-vercel | 1 | 1 | 0 | 1 | implicit | shared | 130 | keep |
| design-review | 1 | 1 | 0 | 1 | implicit | shared | 140 | keep |
| document-release | 1 | 1 | 0 | 1 | explicit-only | shared | 379 | keep |
| find-bugs | 1 | 1 | 0 | 1 | implicit | shared | 140 | keep |
| fixing-metadata | 1 | 1 | 0 | 1 | implicit | shared | 127 | keep |
| frontend-design | 1 | 1 | 0 | 1 | implicit | shared | 134 | keep |
| gstack-openclaw-ceo-review | 1 | 1 | 0 | 1 | explicit-only | shared | 403 | keep |
| gstack-openclaw-investigate | 1 | 1 | 0 | 1 | explicit-only | shared | 343 | keep |
| gstack-openclaw-office-hours | 1 | 1 | 0 | 1 | explicit-only | shared | 446 | keep |
| impeccable | 1 | 1 | 0 | 1 | implicit | shared | 137 | keep |
| land-and-deploy | 1 | 1 | 0 | 1 | implicit | shared | 136 | keep |
| migrate-to-codex | 1 | 1 | 0 | 1 | implicit | user | 104 | keep |
| modern-python | 1 | 1 | 0 | 1 | implicit | shared | 135 | keep |
| plugin-creator | 1 | 1 | 0 | 1 | implicit | system | 471 | system-managed-description |
| review | 1 | 1 | 0 | 1 | implicit | shared | 136 | keep |
| security-best-practices | 1 | 1 | 0 | 1 | implicit | user | 128 | keep |
| setup-browser-cookies | 1 | 1 | 0 | 1 | explicit-only | shared | 300 | keep |
| skill-installer | 1 | 1 | 0 | 1 | implicit | system | 225 | system-managed-description |
| taobao-shopping | 1 | 1 | 0 | 1 | explicit-only | shared | 135 | keep |
| unfreeze | 1 | 1 | 0 | 1 | explicit-only | shared | 242 | keep |
| vercel-composition-patterns | 1 | 1 | 0 | 1 | implicit | shared | 132 | keep |
| visionos-design-guidelines | 1 | 1 | 0 | 1 | explicit-only | shared | 241 | keep |
| web-design-guidelines | 1 | 1 | 0 | 1 | implicit | shared | 138 | keep |
| wechat-local-history | 1 | 1 | 0 | 1 | explicit-only | user | 269 | keep |
| wrangler | 1 | 1 | 0 | 1 | implicit | shared | 132 | keep |
| agents-sdk | 0 | 0 | 0 | 0 | explicit-only | shared | 358 | keep |
| android-design-guidelines | 0 | 0 | 0 | 0 | explicit-only | shared | 281 | keep |
| audit-context-building | 0 | 0 | 0 | 0 | explicit-only | shared | 123 | keep |
| autoplan | 0 | 0 | 0 | 0 | explicit-only | shared | 662 | keep |
| baseline-ui | 0 | 0 | 0 | 0 | explicit-only | shared | 261 | keep |
| benchmark | 0 | 0 | 0 | 0 | explicit-only | shared | 402 | keep |
| canary | 0 | 0 | 0 | 0 | explicit-only | shared | 336 | keep |
| canvas-design | 0 | 0 | 0 | 0 | explicit-only | shared | 289 | keep |
| chatgpt-apps | 0 | 0 | 0 | 0 | implicit | user | 133 | keep-implicit-capability |
| checkpoint | 0 | 0 | 0 | 0 | explicit-only | shared | 444 | keep |
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
| gstack | 0 | 0 | 0 | 0 | explicit-only | shared | 356 | keep |
| gstack-openclaw-retro | 0 | 0 | 0 | 0 | explicit-only | shared | 297 | keep |
| guard | 0 | 0 | 0 | 0 | explicit-only | shared | 363 | keep |
| health | 0 | 0 | 0 | 0 | explicit-only | shared | 311 | keep |
| high-end-visual-design | 0 | 0 | 0 | 0 | explicit-only | shared | 234 | keep |
| imagegen | 0 | 0 | 0 | 0 | implicit | system | 570 | keep-implicit-capability |
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
| retro | 0 | 0 | 0 | 0 | explicit-only | shared | 373 | keep |
| screenshot | 0 | 0 | 0 | 0 | implicit | user | 128 | keep-implicit-capability |
| security-ownership-map | 0 | 0 | 0 | 0 | explicit-only | user | 532 | keep |
| security-review | 0 | 0 | 0 | 0 | explicit-only | shared | 312 | keep |
| security-threat-model | 0 | 0 | 0 | 0 | explicit-only | user | 412 | keep |
| setup-deploy | 0 | 0 | 0 | 0 | explicit-only | shared | 418 | keep |
| shape | 0 | 0 | 0 | 0 | explicit-only | shared | 264 | keep |
| sharp-edges | 0 | 0 | 0 | 0 | explicit-only | shared | 376 | keep |
| sleek-design-mobile-apps | 0 | 0 | 0 | 0 | explicit-only | shared | 259 | keep |
| speech | 0 | 0 | 0 | 0 | explicit-only | user | 309 | keep |
| sred-work-summary | 0 | 0 | 0 | 0 | explicit-only | shared | 152 | keep |
| stitch-design-taste | 0 | 0 | 0 | 0 | explicit-only | shared | 257 | keep |
| tailwind-css-patterns | 0 | 0 | 0 | 0 | explicit-only | shared | 320 | keep |
| tailwind-design-system | 0 | 0 | 0 | 0 | explicit-only | shared | 210 | keep |
| theme-factory | 0 | 0 | 0 | 0 | explicit-only | shared | 262 | keep |
| transcribe | 0 | 0 | 0 | 0 | explicit-only | user | 216 | keep |
| transformers-js | 0 | 0 | 0 | 0 | explicit-only | shared | 425 | keep |
| tvos-design-guidelines | 0 | 0 | 0 | 0 | explicit-only | shared | 233 | keep |
| typeset | 0 | 0 | 0 | 0 | explicit-only | shared | 248 | keep |
| ui-animation | 0 | 0 | 0 | 0 | explicit-only | shared | 413 | keep |
| vercel-cli-with-tokens | 0 | 0 | 0 | 0 | explicit-only | shared | 236 | keep |
| vercel-react-view-transitions | 0 | 0 | 0 | 0 | explicit-only | shared | 664 | keep |
| watchos-design-guidelines | 0 | 0 | 0 | 0 | explicit-only | shared | 222 | keep |
