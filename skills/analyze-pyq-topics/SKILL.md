---
name: analyze-pyq-topics
description: Analyze previous-year question papers (PYQs) to categorize questions by topic and identify frequently repeated / high-yield topics. Fires when asked to analyze past exam papers or PYQs, group questions by topic, subject, chapter or unit, or find repeated, high-yield, most-important or frequently-asked exam topics.
---

Analyze previous-year question papers (PYQs) and turn them into a topic map: every question assigned to its topic, and the topics ranked so the frequently repeated, high-yield ones stand out. The deliverable is a single structured report (tables), not the raw papers back.

Work on the content of the papers only. Do not judge answers or mark them correct; your job is classification and counting.

## Inputs

The source papers are whatever is available for the task — any file type and any origin: PDF, Word (`docx`/`doc`), plain text (`.txt`), Markdown (`.md`), spreadsheets, Google-Drive-backed files, or scanned/image pages that need OCR. Callers may upload files directly or point to a location. Never assume a specific type or origin; use what is actually supplied.

## Steps

1. **Assemble and read the source material.** Gather every paper supplied for the task and get its content into readable text by whatever means is available for its type (text extraction, document parsing, OCR for images or scans). A paper whose text you cannot obtain cannot be classified — so do not silently skip it:
   - If a scanned or image-only paper is present and OCR is available, run it so the paper enters the analysis.
   - If some material genuinely cannot be read, proceed on what you can and state clearly in the report that those papers were excluded and why.
   - **Completion criterion:** the text of every readable paper is in hand, and each paper is tied to its year/session label when known.

2. **Fix the topic taxonomy.** Decide the set of topics you will classify into, derived from what the questions actually ask about (the natural units/chapters of the subject), not from the papers' own section headings. Keep the taxonomy as a single consistent list and reuse the same topic names throughout so counts stay meaningful. Aim for a granularity where a question lands in exactly one bucket and buckets are neither so fine that repeats vanish nor so coarse that topics blur.
   - **Completion criterion:** there is one fixed list of topics, and you can assign every question to exactly one of them.

3. **Tag every question.** Go paper by paper and assign each distinct question to exactly one topic. For a compound or borderline question that spans topics, choose the topic it most centrally tests and note the runner-up topics in a remark column rather than splitting the question's count.
   - **Completion criterion:** every question across all read papers is tagged to exactly one topic, with no question left untagged or double-counted.

4. **Aggregate per topic.** For each topic, count (a) how many questions it received, and (b) across how many distinct years/papers it appears. When a paper shows marks, also sum the marks per topic. Keep the underlying counts so the report is reproducible.

5. **Determine high-yield topics across all three lenses.** Do not rely on a single rule — report each lens so no signal is hidden:
   - **Repeat lens:** topics appearing in the most distinct years/papers, and with the highest raw question counts.
   - **Top-fraction lens:** topics in the top rank by frequency (e.g. the top few topics or the top fraction of the taxonomy).
   - **Weight lens:** topics carrying the most marks where the papers show marks (frequency and weight often diverge — report both).
   A topic is high-yield when it ranks high on any lens; say which lens flagged it, rather than collapsing to one vague label.
   - **Completion criterion:** you can state, per topic, how it scored on each lens.

6. **Build the report.** Assemble one structured report as the final output.

## Output — the report

A single structured document containing:

- **Header line:** subject/paper set analyzed, and the set of years/sessions covered (so scope is visible).
- **Topic table** (one row per topic): Topic | Questions | Distinct years | Share of all questions | Marks (if shown) | High-yield flags. Ranked by frequency.
- **High-yield summary:** the topics flagged high-yield and, for each, the lens(es) that flagged it and its repeat count. Mark the most important few as top priority.
- **Repeat highlights:** note any topic that recurs across many years — that recurrence is the "frequently repeated" signal you were asked to find.
- **Scope note:** any paper excluded (and why), and any assumption you made about taxonomy.

Present tables wherever a list would hide a relationship. Do not invent curriculum advice beyond what the counts show.

## Completion criteria

Stop when the report is delivered and all of the following hold:

- Every readable question is categorized under a topic, and no topic is an empty catch-all used only to clear leftover questions.
- Per-topic counts and distinct-year counts are present and internally consistent (e.g. shares sum sensibly, no double-counting).
- High-yield topics are identified and are justified by at least one lens you state explicitly.
- The report states the scope (papers/years analyzed) and any excluded material.
