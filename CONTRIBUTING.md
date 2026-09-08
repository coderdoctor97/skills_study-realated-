# Contributing

Thanks for your interest in the **study-related skills** collection.

## How skills are added

> Skills are added **manually** — automated skill generation is intentionally disabled
> for this repository (see `agent.md` and `.agent/settings.json`).

To propose or add a skill:

1. Create a folder under `skills/` using `kebab-case` naming
   (e.g. `skills/flashcard-generator/`).
2. Add a `SKILL.md` with YAML frontmatter containing at least `name` and `description`,
   followed by the skill's instructions/body.
3. Keep skill-local assets inside the skill folder; shared brand assets go in `assets/`.
4. Update `agent.md` if you introduce new conventions.

## Repository hygiene

- Do not delete or modify the logo in `assets/Logo/`.
- Do not change the `LICENSE` or its copyright/attribution.
- Follow the formatting rules in `.editorconfig`.

## License

By contributing, you agree your contributions are released under the
[MIT License](./LICENSE). © 2026 Satya.
