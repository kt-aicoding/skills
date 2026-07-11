# Repository Guidelines

- GitHub: `kt-aicoding/skills`
- Category: Codex skill collection.

## Editing Rules

- Keep reusable Codex skills under `skills/<skill-name>/`.
- Keep each skill folder name identical to the `name` in its `SKILL.md`.
- Keep `SKILL.md` concise; route detailed matrices and examples to one-level `references/` files.
- Keep each `description` at or below 140 characters and front-load its unique trigger terms; verify the full text remains visible with `codex debug prompt-input`.
- Keep `agents/openai.yaml` aligned with the skill name, scope, and default prompt.
- Do not duplicate a skill that already has a canonical standalone repository. Link to that repository instead.
- Never add secrets, cookies, tokens, private paths, or copied environment values.

## Validation

```bash
validator="${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py"
for skill in skills/*; do
  python3 "$validator" "$skill"
done
python3 scripts/audit-codex-skills.py --root skills --strict
git diff --check
```
