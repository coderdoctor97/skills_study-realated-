# Skills: Study-Related

<p align="center">
  <img src="assets/Logo/skill_study-related.png" alt="Skills: Study-Related logo" width="260">
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

## Using the skills

### Claude Code
When skills are added under `skills/`, load them by copying or symlinking the
relevant skill directory into a project's `.claude/skills/` folder, or reference
this repository's skills directly.

### Generic agents
Load skills following your agent runtime's documentation. Baseline agent
configuration lives in `.agent/settings.json`.

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for how to propose or add skills.
Note that skills are intentionally added manually — automated skill generation is
disabled for this repository.

## License

Released under the [MIT License](./LICENSE). © 2026 Satya.
