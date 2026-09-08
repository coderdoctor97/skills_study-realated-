## Convenience targets for installing skills from this repository
## using the Skills CLI (https://skills.sh) — the same installer AI Hero uses.
##
## Usage:
##   make install                     # all skills, project-local
##   make install-global              # all skills, global
##   make install-skill SKILL=foo     # one skill, project-local
##   make install-skill-global SKILL=foo
##   make list                        # list available skills

REPO  ?= coderdoctor97/skills_study-realated-
SKILL ?=

.PHONY: install install-global install-skill install-skill-global list

install:
	npx skills@latest add $(REPO) --all

install-global:
	npx skills@latest add $(REPO) --all --global

install-skill:
	@test -n "$(SKILL)" || (echo "Set SKILL=<name>, e.g. make install-skill SKILL=flashcard-generator" && exit 1)
	npx skills@latest add $(REPO) --skill=$(SKILL)

install-skill-global:
	@test -n "$(SKILL)" || (echo "Set SKILL=<name>, e.g. make install-skill-global SKILL=flashcard-generator" && exit 1)
	npx skills@latest add $(REPO) --skill=$(SKILL) --global

list:
	npx skills@latest add $(REPO) --list
