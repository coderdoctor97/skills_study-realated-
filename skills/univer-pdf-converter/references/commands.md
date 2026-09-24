# Command Specification: Univer PDF Converter

Defines the exact execution semantics, options, and behaviors for the slash commands.

---

## 1. `/convert-to-pdf`

### Purpose
Converts any supported `.md`, `.txt`, or `.docx` file into a production-grade, print-ready PDF using Univer Production Formatting.

### Syntax
```bash
/convert-to-pdf <input_file> [--output <output_path>] [--config <config.json>]
```

### Execution Steps
1. **Locate Target File:** Validates that `<input_file>` exists in the workspace (or under `/uploads/`).
2. **Check Configuration:** Checks for an existing custom formatting configuration (e.g., `pdf-config.json`). If found or passed, loads palette and layout rules; otherwise applies defaults.
3. **Parse & Typeset:**
   - Detects all mathematical formulas and wraps them into styled formula cards.
   - Detects markdown tables and styles them with Univer corporate headers and zebra fills.
   - Detects code blocks and diagrams, upgrading them to high-resolution flowcharts, matrices, or matplotlib graphs.
4. **Compile Canvas:**
   - Runs the two-pass `NumberedCanvas` to calculate total pages and render running headers and `"Page X of Y"` footers.
5. **Inspect & Present:**
   - Validates non-zero byte size and page count.
   - Calls `present_file` to surface the final PDF directly in the user's viewer.

---

## 2. `/custom-pdf`

### Purpose
Runs prior to document generation. Prompts the user with standard configuration questions and captures custom formatting requirements into a `.json` configuration file, which `/convert-to-pdf` subsequently consumes.

### Standard Configuration Options
- **Page Size**: `letter` (8.5 × 11 in) or `a4` (210 × 297 mm).
- **Color Palette Preset**:
  - `univer-navy` (Default: `#1E3A8A` primary, `#0369A1` secondary, `#1E293B` text).
  - `slate-emerald` (`#065F46` emerald, `#0D9488` teal, `#0F172A` text).
  - `modern-crimson` (`#991B1B` burgundy, `#DC2626` crimson, `#18181B` text).
- **Cover Page**: `true` | `false` (Prepend a formal publication cover sheet).
- **Table of Contents**: `true` | `false` (Generate automatic section index).
- **Header & Footer Strings**: Custom document titles and classification stamps.

### Execution Output
Generates `pdf-config.json` in the current working directory:
```json
{
  "pagesize": "letter",
  "palette": {
    "primary": "#1E3A8A",
    "secondary": "#0369A1",
    "text": "#1E293B",
    "surface": "#F8FAFC",
    "card_bg": "#EFF6FF",
    "card_border": "#BFDBFE"
  },
  "include_cover": false,
  "include_index": false,
  "header_title": "Document Title",
  "footer_text": "ACADEMIC RESEARCH SPECIFICATION • UNIVER SUITE"
}
```

---

## 3. `/add [--images] [--cover] [--index] [--source <name>]`

### Purpose
Enriches the document before compilation with AI-generated assets, formal covers, indices, and automated layout diagrams.

### Flags
- `--images`: Prompts the user for image-generation prompts or instructions for uploading assets into the workspace with consistent naming conventions.
- `--cover`: Explicitly instructs the engine to render a standalone formal cover page with document metadata, author, and date.
- `--index`: Generates an automated Table of Contents with section anchors.
- `--source <name>`: Specifies the source directory or asset folder for inline images.

### Default Behavior
- **Inactive unless explicitly invoked**: Standard PDF generation uses default Univer visual styling.
- When invoked, modifies the generation options or writes to `pdf-config.json` before triggering the build.
