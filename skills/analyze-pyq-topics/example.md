Example run of `analyze-pyq-topics` on 3 years of a "Biology" paper (illustrative, condensed).

## Input papers (condensed questions)

- 2024: Q1 "Define photosynthesis and state where it occurs." Q2 "Explain the structure of a neuron." Q3 "Describe the human heart's chambers."
- 2023: Q1 "List the stages of photosynthesis." Q2 "What is the function of a neuron's axon?" Q3 "Compare mitosis and meiosis."
- 2022: Q1 "Where does the light reaction of photosynthesis happen?" Q2 "Name the four chambers of the heart."

## Produced report (what the skill returns)

**Scope:** Biology, papers 2022–2024.

| Topic | Questions | Distinct years | Share | High-yield flags |
|---|---|---|---|---|
| Photosynthesis | 4 | 3 | 44% | Repeat (3 yrs) + Top-fraction + Top priority |
| Cell biology (neuron/mitosis) | 3 | 2 | 33% | Repeat (2 yrs) |
| Human anatomy (heart) | 2 | 2 | 22% | Repeat (2 yrs) |

**High-yield summary**
- **Photosynthesis — top priority.** Appears in every year (3/3). Flagged by the repeat lens (most distinct years) and the top-fraction lens (highest count). Questions recur across papers rather than repeat verbatim.
- **Cell biology — high-yield.** Present 2 of 3 years.
- **Human anatomy — high-yield.** Present 2 of 3 years.

**Repeat highlights:** Photosynthesis recurs in all three papers — the clearest "frequently repeated" signal.

**Scope note:** none excluded; taxonomy chosen as the three natural units above.
