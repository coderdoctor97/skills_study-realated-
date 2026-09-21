# UI/UX Redesign pipeline — 4 skills for Next.js + Tailwind

A **non-destructive** UI/UX redesign pipeline for Next.js + Tailwind projects: a pure presentation upgrade with **zero logic regression**. Four slash-command skills, run in order.

| # | Command | What it does | Output |
|---|---------|--------------|--------|
| 1 | `/audit-ui-ux` | Read-only UI/UX audit of the project in the workspace | `ui-ux-audit.md` |
| 2 | `/qna-plan` *(optional)* | Asks your design archetype, design work, features to add, and a useful GitHub skill | `qna-plan.md` |
| 3 | `/plan-redesign` | Plans the redesign, drawing **strictly** on the 27 curated sources | `plan.md` (5 phases + 5 logic-freeze instructions) |
| 4 | `/implement-plan` | Implements `plan.md` phase by phase, changing only presentation | the refactored components |

**Run order:** `/audit-ui-ux` → (optionally) `/qna-plan` → `/plan-redesign` → `/implement-plan`.

If you skip `/qna-plan`, `/plan-redesign` runs in **best-result mode**: it picks the archetype and design direction from the audit plus its own knowledge, and states the assumption in the plan.

## The core rule

The redesign is **presentation-only**. Every state, hook, handler, and API/mutation is frozen (the *logic-freeze contract*, carried in `plan.md` as its 5 instructions). Only the visual layer moves — JSX layout, Tailwind classes, decorative sub-elements, and accessible/motion wrappers.

## Install

Each of the four subfolders is a skill (a folder containing `SKILL.md`). Copy all four into your skills directory, e.g.:

```
~/.agents/skills/audit-ui-ux/
~/.agents/skills/qna-plan/
~/.agents/skills/plan-redesign/
~/.agents/skills/implement-plan/
```

(Or with the `skills` CLI: add the repo, then install each of the four by name.)

## Contents

```
ui-ux-redesign/
├── README.md
├── audit-ui-ux/
│   └── SKILL.md
├── qna-plan/
│   └── SKILL.md
├── plan-redesign/
│   ├── SKILL.md
│   └── SOURCES.md        the 27 curated sources (planning draws strictly from this)
└── implement-plan/
    ├── SKILL.md
    └── TRANSFORM.md      the concrete presentation recipes
```

## Notes

- **User-invoked by default** (`disable-model-invocation: true`) — each command fires only when you type it, at zero standing context cost. To let the agent offer a step unprompted, flip that flag off in that one skill.
- **Strict sources:** `/plan-redesign` plans only from the 27 curated sources in `SOURCES.md` and cites them per phase; anything else is flagged as *outside the matrix*.
- **Shared state lives in the workspace** (`ui-ux-audit.md`, `qna-plan.md`, `plan.md`), so the four skills install independently and hand off through those files.
