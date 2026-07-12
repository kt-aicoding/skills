# Codex Skill Usage Audit

Evidence window: `2026-02-17T11:16:10.544Z` to `2026-07-12T04:54:43.324Z`. Retained sessions: **67** (56 primary, 11 subagent).

This report stores aggregate session counts only. It does not include prompts, tool output, working directories, or session identifiers. A session counts as usage when the user explicitly mentions `$skill` or Codex reads that skill's `SKILL.md`. `no-evidence` means no match in retained logs, not that the skill was never used.

## Summary

- Installed and enabled skills: 144
- Frequent threshold: 5 sessions
- frequent: 6
- no-evidence: 90
- rare: 29
- used: 19

## Frequent skills

| Skill | Sessions | Primary | Explicit | Reads | Policy | Description | Signal |
| --- | ---: | ---: | ---: | ---: | --- | ---: | --- |
| project-workspace-triage | 13 | 13 | 0 | 13 | implicit | 421 | shorten-frequent-description |
| goal-prompt | 10 | 10 | 9 | 3 | implicit | 135 | keep |
| workspace-noise-cleanup | 9 | 9 | 0 | 9 | implicit | 322 | shorten-frequent-description |
| cli-tooling-governance | 5 | 5 | 0 | 5 | implicit | 128 | keep |
| mcp-surface-governance | 5 | 5 | 0 | 5 | implicit | 121 | keep |
| playwright | 5 | 5 | 0 | 5 | implicit | 209 | shorten-frequent-description |

## Review signals

### Frequent descriptions over 140 chars

| Skill | Sessions | Primary | Explicit | Reads | Policy | Description | Signal |
| --- | ---: | ---: | ---: | ---: | --- | ---: | --- |
| project-workspace-triage | 13 | 13 | 0 | 13 | implicit | 421 | shorten-frequent-description |
| workspace-noise-cleanup | 9 | 9 | 0 | 9 | implicit | 322 | shorten-frequent-description |
| playwright | 5 | 5 | 0 | 5 | implicit | 209 | shorten-frequent-description |

### Frequently used explicit-only skills

No explicit-only skill crossed the frequent threshold.

### Implicit skills with no retained evidence

| Skill | Sessions | Primary | Explicit | Reads | Policy | Description | Signal |
| --- | ---: | ---: | ---: | ---: | --- | ---: | --- |
| baseline-ui | 0 | 0 | 0 | 0 | implicit | 261 | review-unused-implicit |
| chatgpt-apps | 0 | 0 | 0 | 0 | implicit | 449 | review-unused-implicit |
| define-goal | 0 | 0 | 0 | 0 | implicit | 380 | review-unused-implicit |
| design-brief | 0 | 0 | 0 | 0 | implicit | 268 | review-unused-implicit |
| design-flow | 0 | 0 | 0 | 0 | implicit | 290 | review-unused-implicit |
| design-tokens | 0 | 0 | 0 | 0 | implicit | 316 | review-unused-implicit |
| figma-implement-design | 0 | 0 | 0 | 0 | implicit | 345 | review-unused-implicit |
| fixing-accessibility | 0 | 0 | 0 | 0 | implicit | 218 | review-unused-implicit |
| fixing-metadata | 0 | 0 | 0 | 0 | implicit | 340 | review-unused-implicit |
| fixing-motion-performance | 0 | 0 | 0 | 0 | implicit | 223 | review-unused-implicit |
| frontend-design-principles | 0 | 0 | 0 | 0 | implicit | 215 | review-unused-implicit |
| gh-address-comments | 0 | 0 | 0 | 0 | implicit | 168 | review-unused-implicit |
| grill-me | 0 | 0 | 0 | 0 | implicit | 254 | review-unused-implicit |
| gstack | 0 | 0 | 0 | 0 | implicit | 356 | review-unused-implicit |
| health | 0 | 0 | 0 | 0 | implicit | 311 | review-unused-implicit |
| imagegen | 0 | 0 | 0 | 0 | implicit | 570 | review-unused-implicit |
| information-architecture | 0 | 0 | 0 | 0 | implicit | 306 | review-unused-implicit |
| layout | 0 | 0 | 0 | 0 | implicit | 260 | review-unused-implicit |
| optimize | 0 | 0 | 0 | 0 | implicit | 228 | review-unused-implicit |
| playwright-interactive | 0 | 0 | 0 | 0 | implicit | 94 | review-unused-implicit |
| polish | 0 | 0 | 0 | 0 | implicit | 239 | review-unused-implicit |
| redesign-existing-projects | 0 | 0 | 0 | 0 | implicit | 225 | review-unused-implicit |
| screenshot | 0 | 0 | 0 | 0 | implicit | 220 | review-unused-implicit |
| security-ownership-map | 0 | 0 | 0 | 0 | implicit | 532 | review-unused-implicit |
| security-review | 0 | 0 | 0 | 0 | implicit | 312 | review-unused-implicit |
| security-threat-model | 0 | 0 | 0 | 0 | implicit | 412 | review-unused-implicit |
| setup-browser-cookies | 0 | 0 | 0 | 0 | implicit | 300 | review-unused-implicit |
| shape | 0 | 0 | 0 | 0 | implicit | 264 | review-unused-implicit |
| sharp-edges | 0 | 0 | 0 | 0 | implicit | 376 | review-unused-implicit |
| tailwind-css-patterns | 0 | 0 | 0 | 0 | implicit | 320 | review-unused-implicit |
| tailwind-design-system | 0 | 0 | 0 | 0 | implicit | 210 | review-unused-implicit |
| ui-animation | 0 | 0 | 0 | 0 | implicit | 413 | review-unused-implicit |
| vercel-cli-with-tokens | 0 | 0 | 0 | 0 | implicit | 236 | review-unused-implicit |
| web-design-guidelines | 0 | 0 | 0 | 0 | implicit | 277 | review-unused-implicit |

## Complete inventory

| Skill | Sessions | Primary | Explicit | Reads | Policy | Description | Signal |
| --- | ---: | ---: | ---: | ---: | --- | ---: | --- |
| project-workspace-triage | 13 | 13 | 0 | 13 | implicit | 421 | shorten-frequent-description |
| goal-prompt | 10 | 10 | 9 | 3 | implicit | 135 | keep |
| workspace-noise-cleanup | 9 | 9 | 0 | 9 | implicit | 322 | shorten-frequent-description |
| cli-tooling-governance | 5 | 5 | 0 | 5 | implicit | 128 | keep |
| mcp-surface-governance | 5 | 5 | 0 | 5 | implicit | 121 | keep |
| playwright | 5 | 5 | 0 | 5 | implicit | 209 | shorten-frequent-description |
| anycap-cli | 4 | 4 | 0 | 4 | implicit | 789 | keep |
| cli-tooling-inventory | 4 | 4 | 0 | 4 | implicit | 448 | keep |
| kt-aicoding-registry | 4 | 4 | 0 | 4 | implicit | 132 | keep |
| configure-custom-domain | 3 | 3 | 0 | 3 | implicit | 353 | keep |
| gstack-upgrade | 3 | 3 | 0 | 3 | implicit | 313 | keep |
| investigate | 3 | 3 | 0 | 3 | implicit | 492 | keep |
| mcp-server-release | 3 | 3 | 0 | 3 | implicit | 350 | keep |
| skill-creator | 3 | 3 | 0 | 3 | implicit | 225 | keep |
| skill-image | 3 | 3 | 0 | 3 | implicit | 138 | keep |
| browse | 2 | 2 | 0 | 2 | implicit | 497 | keep |
| careful | 2 | 2 | 0 | 2 | implicit | 362 | keep |
| gh-fix-ci | 2 | 2 | 0 | 2 | implicit | 313 | keep |
| jd-shopping | 2 | 2 | 0 | 2 | explicit-only | 140 | keep |
| kevinten10-supabase | 2 | 2 | 0 | 2 | implicit | 243 | keep |
| media-production-pipeline | 2 | 2 | 0 | 2 | implicit | 332 | keep |
| openai-docs | 2 | 2 | 0 | 2 | implicit | 447 | keep |
| repo-readme-release | 2 | 2 | 0 | 2 | implicit | 312 | keep |
| vercel-react-best-practices | 2 | 2 | 0 | 2 | implicit | 329 | keep |
| volcengine-ark-migration | 2 | 2 | 0 | 2 | explicit-only | 359 | keep |
| agent-productization | 1 | 1 | 0 | 1 | implicit | 363 | keep |
| brief-to-tasks | 1 | 1 | 0 | 1 | implicit | 263 | keep |
| cli-creator | 1 | 1 | 0 | 1 | implicit | 334 | keep |
| codex-mcp-profiles | 1 | 1 | 0 | 1 | implicit | 125 | keep |
| deploy-to-vercel | 1 | 1 | 0 | 1 | implicit | 194 | keep |
| design-review | 1 | 1 | 0 | 1 | implicit | 263 | keep |
| document-release | 1 | 1 | 0 | 1 | explicit-only | 379 | keep |
| find-bugs | 1 | 1 | 0 | 1 | implicit | 184 | keep |
| frontend-design | 1 | 1 | 0 | 1 | implicit | 297 | keep |
| gstack-openclaw-ceo-review | 1 | 1 | 0 | 1 | explicit-only | 403 | keep |
| gstack-openclaw-investigate | 1 | 1 | 0 | 1 | explicit-only | 343 | keep |
| gstack-openclaw-office-hours | 1 | 1 | 0 | 1 | explicit-only | 446 | keep |
| impeccable | 1 | 1 | 0 | 1 | implicit | 444 | keep |
| implementation-workflow | 1 | 1 | 0 | 1 | implicit | 129 | keep |
| land-and-deploy | 1 | 1 | 0 | 1 | implicit | 252 | keep |
| migrate-to-codex | 1 | 1 | 0 | 1 | implicit | 104 | keep |
| modern-python | 1 | 1 | 0 | 1 | implicit | 159 | keep |
| open-gstack-browser | 1 | 1 | 0 | 1 | implicit | 465 | keep |
| pdf | 1 | 1 | 0 | 1 | implicit | 248 | keep |
| plugin-creator | 1 | 1 | 0 | 1 | implicit | 471 | keep |
| review | 1 | 1 | 0 | 1 | implicit | 338 | keep |
| security-best-practices | 1 | 1 | 0 | 1 | implicit | 385 | keep |
| skill-installer | 1 | 1 | 0 | 1 | implicit | 225 | keep |
| taobao-shopping | 1 | 1 | 0 | 1 | explicit-only | 135 | keep |
| unfreeze | 1 | 1 | 0 | 1 | explicit-only | 242 | keep |
| vercel-composition-patterns | 1 | 1 | 0 | 1 | implicit | 310 | keep |
| visionos-design-guidelines | 1 | 1 | 0 | 1 | explicit-only | 241 | keep |
| wechat-local-history | 1 | 1 | 0 | 1 | explicit-only | 269 | keep |
| wrangler | 1 | 1 | 0 | 1 | implicit | 336 | keep |
| agents-sdk | 0 | 0 | 0 | 0 | explicit-only | 358 | keep |
| android-design-guidelines | 0 | 0 | 0 | 0 | explicit-only | 281 | keep |
| audit-context-building | 0 | 0 | 0 | 0 | explicit-only | 123 | keep |
| autoplan | 0 | 0 | 0 | 0 | explicit-only | 662 | keep |
| baseline-ui | 0 | 0 | 0 | 0 | implicit | 261 | review-unused-implicit |
| benchmark | 0 | 0 | 0 | 0 | explicit-only | 402 | keep |
| canary | 0 | 0 | 0 | 0 | explicit-only | 336 | keep |
| canvas-design | 0 | 0 | 0 | 0 | explicit-only | 289 | keep |
| chatgpt-apps | 0 | 0 | 0 | 0 | implicit | 449 | review-unused-implicit |
| checkpoint | 0 | 0 | 0 | 0 | explicit-only | 444 | keep |
| codex | 0 | 0 | 0 | 0 | explicit-only | 487 | keep |
| color-expert | 0 | 0 | 0 | 0 | explicit-only | 455 | keep |
| cso | 0 | 0 | 0 | 0 | explicit-only | 615 | keep |
| define-goal | 0 | 0 | 0 | 0 | implicit | 380 | review-unused-implicit |
| design-brief | 0 | 0 | 0 | 0 | implicit | 268 | review-unused-implicit |
| design-consultation | 0 | 0 | 0 | 0 | explicit-only | 521 | keep |
| design-flow | 0 | 0 | 0 | 0 | implicit | 290 | review-unused-implicit |
| design-html | 0 | 0 | 0 | 0 | explicit-only | 720 | keep |
| design-shotgun | 0 | 0 | 0 | 0 | explicit-only | 400 | keep |
| design-taste-frontend | 0 | 0 | 0 | 0 | explicit-only | 202 | keep |
| design-tokens | 0 | 0 | 0 | 0 | implicit | 316 | review-unused-implicit |
| devex-review | 0 | 0 | 0 | 0 | explicit-only | 667 | keep |
| durable-objects | 0 | 0 | 0 | 0 | explicit-only | 382 | keep |
| extract-design-system | 0 | 0 | 0 | 0 | explicit-only | 98 | keep |
| figma-implement-design | 0 | 0 | 0 | 0 | implicit | 345 | review-unused-implicit |
| firecrawl-build-scrape | 0 | 0 | 0 | 0 | explicit-only | 270 | keep |
| firecrawl-build-search | 0 | 0 | 0 | 0 | explicit-only | 254 | keep |
| fixing-accessibility | 0 | 0 | 0 | 0 | implicit | 218 | review-unused-implicit |
| fixing-metadata | 0 | 0 | 0 | 0 | implicit | 340 | review-unused-implicit |
| fixing-motion-performance | 0 | 0 | 0 | 0 | implicit | 223 | review-unused-implicit |
| freeze | 0 | 0 | 0 | 0 | explicit-only | 327 | keep |
| frontend-design-principles | 0 | 0 | 0 | 0 | implicit | 215 | review-unused-implicit |
| full-output-enforcement | 0 | 0 | 0 | 0 | explicit-only | 203 | keep |
| gh-address-comments | 0 | 0 | 0 | 0 | implicit | 168 | review-unused-implicit |
| grill-me | 0 | 0 | 0 | 0 | implicit | 254 | review-unused-implicit |
| gstack | 0 | 0 | 0 | 0 | implicit | 356 | review-unused-implicit |
| gstack-openclaw-retro | 0 | 0 | 0 | 0 | explicit-only | 297 | keep |
| guard | 0 | 0 | 0 | 0 | explicit-only | 363 | keep |
| health | 0 | 0 | 0 | 0 | implicit | 311 | review-unused-implicit |
| high-end-visual-design | 0 | 0 | 0 | 0 | explicit-only | 234 | keep |
| imagegen | 0 | 0 | 0 | 0 | implicit | 570 | review-unused-implicit |
| industrial-brutalist-ui | 0 | 0 | 0 | 0 | explicit-only | 286 | keep |
| information-architecture | 0 | 0 | 0 | 0 | implicit | 306 | review-unused-implicit |
| ios-design-guidelines | 0 | 0 | 0 | 0 | explicit-only | 237 | keep |
| ipados-design-guidelines | 0 | 0 | 0 | 0 | explicit-only | 276 | keep |
| jupyter-notebook | 0 | 0 | 0 | 0 | explicit-only | 237 | keep |
| layout | 0 | 0 | 0 | 0 | implicit | 260 | review-unused-implicit |
| learn | 0 | 0 | 0 | 0 | explicit-only | 307 | keep |
| macos-design-guidelines | 0 | 0 | 0 | 0 | explicit-only | 237 | keep |
| minimalist-ui | 0 | 0 | 0 | 0 | explicit-only | 145 | keep |
| office-hours | 0 | 0 | 0 | 0 | explicit-only | 756 | keep |
| optimize | 0 | 0 | 0 | 0 | implicit | 228 | review-unused-implicit |
| overdrive | 0 | 0 | 0 | 0 | explicit-only | 250 | keep |
| pair-agent | 0 | 0 | 0 | 0 | explicit-only | 592 | keep |
| plan-ceo-review | 0 | 0 | 0 | 0 | explicit-only | 570 | keep |
| plan-design-review | 0 | 0 | 0 | 0 | explicit-only | 425 | keep |
| plan-devex-review | 0 | 0 | 0 | 0 | explicit-only | 690 | keep |
| plan-eng-review | 0 | 0 | 0 | 0 | explicit-only | 546 | keep |
| playwright-interactive | 0 | 0 | 0 | 0 | implicit | 94 | review-unused-implicit |
| polish | 0 | 0 | 0 | 0 | implicit | 239 | review-unused-implicit |
| qa | 0 | 0 | 0 | 0 | explicit-only | 665 | keep |
| qa-only | 0 | 0 | 0 | 0 | explicit-only | 470 | keep |
| quieter | 0 | 0 | 0 | 0 | explicit-only | 227 | keep |
| redesign-existing-projects | 0 | 0 | 0 | 0 | implicit | 225 | review-unused-implicit |
| replicate | 0 | 0 | 0 | 0 | explicit-only | 58 | keep |
| retro | 0 | 0 | 0 | 0 | explicit-only | 373 | keep |
| screenshot | 0 | 0 | 0 | 0 | implicit | 220 | review-unused-implicit |
| security-ownership-map | 0 | 0 | 0 | 0 | implicit | 532 | review-unused-implicit |
| security-review | 0 | 0 | 0 | 0 | implicit | 312 | review-unused-implicit |
| security-threat-model | 0 | 0 | 0 | 0 | implicit | 412 | review-unused-implicit |
| setup-browser-cookies | 0 | 0 | 0 | 0 | implicit | 300 | review-unused-implicit |
| setup-deploy | 0 | 0 | 0 | 0 | explicit-only | 418 | keep |
| shape | 0 | 0 | 0 | 0 | implicit | 264 | review-unused-implicit |
| sharp-edges | 0 | 0 | 0 | 0 | implicit | 376 | review-unused-implicit |
| sleek-design-mobile-apps | 0 | 0 | 0 | 0 | explicit-only | 259 | keep |
| speech | 0 | 0 | 0 | 0 | explicit-only | 309 | keep |
| sred-work-summary | 0 | 0 | 0 | 0 | explicit-only | 152 | keep |
| stitch-design-taste | 0 | 0 | 0 | 0 | explicit-only | 257 | keep |
| tailwind-css-patterns | 0 | 0 | 0 | 0 | implicit | 320 | review-unused-implicit |
| tailwind-design-system | 0 | 0 | 0 | 0 | implicit | 210 | review-unused-implicit |
| theme-factory | 0 | 0 | 0 | 0 | explicit-only | 262 | keep |
| transcribe | 0 | 0 | 0 | 0 | explicit-only | 216 | keep |
| transformers-js | 0 | 0 | 0 | 0 | explicit-only | 425 | keep |
| tvos-design-guidelines | 0 | 0 | 0 | 0 | explicit-only | 233 | keep |
| typeset | 0 | 0 | 0 | 0 | explicit-only | 248 | keep |
| ui-animation | 0 | 0 | 0 | 0 | implicit | 413 | review-unused-implicit |
| vercel-cli-with-tokens | 0 | 0 | 0 | 0 | implicit | 236 | review-unused-implicit |
| vercel-react-view-transitions | 0 | 0 | 0 | 0 | explicit-only | 664 | keep |
| watchos-design-guidelines | 0 | 0 | 0 | 0 | explicit-only | 222 | keep |
| web-design-guidelines | 0 | 0 | 0 | 0 | implicit | 277 | review-unused-implicit |
