# Skills: Study-Related

<p align="center">
  <img src="assets/Logo/skill_study-related.png" alt="Skills: Study-Related logo" width="500">
</p>

<p align="center">
  A curated collection of agent skills focused on study, learning, and academic productivity.
</p>

## Overview

This repository is a home for **study-related skills** — modular, reusable capabilities
that agents (Claude Code and other agent runtimes) can load to help with learning,
research, note-taking, and academic workflows.

> Skills are added manually to keep the collection intentional and high-quality.
> See [`agent.md`](./agent.md) for conventions and the full repository layout.

## Repository layout

```text
skills_study-related/
├── assets/            # Brand assets (logo, etc.)
│   └── Logo/
│       └── skill_study-related.png
├── skills/            # Skill packages (added manually later)
├── .claude/           # Claude Code configuration (settings, etc.)
├── .agent/            # Generic agent configuration
├── agent.md           # Agent-facing documentation & conventions
├── README.md          # This file
├── LICENSE            # MIT License
├── .gitignore
└── .editorconfig
```

## Installation

Skills install with the [Skills CLI](https://skills.sh) — the same `npx skills`
installer [AI Hero](https://www.aihero.dev/) uses. No registry or npm publish is
needed; the CLI reads skill packages straight from this repository.

Full reference and every flag: [`INSTALL.md`](./INSTALL.md).

```bash
REPO=coderdoctor97/skills_study-realated-   # or the full URL https://github.com/coderdoctor97/skills_study-realated-

# All skills, project-local
npx skills@latest add "$REPO" --all

# All skills, global (every project)
npx skills@latest add "$REPO" --all --global

# One skill, project-local
npx skills@latest add "$REPO" --skill=<skill-name>

# One skill, global
npx skills@latest add "$REPO" --skill=<skill-name> --global
```

> List what's available first: `npx skills@latest add "$REPO" --list`

A `Makefile` is also provided for convenience: `make install`, `make install-global`,
`make install-skill SKILL=<name>`, `make install-skill-global SKILL=<name>`, `make list`.

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for how to propose or add skills.
Note that skills are intentionally added manually — automated skill generation is
disabled for this repository.

## License

Released under the [MIT License](./LICENSE). © 2026 Satya.
