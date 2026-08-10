# Evidence Model

Use this reference when research requires more than a few straightforward citations.

## Source Levels

| Level | Examples | Appropriate use |
| --- | --- | --- |
| A - authoritative primary | Law or regulator text, official policy/docs, standards, first-party dataset, original paper | Establish the source's own rule, data, interface, or findings |
| B - independent primary | Separate dataset, filing, court record, reproducible test, another original study | Corroborate consequential or disputed claims |
| C - high-quality secondary | Systematic review, respected technical analysis, institutional explainer | Interpret or synthesize primary material |
| D - discovery only | Search snippets, aggregators, forums, social posts, unsourced summaries | Find leads; do not use alone for a material conclusion |

Authority is claim-specific. A vendor is authoritative about its documented API but not automatically about comparative superiority. A user report can prove that someone reported an experience, not that the experience is typical.

## Claim Status

- `verified`: directly supported by an appropriate source and current for the stated scope.
- `corroborated`: supported by more than one independent appropriate source.
- `source-reported`: accurately reflects what one source states but is not independently verified.
- `inferred`: reasoned from evidence; the reasoning and uncertainty must be explicit.
- `conflicted`: credible sources disagree or use incompatible scope/definitions.
- `unknown`: evidence is missing, inaccessible, outdated, or insufficient.

## Compact Claim Ledger

```markdown
| Claim | Status | Source and date | Scope | Conflict or limitation | Confidence |
| --- | --- | --- | --- | --- | --- |
| <one material claim> | verified | <direct link, effective date> | <where it applies> | <limits> | high |
```

Keep claims atomic. If one sentence needs two different sources, split it into two ledger rows or cite both at the exact point they apply.

## Conflict Resolution

Check these before deciding that two sources truly disagree:

1. publication, update, and effective dates;
2. jurisdiction, product version, population, or environment;
3. definitions, denominators, and measurement periods;
4. primary data versus interpretation;
5. provisional, superseded, withdrawn, or archived status;
6. incentives and whether the source is describing its own policy.

When conflict remains, present both positions, explain the decision impact, and identify the smallest next check that could resolve it.

## Research Note Shape

```markdown
# <Question>

- As of: <date and timezone>
- Scope: <jurisdiction/product/population>
- Decision: <what this research supports>

## Current Answer
<concise conclusion with confidence>

## Evidence
<claim ledger>

## Conflicts And Unknowns
<material disagreement, missing evidence, limitations>

## Next Verification
<concrete action, owner, or trigger>

## Resume Entry
<authoritative files/sources and first next step>
```
