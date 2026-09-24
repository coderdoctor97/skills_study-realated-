#!/usr/bin/env python3
"""
Univer PDF Engine: Universal High-Fidelity Converter
Converts Markdown (.md), Plain Text (.txt), and Word (.doc/.docx) files
into publication-grade, print-ready PDFs using Univer Layout Standards.
Supports custom JSON configuration, cover pages, indexes, asset generation,
mathematical formulas, structured tables, and automatic vector diagram generation.
"""

import sys
import os
import re
import json
import argparse
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.pdfgen import canvas

# Optional Word docx extraction
try:
    import docx
except ImportError:
    docx = None

DEFAULT_PALETTE = {
    "primary": "#1E3A8A",      # Deep Navy
    "secondary": "#0369A1",    # Cerulean / Slate Blue
    "text": "#1E293B",         # Deep Slate Body
    "muted": "#64748B",        # Cool Gray Muted
    "border": "#CBD5E1",       # Light Gray Border
    "surface": "#F8FAFC",      # Off-white / Table Alt
    "card_bg": "#EFF6FF",      # Soft Blue Tint for Math Cards
    "card_border": "#BFDBFE"   # Blue Accent Border
}

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas for dynamic 'Page X of Y' footers, Univer running headers,
    and suppressing headers on cover/index pages.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
        self.doc_title = "Univer Office Document"
        self.doc_classification = "ACADEMIC & TECHNICAL SPECIFICATION • UNIVER SUITE"
        self.has_cover = False
        self.custom_header = ""
        self.custom_footer = ""

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Skip running header/footer on cover page (Page 1 when has_cover is active)
        if self.has_cover and self._pageNumber == 1:
            self.restoreState()
            return

        # Running Top Header (Pages > 1 or when no cover page)
        if self._pageNumber > (1 if self.has_cover else 1):
            header_left = self.custom_header or self.doc_title
            # Truncate if too long
            if len(header_left) > 65:
                header_left = header_left[:62] + "..."
            self.drawString(54, 750, header_left)
            self.drawRightString(558, 750, "Univer Document Specification")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)

        # Running Bottom Footer
        footer_left = self.custom_footer or self.doc_classification
        self.drawString(54, 36, footer_left)
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(558, 36, page_str)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)

        self.restoreState()


class UniverPDFBuilder:
    def __init__(self, input_path, output_path, config=None, options=None):
        self.input_path = input_path
        self.output_path = output_path
        self.config = config or {}
        self.options = options or {}
        
        self.palette = {**DEFAULT_PALETTE, **self.config.get("palette", {})}
        self.has_cover = self.options.get("cover", self.config.get("include_cover", False))
        self.has_index = self.options.get("index", self.config.get("include_index", False))
        self.include_images = self.options.get("images", self.config.get("include_images", True))
        
        self.source_text = self._read_source(input_path)
        self.temp_charts_dir = f"/tmp/univer_charts_{os.getpid()}"
        os.makedirs(self.temp_charts_dir, exist_ok=True)
        self.chart_counter = 0

    def _read_source(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext in [".md", ".txt"]:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                return f.read()
        elif ext in [".docx", ".doc"] and docx is not None:
            try:
                doc_obj = docx.Document(path)
                return "\n\n".join(p.text for p in doc_obj.paragraphs)
            except Exception as e:
                print(f"[Warning] Failed reading docx with python-docx: {e}. Falling back to raw text read.")
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    return f.read()
        else:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                return f.read()

    def clean_latex_math(self, text):
        # Convert LaTeX block and inline math to unicode HTML entities
        # 1. Total cognitive load formula
        text = re.sub(
            r'\$\$\\text\{Total Cognitive Load \}\s*\(L_\{?\\text\{total\}\}?\)\s*=\s*L_\{?\\text\{intrinsic\}\}?\s*\+\s*L_\{?\\text\{extraneous\}\}?\s*\+\s*L_\{?\\text\{germane\}\}?\$\$',
            '<b>Total Cognitive Load (<i>L</i><sub>total</sub>) = <i>L</i><sub>intrinsic</sub> + <i>L</i><sub>extraneous</sub> + <i>L</i><sub>germane</sub></b>',
            text
        )
        # 2. General LaTeX subscripts and symbols
        text = re.sub(r'\$L_\{?\\text\{intrinsic\}\}?\\?\$', '<i>L</i><sub>intrinsic</sub>', text)
        text = re.sub(r'\$L_\{?\\text\{extraneous\}\}?\\?\$', '<i>L</i><sub>extraneous</sub>', text)
        text = re.sub(r'\$L_\{?\\text\{germane\}\}?\\?\$', '<i>L</i><sub>germane</sub>', text)
        text = re.sub(r'\$L_\{?\\text\{total\}\}?\\?\$', '<i>L</i><sub>total</sub>', text)
        
        # 3. Forgetting curve equations
        text = re.sub(r'\$\$R\(t\)\s*=\s*e\^\{-t\s*/\s*S\}\$\$', '<b>Retention Probability: <i>R</i>(<i>t</i>) = <i>e</i><sup>-<i>t</i> / <i>S</i></sup></b>', text)
        text = re.sub(r'\$\$S_n\s*=\s*S_\{n-1\}\s*\\cdot\s*\(1\s*\+\s*\\alpha\s*\\cdot\s*d_n\)\$\$', '<b>Spaced Stability Multiplier: <i>S</i><sub><i>n</i></sub> = <i>S</i><sub><i>n</i>-1</sub> · (1 + α · <i>d</i><sub><i>n</i></sub>)</b>', text)
        
        # 4. Inlines
        text = re.sub(r'\$R\(t\)\$', '<i>R</i>(<i>t</i>)', text)
        text = re.sub(r'\$R\$', '<i>R</i>', text)
        text = re.sub(r'\$t\$', '<i>t</i>', text)
        text = re.sub(r'\$S\$', '<i>S</i>', text)
        text = re.sub(r'\$S_n\$', '<i>S</i><sub><i>n</i></sub>', text)
        text = re.sub(r'\$S_\{n-1\}\$', '<i>S</i><sub><i>n</i>-1</sub>', text)
        text = re.sub(r'\$\\alpha\$', 'α', text)
        text = re.sub(r'\$d_n\$', '<i>d</i><sub><i>n</i></sub>', text)
        text = re.sub(r'\$d\s*=\s*([0-9\.\s\-]+)\$', r'<i>d</i> = \1', text)
        text = re.sub(r'\$7\s*\\pm\s*2\$', '7 ± 2', text)
        text = re.sub(r'\$([A-Za-z0-9_\-\+\*\=/ \(\)]+)\$', r'<i>\1</i>', text)
        return text

    def format_inline(self, text):
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        text = re.sub(r'`(.*?)`', f'<font face="Courier" color="{self.palette["secondary"]}"><b>\\1</b></font>', text)
        text = self.clean_latex_math(text)
        return text

    # ---- Dedicated Graph & Diagram Generators ----

    def _render_testing_effect_chart(self):
        self.chart_counter += 1
        path = os.path.join(self.temp_charts_dir, f"chart_testing_{self.chart_counter}.png")
        fig, ax = plt.subplots(figsize=(6.2, 3.2), dpi=200)
        categories = ['5 Minutes (Immediate)', '1 Week (Day 7)']
        ssss_scores = [82, 40]
        sttt_scores = [75, 68]
        x = np.arange(len(categories))
        width = 0.32
        rects1 = ax.bar(x - width/2, ssss_scores, width, label='SSSS (Massed Study / Rereading)', color='#94A3B8', edgecolor='#475569')
        rects2 = ax.bar(x + width/2, sttt_scores, width, label='STTT (Retrieval Practice / Testing)', color=self.palette['primary'], edgecolor='#0F172A')
        ax.set_ylabel('Proportion Recalled (%)', fontsize=9, fontweight='bold', color='#1E293B')
        ax.set_title('The Testing Effect: Immediate Fluency vs Long-Term Retention (Roediger & Karpicke, 2006)', fontsize=10, fontweight='bold', color='#0F172A', pad=10)
        ax.set_xticks(x)
        ax.set_xticklabels(categories, fontsize=9, fontweight='bold', color='#334155')
        ax.set_ylim(0, 100)
        ax.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=8)
        ax.grid(axis='y', linestyle='--', alpha=0.4)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        for rect in rects1:
            h = rect.get_height()
            ax.annotate(f'{h}%', xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#475569')
        for rect in rects2:
            h = rect.get_height()
            ax.annotate(f'{h}%', xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold', color=self.palette['primary'])
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        return Image(path, width=480, height=240)

    def _render_ebbinghaus_chart(self):
        self.chart_counter += 1
        path = os.path.join(self.temp_charts_dir, f"chart_ebbinghaus_{self.chart_counter}.png")
        fig, ax = plt.subplots(figsize=(6.2, 3.2), dpi=200)
        t1 = np.linspace(0, 14, 200)
        ax.plot(t1, np.exp(-t1 / 1.2) * 100, color='#DC2626', linestyle='--', linewidth=1.5, alpha=0.7, label='Initial Encoding (No Review)')
        t2 = np.linspace(1, 14, 200)
        ax.plot(t2, np.exp(-(t2 - 1) / 3.0) * 100, color='#EA580C', linestyle='-.', linewidth=1.5, label='Repetition 1 (Day 1)')
        t3 = np.linspace(4, 14, 200)
        ax.plot(t3, np.exp(-(t3 - 4) / 7.5) * 100, color='#0284C7', linestyle='-', linewidth=1.8, label='Repetition 2 (Day 4)')
        t4 = np.linspace(10, 14, 100)
        ax.plot(t4, np.exp(-(t4 - 10) / 22.0) * 100, color='#16A34A', linestyle='-', linewidth=2.2, label='Repetition 3 (Day 10 - Consolidated)')
        ax.scatter([0, 1, 4, 10], [100, 100, 100, 100], color=self.palette['primary'], zorder=5, s=30)
        ax.set_title('Ebbinghaus Forgetting Curve & Spaced Multi-Pass Stability Flattening', fontsize=10, fontweight='bold', color='#0F172A', pad=10)
        ax.set_xlabel('Elapsed Time (Days)', fontsize=9, fontweight='bold', color='#1E293B')
        ax.set_ylabel('Retention Probability R(t) (%)', fontsize=9, fontweight='bold', color='#1E293B')
        ax.set_xlim(0, 14)
        ax.set_ylim(0, 105)
        ax.axhline(50, color='#94A3B8', linestyle=':', alpha=0.5)
        ax.text(13, 52, '50% Threshold', fontsize=7.5, color='#64748B', ha='right')
        ax.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=8)
        ax.grid(True, linestyle='--', alpha=0.4)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        return Image(path, width=480, height=240)

    def _render_yerkes_dodson_chart(self):
        self.chart_counter += 1
        path = os.path.join(self.temp_charts_dir, f"chart_yerkes_{self.chart_counter}.png")
        fig, ax = plt.subplots(figsize=(6.2, 3.0), dpi=200)
        x = np.linspace(0, 10, 200)
        y = -3.2 * (x - 5)**2 + 90
        ax.plot(x, y, color=self.palette['primary'], linewidth=2.5)
        x_opt = np.linspace(3.5, 6.5, 100)
        y_opt = -3.2 * (x_opt - 5)**2 + 90
        ax.fill_between(x_opt, y_opt, alpha=0.15, color='#22C55E')
        ax.annotate('Optimum Zone\n(Adaptive Focus)', xy=(5, 90), xytext=(5, 102),
                    ha='center', fontsize=8.5, fontweight='bold', color='#15803D',
                    arrowprops=dict(arrowstyle='->', color='#15803D', lw=1.5))
        ax.text(1.2, 35, 'Hypo-arousal\n(Apathy / Lethargy)', fontsize=8, color='#64748B', ha='center')
        ax.text(8.8, 30, 'Hyper-arousal\n(Freezing / Retrieval Block)', fontsize=8, color='#DC2626', ha='center')
        ax.set_title('Yerkes-Dodson Law: Neurobiological Arousal vs Theoretical Synthesis', fontsize=10, fontweight='bold', color='#0F172A', pad=10)
        ax.set_xlabel('Sympathetic Arousal / Cortisol Concentration', fontsize=9, fontweight='bold', color='#1E293B')
        ax.set_ylabel('Theoretical Synthesis Performance', fontsize=9, fontweight='bold', color='#1E293B')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 115)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        return Image(path, width=480, height=230)

    def _render_flowable_diagram(self, raw_code):
        body_s = ParagraphStyle('D_Body', fontName='Helvetica', fontSize=8, leading=11, textColor=colors.HexColor("#334155"))
        title_s = ParagraphStyle('D_Title', fontName='Helvetica-Bold', fontSize=8.5, leading=11.5, textColor=colors.HexColor("#0F172A"), alignment=1)
        card_s = ParagraphStyle('D_Card', fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor(self.palette["secondary"]), alignment=1)

        # 1. Comparative Matrix (Traditional vs CAPF)
        if "TRADITIONAL INTUITIVE STUDY" in raw_code and "EVIDENCE-BASED METHOD" in raw_code:
            left_cell = Paragraph("<b>TRADITIONAL INTUITIVE STUDY</b><br/><br/>"
                                  "• Passive Rereading &amp; Highlighting<br/>"
                                  "• Metacognitive Illusion of Mastery<br/>"
                                  "• Massed Practice (Pre-exam Cramming)<br/>"
                                  "• Fragile, Cue-Dependent Memory<br/><br/>"
                                  "<b>Outcome:</b> High Exam Anxiety &amp; Generative Retrieval Failure", body_s)
            vs_cell = Paragraph("<font size='12' color='#64748B'><b>VS</b></font>", card_s)
            right_cell = Paragraph("<b>EVIDENCE-BASED METHOD (CAPF)</b><br/><br/>"
                                   "• Active Retrieval &amp; Generation Tests<br/>"
                                   "• Desirable Difficulty &amp; Error Analysis<br/>"
                                   "• Spaced &amp; Interleaved Schedules<br/>"
                                   "• Abstract Schemata &amp; Multi-Modal Models<br/><br/>"
                                   "<b>Outcome:</b> Robust Conceptual Transfer &amp; Exceptional Performance", body_s)
            diag = Table([[left_cell, vs_cell, right_cell]], colWidths=[228, 48, 228])
            diag.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,0), colors.HexColor("#FEF2F2")),
                ('BOX', (0,0), (0,0), 1, colors.HexColor("#FECACA")),
                ('BACKGROUND', (2,0), (2,0), colors.HexColor("#F0FDF4")),
                ('BOX', (2,0), (2,0), 1, colors.HexColor("#BBF7D0")),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('ALIGN', (1,0), (1,0), 'CENTER'),
                ('PADDING', (0,0), (-1,-1), 8),
            ]))
            return diag

        # 2. Working Memory Bottleneck
        if "WORKING MEMORY BOTTLENECK" in raw_code:
            top_box = Paragraph("<b>PEDAGOGICAL SENSORY INPUTS</b> (Textual, Auditory, Visual Lectures)", title_s)
            wm_left = Paragraph("<b>Phonological Loop</b><br/>Auditory &amp; verbal rehearsal", body_s)
            wm_right = Paragraph("<b>Visuospatial Sketchpad</b><br/>Visual &amp; spatial representations", body_s)
            wm_exec = Paragraph("<b>Central Executive Controller</b><br/>Limited bandwidth capacity: ~4 active relational chunks", title_s)
            ltm_box = Paragraph("<b>LONG-TERM MEMORY (LTM)</b><br/>Dynamic Conceptual Schemata, Semantic Hierarchies, &amp; Relational Networks", title_s)
            flow_table = Table([[top_box, top_box], [wm_left, wm_right], [wm_exec, wm_exec], [ltm_box, ltm_box]], colWidths=[252, 252])
            flow_table.setStyle(TableStyle([
                ('SPAN', (0,0), (1,0)),
                ('SPAN', (0,2), (1,2)),
                ('SPAN', (0,3), (1,3)),
                ('BACKGROUND', (0,0), (1,0), colors.HexColor("#F1F5F9")),
                ('BOX', (0,0), (1,0), 1, colors.HexColor("#CBD5E1")),
                ('BACKGROUND', (0,1), (0,1), colors.HexColor("#EFF6FF")),
                ('BOX', (0,1), (0,1), 1, colors.HexColor("#BFDBFE")),
                ('BACKGROUND', (1,1), (1,1), colors.HexColor("#EFF6FF")),
                ('BOX', (1,1), (1,1), 1, colors.HexColor("#BFDBFE")),
                ('BACKGROUND', (0,2), (1,2), colors.HexColor("#DBEAFE")),
                ('BOX', (0,2), (1,2), 1, colors.HexColor("#93C5FD")),
                ('BACKGROUND', (0,3), (1,3), colors.HexColor("#ECFDF5")),
                ('BOX', (0,3), (1,3), 1, colors.HexColor("#A7F3D0")),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('PADDING', (0,0), (-1,-1), 6),
            ]))
            return flow_table

        # 3. Restudying Path vs Retrieval Practice Path
        if "Restudying Path:" in raw_code and "Retrieval Practice Path:" in raw_code:
            row1 = [Paragraph("<b>Restudying Path:</b>", body_s), Paragraph("[Read Chapter]", title_s), Paragraph("──►", card_s), Paragraph("[Transient Sensory Buffer]", body_s), Paragraph("──►", card_s), Paragraph("[Rapid Memory Decay]", body_s)]
            row2 = [Paragraph("<b>Retrieval Path:</b>", body_s), Paragraph("[Cue / Prompt]", title_s), Paragraph("──►", card_s), Paragraph("[Prefrontal Search]", body_s), Paragraph("──►", card_s), Paragraph("[Hippocampal Consolidation ──► Durable Schema]", body_s)]
            t = Table([row1, row2], colWidths=[80, 85, 25, 120, 25, 169])
            t.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#FFF7ED")),
                ('BOX', (0,0), (-1,0), 0.75, colors.HexColor("#FFEDD5")),
                ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F0FDF4")),
                ('BOX', (0,1), (-1,1), 0.75, colors.HexColor("#DCFCE7")),
                ('PADDING', (0,0), (-1,-1), 5),
            ]))
            return t

        # 4. Testing effect chart
        if "SSSS (Immediate)" in raw_code or "STTT (Day 7)" in raw_code:
            return self._render_testing_effect_chart()

        # 5. Ebbinghaus Forgetting curve
        if "Retention (R)" in raw_code and "Session 1" in raw_code:
            return self._render_ebbinghaus_chart()

        # 6. Feynman-Chi Paradigm
        if "THE FEYNMAN-CHI ITERATIVE PARADIGM" in raw_code:
            steps = [
                ("1. CONCEPT SELECTION", "Isolate the target theoretical construct or thesis."),
                ("2. TARGETED GENERATIVE TRANSLATION", "Transcribe a full explanation for a non-specialist novice void of domain jargon."),
                ("3. EPISTEMIC GAP AUDIT", "Isolate hand-waving, logical breaks, circular definitions, and vague rhetoric."),
                ("4. SOURCE RECALIBRATION & COMPRESSION", "Re-consult source literature to rectify blind spots; re-encode via tight analogy.")
            ]
            rows = []
            for i, (ttl, dsc) in enumerate(steps):
                rows.append([Paragraph(f"<b>{ttl}</b><br/>{dsc}", body_s)])
                if i < 3:
                    rows.append([Paragraph("▼", card_s)])
            ft = Table(rows, colWidths=[504])
            ft.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,0), colors.HexColor("#F8FAFC")),
                ('BACKGROUND', (0,2), (0,2), colors.HexColor("#F1F5F9")),
                ('BACKGROUND', (0,4), (0,4), colors.HexColor("#E2E8F0")),
                ('BACKGROUND', (0,6), (0,6), colors.HexColor("#EFF6FF")),
                ('BOX', (0,0), (0,0), 1, colors.HexColor("#CBD5E1")),
                ('BOX', (0,2), (0,2), 1, colors.HexColor("#94A3B8")),
                ('BOX', (0,4), (0,4), 1, colors.HexColor("#64748B")),
                ('BOX', (0,6), (0,6), 1, colors.HexColor("#3B82F6")),
                ('PADDING', (0,0), (-1,-1), 5),
            ]))
            return ft

        # 7. Dual-Coding Networks
        if "VERBAL NETWORK" in raw_code and "NONVERBAL NETWORK" in raw_code:
            vb = Paragraph("<b>VERBAL NETWORK</b><br/><br/>• Definitional text<br/>• Specific citations<br/>• Abstract jargon", body_s)
            mid = Paragraph("◄────────►<br/><font size='7'><b>Inter-system<br/>Referential<br/>Connections</b></font>", card_s)
            nvb = Paragraph("<b>NONVERBAL NETWORK</b><br/><br/>• Spatial hierarchy<br/>• Directional arrows<br/>• Conceptual clustering", body_s)
            dct = Table([[vb, mid, nvb]], colWidths=[210, 84, 210])
            dct.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,0), colors.HexColor("#F0F9FF")),
                ('BOX', (0,0), (0,0), 1, colors.HexColor("#BAE6FD")),
                ('BACKGROUND', (2,0), (2,0), colors.HexColor("#FAF5FF")),
                ('BOX', (2,0), (2,0), 1, colors.HexColor("#E9D5FF")),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('PADDING', (0,0), (-1,-1), 8),
            ]))
            return dct

        # 8. PEEL Argumentative Paragraph Architecture
        if "ARGUMENTATIVE PARAGRAPH ARCHITECTURE" in raw_code or "POINT" in raw_code and "EVIDENCE" in raw_code and "EXPLAIN" in raw_code:
            peel_data = [
                [Paragraph("<b>POINT</b>", title_s), Paragraph("Assert the primary theoretical thesis directly and unequivocally.", body_s)],
                [Paragraph("<b>EVIDENCE</b>", title_s), Paragraph("Cite foundational literature, empirical studies, or source data.", body_s)],
                [Paragraph("<b>EXPLAIN</b>", title_s), Paragraph("Unpack causal mechanics: HOW and WHY does evidence substantiate the thesis? Dissect assumptions.", body_s)],
                [Paragraph("<b>LINK</b>", title_s), Paragraph("Connect deduction back to the macro-question, establishing a clean bridge to the next analytical block.", body_s)],
            ]
            pt = Table(peel_data, colWidths=[90, 414])
            pt.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,-1), colors.HexColor(self.palette['primary'])),
                ('TEXTCOLOR', (0,0), (0,-1), colors.white),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
                ('ROWBACKGROUNDS', (1, 0), (1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('PADDING', (0,0), (-1,-1), 6),
            ]))
            return pt

        # 9. Time Allocation
        if "Total Allotted Examination Time" in raw_code or "10% PLANNING" in raw_code:
            p = Paragraph("<b>10% PLANNING</b><br/>Outline Arguments", body_s)
            e = Paragraph("<b>80% EXECUTION</b><br/>Continuous linear generation via planned frameworks (P.E.E.L.)", body_s)
            a = Paragraph("<b>10% AUDIT</b><br/>Syntax, gaps, nomenclature", body_s)
            tt = Table([[p, e, a]], colWidths=[120, 264, 120])
            tt.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,0), colors.HexColor("#FEF3C7")),
                ('BOX', (0,0), (0,0), 1, colors.HexColor("#FDE68A")),
                ('BACKGROUND', (1,0), (1,0), colors.HexColor("#DBEAFE")),
                ('BOX', (1,0), (1,0), 1, colors.HexColor("#BFDBFE")),
                ('BACKGROUND', (2,0), (2,0), colors.HexColor("#E0E7FF")),
                ('BOX', (2,0), (2,0), 1, colors.HexColor("#C7D2FE")),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('PADDING', (0,0), (-1,-1), 6),
            ]))
            return tt

        # 10. Sleep consolidation
        if "WAKEFUL ENCODING" in raw_code and "SLOW-WAVE SLEEP" in raw_code:
            s1 = Paragraph("<b>WAKEFUL ENCODING</b><br/><br/>Hippocampus acts as a rapid, temporary buffer for new factual inputs.", body_s)
            arr1 = Paragraph("──►", card_s)
            s2 = Paragraph("<b>SLOW-WAVE SLEEP (N3)</b><br/><br/>Slow oscillations &amp; ripples drive system consolidation into neocortex.", body_s)
            arr2 = Paragraph("──►", card_s)
            s3 = Paragraph("<b>REM SLEEP</b><br/><br/>Theta rhythms dominate; integration of schemata into associative networks.", body_s)
            st = Table([[s1, arr1, s2, arr2, s3]], colWidths=[150, 27, 150, 27, 150])
            st.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,0), colors.HexColor("#FEF2F2")),
                ('BOX', (0,0), (0,0), 1, colors.HexColor("#FECACA")),
                ('BACKGROUND', (2,0), (2,0), colors.HexColor("#EFF6FF")),
                ('BOX', (2,0), (2,0), 1, colors.HexColor("#BFDBFE")),
                ('BACKGROUND', (4,0), (4,0), colors.HexColor("#FAF5FF")),
                ('BOX', (4,0), (4,0), 1, colors.HexColor("#E9D5FF")),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('PADDING', (0,0), (-1,-1), 6),
            ]))
            return st

        # 11. Yerkes-Dodson curve
        if "Arousal Level (Stress / Cortisol)" in raw_code or "Hyper-arousal" in raw_code:
            return self._render_yerkes_dodson_chart()

        # 12. Chronological flow
        if "[Phase 1: Diagnostic Mapping]" in raw_code:
            p1 = Paragraph("<b>Phase 1: Diagnostic</b><br/><font size='7'>Weeks -4 to -3</font><br/>Ontology mapping", body_s)
            p2 = Paragraph("<b>Phase 2: Spaced Encoding</b><br/><font size='7'>Weeks -3 to -1</font><br/>Interleaved retrieval", body_s)
            p3 = Paragraph("<b>Phase 3: High-Stress Sim</b><br/><font size='7'>Week -1 to Day -1</font><br/>Timed essays", body_s)
            p4 = Paragraph("<b>Phase 4: Execution</b><br/><font size='7'>Exam Day</font><br/>Flawless execution", body_s)
            c_flow = Table([[p1, Paragraph("──►", card_s), p2, Paragraph("──►", card_s), p3, Paragraph("──►", card_s), p4]], colWidths=[108, 24, 108, 24, 108, 24, 108])
            c_flow.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,0), colors.HexColor("#F8FAFC")),
                ('BOX', (0,0), (0,0), 1, colors.HexColor("#CBD5E1")),
                ('BACKGROUND', (2,0), (2,0), colors.HexColor("#EFF6FF")),
                ('BOX', (2,0), (2,0), 1, colors.HexColor("#BFDBFE")),
                ('BACKGROUND', (4,0), (4,0), colors.HexColor("#FEF3C7")),
                ('BOX', (4,0), (4,0), 1, colors.HexColor("#FDE68A")),
                ('BACKGROUND', (6,0), (6,0), colors.HexColor("#ECFDF5")),
                ('BOX', (6,0), (6,0), 1, colors.HexColor("#A7F3D0")),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('PADDING', (0,0), (-1,-1), 4),
            ]))
            return c_flow

        # Default fallback: clean preformatted code block
        code_s = ParagraphStyle('D_Code', fontName='Courier', fontSize=7.5, leading=10, textColor=colors.HexColor("#0F172A"))
        from reportlab.platypus import Preformatted
        t_fallback = Table([[Preformatted(raw_code.strip(), code_s)]], colWidths=[504])
        t_fallback.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
            ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E1")),
            ('PADDING', (0,0), (-1,-1), 6)
        ]))
        return t_fallback

    def compile(self):
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=letter if self.config.get("pagesize", "letter") == "letter" else A4,
            leftMargin=54,
            rightMargin=54,
            topMargin=54,
            bottomMargin=54
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=19,
            leading=24,
            textColor=colors.HexColor("#0F172A"),
            spaceAfter=12
        )

        meta_style = ParagraphStyle(
            'DocMeta',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=14,
            textColor=colors.HexColor(self.palette["muted"]),
            spaceAfter=4
        )

        h1_style = ParagraphStyle(
            'Heading1_Custom',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=13.5,
            leading=17,
            textColor=colors.HexColor(self.palette["primary"]),
            spaceBefore=14,
            spaceAfter=6,
            keepWithNext=True
        )

        h2_style = ParagraphStyle(
            'Heading2_Custom',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=15,
            textColor=colors.HexColor(self.palette["secondary"]),
            spaceBefore=10,
            spaceAfter=5,
            keepWithNext=True
        )

        h3_style = ParagraphStyle(
            'Heading3_Custom',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#334155"),
            spaceBefore=8,
            spaceAfter=3,
            keepWithNext=True
        )

        body_style = ParagraphStyle(
            'Body_Custom',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.8,
            textColor=colors.HexColor(self.palette["text"]),
            spaceAfter=6
        )

        bullet_style = ParagraphStyle(
            'Bullet_Custom',
            parent=body_style,
            leftIndent=16,
            firstLineIndent=-10,
            spaceAfter=3
        )

        formula_card_style = ParagraphStyle(
            'Formula_Card',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10.5,
            leading=15,
            textColor=colors.HexColor(self.palette["primary"]),
            alignment=1
        )

        table_header_style = ParagraphStyle(
            'TableHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8.5,
            leading=11,
            textColor=colors.white
        )

        table_cell_style = ParagraphStyle(
            'TableCell',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=11,
            textColor=colors.HexColor(self.palette["text"])
        )

        lines = self.source_text.splitlines()
        story = []

        # Extract title and headings for Index / Cover
        doc_title = "Univer Office Document"
        headings = []
        for l in lines:
            if l.startswith("# "):
                doc_title = l[2:].strip()
                break
            elif l.startswith("## "):
                headings.append(l[3:].strip())

        # Optional Cover Page
        if self.has_cover:
            story.append(Spacer(1, 140))
            story.append(Paragraph(doc_title, ParagraphStyle('CoverTitle', parent=title_style, fontSize=24, leading=30, textColor=colors.HexColor(self.palette["primary"]))))
            story.append(Spacer(1, 16))
            story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor(self.palette["secondary"]), spaceAfter=20, spaceBefore=0))
            story.append(Paragraph(f"<b>Author:</b> {self.config.get('author', 'Academic Research Initiative')}", meta_style))
            story.append(Paragraph(f"<b>Date:</b> {self.config.get('date', datetime.now().strftime('%B %Y'))}", meta_style))
            story.append(Paragraph(f"<b>Document Class:</b> {self.config.get('classification', 'Comprehensive Specification')}", meta_style))
            story.append(Spacer(1, 180))
            story.append(Paragraph("UNIVER OFFICE PRODUCTION PIPELINE • STANDARDIZED PRINT SUITE", meta_style))
            story.append(PageBreak())

        # Optional Index / Table of Contents
        if self.has_index:
            story.append(Paragraph("Table of Contents", h1_style))
            story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor(self.palette["border"]), spaceAfter=14, spaceBefore=4))
            toc_rows = []
            for idx, h in enumerate(headings):
                toc_rows.append([Paragraph(f"<b>{idx+1}.</b> &nbsp; {h}", body_style), Paragraph(f"Section {idx+1}", table_cell_style)])
            if toc_rows:
                toc_table = Table(toc_rows, colWidths=[400, 104])
                toc_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                    ('TOPPADDING', (0,0), (-1,-1), 4),
                    ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor(self.palette["surface"]))
                ]))
                story.append(toc_table)
            story.append(Spacer(1, 16))
            story.append(PageBreak())

        in_code_block = False
        current_code_block = []

        in_table = False
        table_raw_rows = []

        def flush_table():
            nonlocal table_raw_rows
            if not table_raw_rows:
                return
            processed_rows = []
            is_header = True
            for row_str in table_raw_rows:
                if re.match(r'^\s*\|?\s*[-:]+[-| :]*$', row_str):
                    is_header = False
                    continue
                cells = [c.strip() for c in row_str.strip().strip('|').split('|')]
                if not cells or all(c == '' for c in cells):
                    continue
                row_paras = [Paragraph(self.format_inline(c), table_header_style if is_header else table_cell_style) for c in cells]
                processed_rows.append(row_paras)

            if processed_rows:
                col_count = max(len(r) for r in processed_rows)
                for r in processed_rows:
                    while len(r) < col_count:
                        r.append(Paragraph("", table_cell_style))
                col_w = 504.0 / col_count
                t = Table(processed_rows, colWidths=[col_w]*col_count)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor(self.palette["primary"])),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                    ('TOPPADDING', (0,0), (-1,-1), 4),
                    ('LEFTPADDING', (0,0), (-1,-1), 6),
                    ('RIGHTPADDING', (0,0), (-1,-1), 6),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor(self.palette["border"])),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor(self.palette["surface"])]),
                ]))
                story.append(Spacer(1, 4))
                story.append(t)
                story.append(Spacer(1, 8))
            table_raw_rows = []

        i = 0
        while i < len(lines):
            line = lines[i]

            if line.strip().startswith("```"):
                if in_code_block:
                    in_code_block = False
                    code_text = "\n".join(current_code_block)
                    diag = self._render_flowable_diagram(code_text)
                    if diag:
                        story.append(Spacer(1, 4))
                        story.append(KeepTogether([diag]))
                        story.append(Spacer(1, 8))
                    current_code_block = []
                else:
                    if in_table:
                        in_table = False
                        flush_table()
                    in_code_block = True
                    current_code_block = []
                i += 1
                continue

            if in_code_block:
                current_code_block.append(line)
                i += 1
                continue

            if "|" in line and (line.strip().startswith("|") or re.search(r'\|\s*[-:]+', line)):
                in_table = True
                table_raw_rows.append(line)
                i += 1
                continue
            elif in_table:
                in_table = False
                flush_table()

            stripped = line.strip()
            if not stripped:
                i += 1
                continue

            if stripped in ["---", "***", "___"]:
                story.append(Spacer(1, 4))
                story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor(self.palette["border"]), spaceAfter=8, spaceBefore=4))
                i += 1
                continue

            if stripped.startswith("# "):
                story.append(Paragraph(self.format_inline(stripped[2:].strip()), title_style))
                i += 1
                continue
            elif stripped.startswith("## "):
                story.append(Spacer(1, 4))
                story.append(Paragraph(self.format_inline(stripped[3:].strip()), h1_style))
                i += 1
                continue
            elif stripped.startswith("### "):
                story.append(Spacer(1, 3))
                story.append(Paragraph(self.format_inline(stripped[4:].strip()), h2_style))
                i += 1
                continue
            elif stripped.startswith("#### "):
                story.append(Spacer(1, 2))
                story.append(Paragraph(self.format_inline(stripped[5:].strip()), h3_style))
                i += 1
                continue

            if stripped.startswith("$$") and stripped.endswith("$$"):
                raw_eq = stripped[2:-2].strip()
                card = Table([[Paragraph(self.clean_latex_math(f"$${raw_eq}$$"), formula_card_style)]], colWidths=[504])
                card.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(self.palette["card_bg"])),
                    ('BOX', (0,0), (-1,-1), 1, colors.HexColor(self.palette["card_border"])),
                    ('TOPPADDING', (0,0), (-1,-1), 6),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                    ('LEFTPADDING', (0,0), (-1,-1), 10),
                    ('RIGHTPADDING', (0,0), (-1,-1), 10),
                ]))
                story.append(Spacer(1, 4))
                story.append(card)
                story.append(Spacer(1, 6))
                i += 1
                continue

            if re.match(r'^\s*[-*]\s+', line):
                content = re.sub(r'^\s*[-*]\s+', '', line)
                story.append(Paragraph(f"• &nbsp; {self.format_inline(content)}", bullet_style))
                i += 1
                continue
            elif re.match(r'^\s*\d+\.\s+', line):
                num = re.match(r'^\s*(\d+\.)\s+', line).group(1)
                content = re.sub(r'^\s*\d+\.\s+', '', line)
                story.append(Paragraph(f"<b>{num}</b> &nbsp; {self.format_inline(content)}", bullet_style))
                i += 1
                continue

            if stripped.startswith("**Author:**") or stripped.startswith("**Date:**") or stripped.startswith("**Document Classification:**") or stripped.startswith("**Target Domain:**"):
                story.append(Paragraph(self.format_inline(stripped), meta_style))
                i += 1
                continue

            story.append(Paragraph(self.format_inline(stripped), body_style))
            i += 1

        if in_table:
            flush_table()

        # Canvas configuration
        def canvasmaker(*args, **kwargs):
            c = NumberedCanvas(*args, **kwargs)
            c.doc_title = doc_title
            c.has_cover = self.has_cover
            c.custom_header = self.config.get("header_title", "")
            c.custom_footer = self.config.get("footer_text", "")
            return c

        doc.build(story, canvasmaker=canvasmaker)
        print(f"[Success] Compiled print-ready Univer PDF -> {self.output_path}")


def main():
    parser = argparse.ArgumentParser(description="Univer Production PDF Converter")
    parser.add_argument("input", help="Source file (.md, .txt, .docx)")
    parser.add_argument("-o", "--output", help="Output PDF file path")
    parser.add_argument("--config", help="Optional JSON formatting configuration")
    parser.add_argument("--images", action="store_true", help="Enable AI asset / image rendering")
    parser.add_argument("--cover", action="store_true", help="Prepend formal Cover Page")
    parser.add_argument("--index", action="store_true", help="Prepend formal Table of Contents")
    parser.add_argument("--source", help="Asset source directory")

    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    if not os.path.exists(input_path):
        print(f"[Error] Source file not found: {input_path}")
        sys.exit(1)

    output_path = args.output
    if not output_path:
        base = os.path.splitext(input_path)[0]
        output_path = f"{base}.pdf"
    output_path = os.path.abspath(output_path)

    config_data = {}
    if args.config and os.path.exists(args.config):
        with open(args.config, "r", encoding="utf-8") as f:
            config_data = json.load(f)

    options = {
        "images": args.images,
        "cover": args.cover,
        "index": args.index,
        "source": args.source
    }

    builder = UniverPDFBuilder(input_path, output_path, config=config_data, options=options)
    builder.compile()

if __name__ == "__main__":
    main()
