---
name: qna-plan
description: Optional pre-planning Q&A — asks your target design archetype, the design work to do, features to add, and a useful GitHub skill, then writes the answers to qna-plan.md for /plan-redesign to use.
disable-model-invocation: true
---

# qna-plan — optional design-intent Q&A before planning

Before `/plan-redesign`, capture the design intent so the plan is built on *your* choices rather than the agent's assumptions. Ask the questions below (the user may skip any), then write the answers to `qna-plan.md`.

## The questions

Ask as one structured set; let the user skip any.

1. **Target design archetype.** Which look is the goal? Offer these, plus a custom option: *Linear-style Minimalist Dark Mode*, *Stripe-grade Clean SaaS*, *Modern Bento Dashboard*, *Apple-inspired Spatial Glassmorphism*, *Vercel Geist Monochrome*.
2. **Design work to implement.** Specific visual/design improvements the user wants done (typography, spacing, colors, specific components, layouts, motion).
3. **Features to add.** New functionality the user wants. Classify each as *presentation-only* (in scope for this zero-regression redesign) or *logic-changing* (out of scope — a real feature change, to handle separately); flag the logic-changing ones clearly.
4. **A useful GitHub skill.** Which single skill from GitHub would help during planning and implementation (a component kit, icon set, motion library, or design-system generator)? If none, record "none."

## Write the answers

Save `qna-plan.md` at the project root with these sections: **Archetype** (chosen + a line on why), **Design work**, **Features to add** (split into in-scope / out-of-scope), **GitHub skill** (name + what it's for), and any **Notes**.
*Done when:* all four question groups are answered or explicitly marked skipped, and `qna-plan.md` is written and readable by `/plan-redesign`.

## Scope guardrail

This pipeline is a pure-presentation refactor. Any requested feature that changes state, data flow, or side effects is listed under *out-of-scope* and called out as a separate change — the redesign itself never touches logic.
*Done when:* every feature request is classified in-scope or out-of-scope.
