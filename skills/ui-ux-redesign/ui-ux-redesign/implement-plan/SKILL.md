---
name: implement-plan
description: Implement the existing plan.md — run its 5 phases under the 5 logic-freeze instructions, changing only presentation and preserving all logic and state.
disable-model-invocation: true
---

# implement-plan — execute plan.md phase by phase, logic untouched

Take the existing `plan.md` and implement its 5 phases, changing **only the presentation** while the 5 logic-freeze instructions hold. The transformation recipes live in `TRANSFORM.md` (this folder).

## The flow

**1. Load the plan and the contract.** Read `plan.md` (required — if it's missing, stop and ask the user to run `/plan-redesign` first). Extract the **5 logic-freeze instructions** (Block B) and the **5 phases** (Block C). Load `TRANSFORM.md` for the recipes. The 5 logic-freeze instructions are the operating rule for every edit: state, hooks, handlers, and API/mutations are frozen; only the visual layer moves.
*Done when:* the contract and the 5 phases are loaded, and the frozen logic (from the audit's freeze matrix) is named as the boundary.

**2. Run the phases in order (1 → 5).** For each phase:
- Pick its target components from `plan.md`.
- Apply the transformations using the matching `TRANSFORM.md` recipes (tokens, typography, spatial/bento, motion, responsive) for that phase's components.
- Keep every change inside the visual layer and route all class concatenation through `cn()`.
- **Verify the phase:** the diff for the phase's components is presentation-only — no state, hook, handler, or API/mutation changed. Check against the phase's definition of done.
*Done when:* all 5 phases are implemented and each phase's definition of done is met.

**3. Final zero-regression pass.** Re-check the whole app against the audit's logic-freeze matrix: every frozen hook, handler, and API call is intact; the build/typecheck passes; the visual upgrade is live across the refactored components. Report what changed (presentation) and confirm nothing logic-related moved.
*Done when:* all 5 phases are done and the final zero-regression verification passes — presentation upgraded, logic untouched.
