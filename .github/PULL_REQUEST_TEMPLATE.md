## What this changes

One or two sentences. If it adds a skill, say which decision the skill settles.

## Checks

Run these before opening the PR — CI runs the same two, so a failure here is a failure there:

```bash
python tools/lint_skills.py .
python tools/render_skill_readmes.py . --check
```

- [ ] `lint_skills.py` passes (v2 frontmatter, and the body opening on `Prerequisites` and closing
      on `Inputs` / `Outputs` — see [`docs/skill-format.md`](../docs/skill-format.md))
- [ ] `render_skill_readmes.py . --check` passes; the per-skill READMEs are generated, never edited
      by hand
- [ ] `title_fr` and `description_fr` are real French, not the English text copied across
- [ ] The root `README.md` and `README.fr.md` domain counts are updated if a skill was added
- [ ] No API keys, tokens, or credentials anywhere in the examples

## Verified how

Say what you actually ran. "Looks right" is not a verification; a snippet nobody executed is the
main way wrong advice gets in.
