# Agent Documentation

This file is the agent-facing guide for working inside the **study-related skills**
repository. Read it before making structural changes.

## What this repository is

A curated collection of **study-related agent skills** (learning, research,
note-taking, academic productivity). The repository is intentionally minimal right
now: brand assets, baseline configuration, and documentation. Skills themselves are
added later, by hand.

## Repository structure

| Path                | Purpose                                                        |
| ------------------- | -------------------------------------------------------------- |
| `assets/Logo/`      | Brand logo (`skill_study-related.png`).                        |
| `skills/`           | Skill packages. **Empty for now** — populated manually later.  |
| `.claude/`          | Claude Code baseline configuration (`settings.json`).          |
| `.agent/`           | Generic agent baseline configuration (`settings.json`).        |
| `agent.md`          | This document.                                                 |
| `README.md`         | Human-facing overview.                                         |
| `CONTRIBUTING.md`   | How to propose/add skills.                                     |
| `LICENSE`           | MIT License (© 2026 Satya).                                    |

## Conventions for adding skills (later, manually)

When a skill is added, follow this shape:

```text
skills/
└── <skill-name>/
    ├── SKILL.md            # required: frontmatter (name, description) + body
    ├── scripts/            # optional: helper scripts
    └── references/         # optional: reference material
```

- One directory per skill, named in `kebab-case`.
- `SKILL.md` must include YAML frontmatter with at least `name` and `description`.
- Keep shared brand assets in `assets/`; skill-local assets live inside the skill folder.
- Document any new conventions back into this file.

## What the agent must NOT do

- **Do not auto-generate or auto-add skills.** Skills are added manually by a human.
- **Do not delete or overwrite the logo** at `assets/Logo/skill_study-related.png`.
- **Do not modify `LICENSE`** or its copyright/attribution.
- **Do not push force** or perform destructive git operations (denied in config).

## Working with Claude Code

- Baseline permissions live in `.claude/settings.json` (read-only + safe git by default).
- Skills are loaded from `.claude/skills/`; link or copy a `skills/<name>` package there
  when you want it active for this project.

## Working with generic agents

- Baseline configuration lives in `.agent/settings.json`.
- `autoAddSkills` is `false` — the agent should not create skills on its own.
- Skill content is discovered under the `skills/` directory.

## Branding

- Logo: `assets/Logo/skill_study-related.png`. Reference it in docs with a relative path.
- Keep the logo and any new assets reasonably sized and in common formats (png/svg).

## License

MIT License. © 2026 Satya. See [`LICENSE`](./LICENSE).
