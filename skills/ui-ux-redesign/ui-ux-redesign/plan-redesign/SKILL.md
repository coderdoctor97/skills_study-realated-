---
name: plan-redesign
description: Plan the non-destructive UI/UX redesign of the audited project, drawing strictly on the 27 curated sources, and write plan.md with 5 phases and the 5 logic-freeze instructions.
disable-model-invocation: true
---

# plan-redesign — produce plan.md (5 phases + the 5 logic-freeze instructions)

Turn the audit (and the optional Q&A) into a concrete, phase-by-phase redesign plan for the *existing* project — a pure-presentation upgrade that never touches logic. The output is `plan.md`, which `/implement-plan` then executes.

## The flow

**1. Load the inputs.** Read `ui-ux-audit.md` (required — if it's missing, stop and ask the user to run `/audit-ui-ux` first). Read `qna-plan.md` if present.
- If `qna-plan.md` is present: adopt its **archetype**, design work, in-scope features, and chosen GitHub skill.
- If it's absent: run **best-result mode** — pick the archetype from the audit (dashboard → Modern Bento, product tool → Linear, marketing/SaaS → Stripe, etc.) plus the agent's own knowledge, and record the assumption in the plan's header.
*Done when:* the audit is loaded and the archetype is chosen (from the Q&A or by best-result mode, with the choice recorded).

**2. Bind to the sources strictly.** The plan draws **only** from the 27 curated sources in `SOURCES.md` (this folder). For every planned transformation, name the source(s) it comes from. A need outside the 27 is marked *outside the matrix* and sourced from the audit + the agent's own knowledge.
*Done when:* every phase in the draft cites at least one source from `SOURCES.md` (or is flagged as outside it).

**3. Write `plan.md`.** Compose it from the **template** below, populating each phase with: the target components (from the audit's priority refactor candidates), the specific transformations, the sources drawn from, and a definition of done.
*Done when:* `plan.md` exists with exactly **5 phases**, the **5 logic-freeze instructions**, a recorded archetype, and per-phase sources + definitions of done.

## plan.md template

`plan.md` always contains these three blocks, in this order.

### Block A — header
Project · date · chosen **archetype** (and why) · the subset of the 27 sources the plan uses · which mode (Q&A-driven or best-result) produced it.

### Block B — the 5 logic-freeze instructions
Write these **verbatim**; they are the *logic-freeze contract* that `/implement-plan` holds itself to for every edit.

1. **Preserve every state and hook.** Every `useState`, `useReducer`, `useRef`, `useMemo`, `useCallback`, `useContext`, and third-party hook (`useQuery`, `useForm`, `useRouter`, `useSearchParams`) keeps its exact name, dependency array, and internal logic. Change only how the output is presented.
2. **Preserve every handler and event.** Every `onClick`, `onSubmit`, `onChange`, `onKeyDown`, `onBlur`, and custom callback stays attached to its element with an unchanged signature and payload. Change only that element's appearance.
3. **Preserve every API and mutation.** Server actions, API-route requests, React Query mutations, and SWR revalidations keep identical arguments and effects.
4. **Stay inside the visual layer.** Every change comes from JSX restructure, Tailwind utility swaps, added decorative sub-elements, and accessible/motion wrappers around existing elements — never from data flow, validation, or side effects.
5. **Merge classes safely.** Any concatenated or prop-passed class string goes through `cn()` (clsx + tailwind-merge) so styles never collide.

### Block C — the 5 phases
Each phase has: goal, target components (from the audit), the transformations to apply (the detail lives in `implement-plan/TRANSFORM.md`), the sources drawn from (`SOURCES.md`), and a definition of done.

1. **Foundation & design tokens** — semantic color tokens, the type scale, the 8pt spacing scale, dark-mode ramps, the `cn()` helper, and base global styles.
2. **Atomic components** — the audit's primitives: buttons, inputs, badges, cards, modals, switches, tooltips.
3. **Layout & domain components** — nav, sidebar, app shell, footers, and feature/domain components; introduce bento-grid architecture where it fits.
4. **Motion, micro-interactions & feedback** — state transitions, active-press haptics, accessible focus rings, loading skeletons/shimmer, toasts, and spring/tab animations.
5. **Responsive parity, accessibility & verification** — mobile ergonomics (44px targets, tables → cards, modals → bottom sheets), accessibility (focus, aria, contrast), zero-CLS, and the final zero-regression check.
