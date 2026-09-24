# Univer Visual Standards & PDF Specification

This reference defines the typographic, geometric, mathematical, and diagrammatic rules required for Univer production-grade PDFs.

## 1. Typography & Hierarchy

- **Title (`H0` / `#`)**: 19–20 pt Helvetica-Bold. Leading: 24–25 pt. Color: Primary Dark `#0F172A`.
- **Heading 1 (`##`)**: 13.5–14 pt Helvetica-Bold. Leading: 17–18 pt. Color: Accent Navy `#1E3A8A`. Space before: 14 pt, space after: 6 pt. `keepWithNext: True`.
- **Heading 2 (`###`)**: 11–11.5 pt Helvetica-Bold. Leading: 15 pt. Color: Cerulean `#0369A1`. Space before: 10 pt, space after: 5 pt. `keepWithNext: True`.
- **Heading 3 (`####`)**: 9.5–10 pt Helvetica-Bold. Leading: 13 pt. Color: Slate `#334155`. Space before: 8 pt, space after: 3 pt. `keepWithNext: True`.
- **Body Text**: 9.5 pt Helvetica. Leading: 13.8–14 pt. Color: Deep Slate `#1E293B`. Space after: 6 pt.
- **Monospace / Code**: Courier / Liberation Mono. 7.5–8 pt. Leading: 10–11 pt. Color: `#0F172A`. Background: `#F1F5F9`.

## 2. Page Geometry & Running Elements

- **Page Dimensions**: Standard US Letter (8.5 × 11 in) or ISO A4 (210 × 297 mm).
- **Margins**: 54 pt (0.75 in) uniform left, right, top, and bottom margins. Available printable width: 504 pt.
- **Top Running Header (Pages > 1)**:
  - Left: Document Title or active section (Helvetica 8 pt, `#64748B`).
  - Right: "Univer Document Specification" (Helvetica 8 pt, `#64748B`).
  - Baseline separator line: 0.5 pt stroke, `#CBD5E1`, Y = 742 pt.
- **Bottom Running Footer (All Pages)**:
  - Left: Classification / Organization specification string (Helvetica 8 pt, `#64748B`).
  - Right: Dynamic two-pass `"Page X of Y"` string.
  - Top separator line: 0.5 pt stroke, `#CBD5E1`, Y = 46 pt.

## 3. Mathematical Formula Cards

Raw LaTeX syntax (`$$...$$` or `$...$`) is strictly prohibited in final deliverables.

- **Display Formulas**: Rendered inside isolated, centered callout cards (`#EFF6FF` soft blue surface, `1 pt` border in `#BFDBFE`).
- **Typography**: Italicized symbols ($L$, $t$, $S$, $\alpha$), proper Unicode sub/superscripts ($L_{\text{total}}$, $S_{n-1}$, $e^{-t/S}$), and bolded functional equations.
- **Inline Variables**: Converted to clean italicized HTML entities with proper sub/superscripts.

## 4. Structured Tables

- **Header Row**: Deep Navy `#1E3A8A` background with bold white text (`#FFFFFF`).
- **Alternating Rows**: Zebra-striped between `#FFFFFF` and off-white `#F8FAFC`.
- **Grid Lines**: Thin 0.5 pt borders in `#CBD5E1`.
- **Padding**: 6 pt horizontal, 4 pt vertical for optimal information density without crowding.

## 5. Architectural Flowcharts & Data Graphs

Textual ASCII diagrams must be parsed and upgraded into publication-grade visual components:
- **Comparison Blocks**: Split two-column comparison cards with color-coded sentiment backgrounds (`#FEF2F2` for baseline/traditional vs. `#F0FDF4` for optimized/CAPF).
- **Process Pipelines**: Multi-node horizontal flow tables with directional glyphs (`──►`, `▼`) and styled entity containers.
- **Empirical Bar Charts**: Rendered with Matplotlib at high DPI (200+), clean slate axis typography, hidden top/right spines, and direct data labels.
- **Decay & Distribution Curves**: Smooth parametric vector plots with annotated thresholds and soft confidence fills.
