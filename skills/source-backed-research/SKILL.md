---
name: source-backed-research
description: Research current, high-stakes, or disputed questions with primary sources, claim-level citations, cross-checks, and explicit uncertainty.
---

# Source-Backed Research

Build decision-ready research from current evidence. Use this for factual investigations, comparisons, recommendations, and reports where source quality or freshness matters.

## Boundaries

- Use `openai-docs` for OpenAI product/API questions; it owns the official OpenAI retrieval path.
- Use `investigate` for code failures and root-cause debugging.
- Use a domain-specific Skill when it defines stricter rules, forms, or submission boundaries.
- Do not invoke this workflow for a simple stable fact that can be answered directly without research.

## Workflow

1. Frame the decision or question. Record the relevant date, geography, audience, constraints, and what would change the answer.
2. Inspect user-provided and project-local material first. Treat it as evidence to verify, not as automatically current or authoritative.
3. Browse whenever facts may have changed, accuracy is high-stakes, a named page or document is referenced, or precise citations are required.
4. Search in layers:
   - authoritative primary sources for the claim;
   - independent primary or high-quality secondary sources for material cross-checks;
   - discovery sources only to locate stronger evidence.
5. Build a claim ledger before drafting the conclusion. Use `references/evidence-model.md` for source levels, claim status, and the compact ledger format.
6. Resolve conflicts by checking effective dates, jurisdiction, population, definitions, methodology, and whether a source is reporting its own policy or interpreting another source.
7. Separate established facts, source-reported claims, analysis/inference, and unknowns. Never upgrade an inference into a fact because sources are directionally consistent.
8. Write the answer around the decision:
   - direct conclusion or current best answer;
   - evidence for each material claim with nearby citations;
   - conflicts, limitations, and confidence;
   - concrete next verification or action when uncertainty matters.
9. For long-running work, persist a dated research note under the owning project's conventions. Include the question, as-of date, claim ledger, conclusion, open questions, and resume entry.

## Source Rules

- Prefer laws, regulators, standards bodies, official product documentation, first-party datasets, court or government records, and original research papers.
- A single primary source can establish its own current policy or data. Independent corroboration is still required for disputed interpretations, comparative claims, and consequential recommendations.
- For medical, legal, and financial topics, distinguish general information from individualized professional advice and verify current jurisdiction or clinical guidance.
- Cite the page that supports the claim, not a search result or unrelated home page.
- Note publication, update, or effective dates when freshness affects the conclusion.
- Do not hide missing access, paywalls, contradictory evidence, sample limitations, or unavailable primary material.

## Privacy And Copyright

- Do not send private files, identifiers, health details, legal evidence, credentials, or unpublished business information to external search services unless the user explicitly authorizes that disclosure.
- Search with the minimum necessary abstraction; keep sensitive synthesis local.
- Quote only short necessary excerpts. Prefer paraphrase and claim-level citations over copying source text.

## Completion Gate

Before calling the research complete, confirm:

- every material factual claim has direct support;
- time-sensitive claims have an as-of date;
- consequential conclusions have appropriate cross-checks;
- source conflicts and inference boundaries are visible;
- citations open to the supporting page;
- remaining uncertainty has a concrete verification path or is explicitly accepted.
