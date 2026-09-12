---
name: clarify-agent-prompt
description: Rewrite an agent-facing prompt to be structurally clearer and more instructive without altering its instruction, features, or goal. Fires when the user asks to "improve", "clarify", "restructure", or "clean up" a prompt while stressing that its meaning and requirements must not change.
---

A prompt is a document an agent consumes. Its job is that any agent — this model or another, today or later — reads it once and reliably does what is required. Most prompts are sound in meaning but written as a dense paragraph for a human eye; what is missing is structure. This skill supplies the structure. It never changes _what_ must be done; it changes only how clearly that is said.

The input is the prompt in context. The output is a single rewritten prompt, structurally reorganized and explicit enough that an agent can follow it alone — nothing more: no commentary, no change notes, no preamble.

## The three invariants

Protect exactly three things. Every requirement, fact, and constraint in the input must survive in meaning; nothing may be added or removed:

- **Instruction** — what the agent must do. Preserve every action and every requirement it expresses.
- **Features** — every capability, input, option, or behavior the prompt claims or requests. Add none, remove none.
- **Goal** — the outcome the whole prompt serves. Do not widen, narrow, or drift it.

Every line you write must trace to something already stated or implied. If you are tempted to introduce a new requirement, an extra capability, or a different outcome, stop: that is an invariant failing. Guard against the drift you will feel: a cleaner sentence that quietly drops a shade of meaning, a tidier step that quietly demands more.

## What to change

Structure and legibility — the parts that never touch the invariants:

- **Expose the goal up front.** Open with one line stating what the agent is ultimately to produce or achieve, drawn only from what the prompt implies.
- **Separate the parts.** Break the paragraph into regions the agent can consult independently — task, inputs, steps, rules/constraints, output. Group every related constraint under one heading; do not scatter it.
- **One instruction per line.** Break compound, run-on requirements into single-action lines. Preserve each fragment's exact meaning: never merge two requirements into one that loses a shade, nor split one that adds a demand.
- **Surface implied order as steps.** Where the prompt implies a sequence or sub-steps, render them as ordered steps. Treat that as structure, not invention — every step must already be latent in the wording. When no order is implied, keep a list rather than force a sequence.
- **Name references once.** Where the prompt uses a vague pronoun or dropped noun, name the thing exactly once and refer to it by that name thereafter.
- **Give the agent its exit.** If the prompt implies what done looks like, state it plainly as the final line; do not invent a stricter or laxer bound.
- **Stay agent-agnostic.** Rely only on what is stated. Do not assume a particular assistant's capabilities or tools, since the prompt is meant for any agent.

## Completion criteria

Stop when all three hold:

- Every requirement, feature, and constraint from the input is present with meaning preserved — none dropped, weakened, or strengthened. _Check by line_: walk the original and find each piece in the rewrite.
- The output adds no new instruction, feature, or goal. _Check by hunt_: any line you cannot trace to the original is a violation — delete it.
- The output is a single self-contained prompt an agent can follow without the original beside it.

Deliver only that rewritten prompt.
