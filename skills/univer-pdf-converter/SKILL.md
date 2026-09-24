---
name: univer-pdf-converter
description: "Converts .md, .txt, and .doc/docx files into publication-grade, print-ready PDFs using Univer Office production layout standards. Automatically typesets LaTeX formulas into styled display cards, upgrades ASCII flowcharts and data graphs to vector graphics, and formats structured tables with corporate styling. Includes slash commands: /convert-to-pdf, /custom-pdf, and /add."
---

Converts markdown, plain text, and Word files into print-ready, publication-grade PDFs matching the Univer production styling specification.

Read [`references/univer-standards.md`](references/univer-standards.md) for typographic rules, color palettes, and geometric guidelines.
Read [`references/commands.md`](references/commands.md) for detailed slash command execution mechanics.

## Capabilities & Standards

1. **Academic & Executive Typography**:
   - Clean 54 pt margins, hierarchical headers (`#1E3A8A` H1, `#0369A1` H2), and 9.5 pt high-legibility body text.
   - Dynamic two-pass `NumberedCanvas` rendering `"Page X of Y"` footers and running headers.
2. **Mathematical Typesetting**:
   - Identifies raw LaTeX block syntax (`$$...$$`) and renders isolated, centered mathematical display cards (`#EFF6FF` soft surface with `#BFDBFE` accent border).
   - Formats inline equations into clean italicized variables with proper Unicode sub/superscripts.
3. **Automated Architectural Diagrams & Empirical Graphs**:
   - Converts raw ASCII comparison diagrams into side-by-side color-coded comparative cards.
   - Converts ASCII pipelines into structured multi-node flow tables.
   - Automatically renders statistical data curves (Ebbinghaus decay, testing effect bar charts, Yerkes-Dodson arousal curves) at high resolution.
4. **Structured Tables**:
   - Primary dark header (`#1E3A8A`) with white text, alternating row fills (`#F8FAFC`), and clean 0.5 pt gridlines.

---

## Slash Commands

### 1. `/convert-to-pdf`
Converts any supported `.md`, `.txt`, or `.docx` file into a print-ready PDF using Univer production formatting.

**CLI Invocation:**
```bash
python3 <skill-dir>/bin/univer_pdf_engine.py <input_file> [-o <output.pdf>] [--config <config.json>] [--images] [--cover] [--index]
```

**Steps:**
1. Check that the source file exists.
2. If a `pdf-config.json` exists in the workspace, automatically consume it.
3. Execute the converter engine.
4. Confirm non-zero output file creation and page count.
5. Present the generated PDF in the user viewer using `present_file`.

---

### 2. `/custom-pdf` *(Optional)*
Interactive prompt workflow before document generation. Gathers custom requirements and outputs `pdf-config.json`.

**Interactive Options:**
1. **Page Size**: Letter vs A4.
2. **Color Palette Preset**:
   - `univer-navy` (Default corporate navy & slate).
   - `slate-emerald` (Academic green & teal).
   - `modern-crimson` (Editorial burgundy).
3. **Document Cover Sheet**: Enable / Disable.
4. **Table of Contents / Index**: Enable / Disable.
5. **Header & Footer Text**: Custom title / classification strings.

Write the collected settings to `pdf-config.json` in the active workspace directory.

---

### 3. `/add [--images] [--cover] [--index] [--source <name>]` *(Optional)*
Allows the user to enrich the document prior to compilation:
- **`--images`**: Prompts the user for image-generation prompts or instructions for uploading assets into the workspace with consistent naming.
- **`--cover`**: Instructs the compiler to prepend a formal standalone cover page.
- **`--index`**: Instructs the compiler to build an automated Table of Contents.
- **`--source <name>`**: Specifies an asset directory.

*Default behavior:* Inactive unless invoked; PDF generation proceeds with standard Univer visual styling.

---

## Verification & Completion Criteria

Before concluding any conversion task:
1. Verify the PDF exists at the expected path with non-zero size.
2. Verify that no raw LaTeX code blocks or raw ASCII art leak into the final output.
3. Call `present_file` with the final `.pdf` path so the user can immediately review the rendered output.
