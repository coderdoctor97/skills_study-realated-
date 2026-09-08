# Installing Skills

This repository is wired to work with the [Skills CLI](https://skills.sh) — the
open-source `npx skills` installer that [AI Hero](https://www.aihero.dev/) uses
(for example `npx skills@latest add mattpocock/skills`). There is **no npm
package or registry to publish**: the CLI reads skill packages directly from this
GitHub repository and copies them into your agent's skills folder.

## Repository reference

Use either form as the `<repo>` argument in every command below:

| Form             | Value                                                            |
| ---------------- | --------------------------------------------------------------- |
| GitHub shorthand | `coderdoctor97/skills_study-realated-`                          |
| Full URL         | `https://github.com/coderdoctor97/skills_study-realated-`       |

> The CLI installs from the repository's **default branch**. Skills are added
> manually (see [`agent.md`](./agent.md) / [`CONTRIBUTING.md`](./CONTRIBUTING.md)),
> so run `--list` first to see what is currently available.

## Prerequisites

- [Node.js](https://nodejs.org) 18 or newer. The installer runs via `npx`, so
  nothing needs to be installed globally.
- The agent you want to install into (Claude Code, Codex, Cursor, Cline, etc.).
  The CLI auto-detects installed agents; use `-a/--agent` to target a specific one.

## Install ALL skills at once

| Scope    | Command                                                                                   |
| -------- | ----------------------------------------------------------------------------------------- |
| Local    | `npx skills@latest add coderdoctor97/skills_study-realated- --all`                         |
| Global   | `npx skills@latest add coderdoctor97/skills_study-realated- --all --global`                |

`--all` installs every skill to every detected agent, non-interactively. Add
`--global` (`-g`) to install into your user directory (`~/<agent>/skills/`) so the
skills are available in **all** projects.

Explicit equivalent (handy when targeting specific agents):

```bash
# All skills, project-local, only Claude Code + Codex
npx skills@latest add coderdoctor97/skills_study-realated- --skill '*' -a claude-code -a codex
```

## Install a SINGLE, specific skill

Use the `--skill` (`-s`) flag with the skill's folder name (the name under
`skills/`).

| Scope    | Command                                                                                               |
| -------- | ----------------------------------------------------------------------------------------------------- |
| Local    | `npx skills@latest add coderdoctor97/skills_study-realated- --skill=<skill-name>`                      |
| Global   | `npx skills@latest add coderdoctor97/skills_study-realated- --skill=<skill-name> --global`            |

Example — install only the `flashcard-generator` skill, project-local:

```bash
npx skills@latest add coderdoctor97/skills_study-realated- --skill=flashcard-generator
```

Example — install it globally, targeting Claude Code only, non-interactively:

```bash
npx skills@latest add coderdoctor97/skills_study-realated- --skill=flashcard-generator --global -a claude-code -y
```

Chain multiple `--skill` flags to install several at once:

```bash
npx skills@latest add coderdoctor97/skills_study-realated- --skill=flashcard-generator --skill=note-taker
```

## For agents / CI (non-interactive)

Add `-y` / `--yes` to skip every confirmation prompt. Combine with `--global` and
`--skill` (or `--all`) for fully automated installs:

```bash
# One skill, global, no prompts
npx skills@latest add coderdoctor97/skills_study-realated- --skill=<skill-name> --global -y

# All skills, global, no prompts
npx skills@latest add coderdoctor97/skills_study-realated- --all --global -y
```

## Discover available skills

```bash
npx skills@latest add coderdoctor97/skills_study-realated- --list
```

## Command reference (flags)

| Flag                   | Effect                                                       |
| ---------------------- | ------------------------------------------------------------ |
| `-g, --global`         | Install to user directory instead of the current project     |
| `-a, --agent <a...>`   | Target specific agents (e.g. `claude-code`, `codex`)        |
| `-s, --skill <s...>`   | Install specific skills by name (`'*'` = all)               |
| `-l, --list`           | List available skills without installing                     |
| `--copy`               | Copy files instead of symlinking                             |
| `-y, --yes`            | Skip all confirmation prompts                                |
| `--all`                | Install all skills to all agents, non-interactively          |

## How the CLI finds skills

The installer scans the repository for skill packages — folders that contain a
`SKILL.md` file. New skills are added under `skills/<skill-name>/SKILL.md` (see
[`agent.md`](./agent.md) for the exact convention). Once a skill exists on the
default branch, the commands above will install it.

## Updating installed skills

```bash
npx skills update            # update all installed skills
npx skills update -g         # update only global skills
npx skills update <skill>    # update a specific skill
```
