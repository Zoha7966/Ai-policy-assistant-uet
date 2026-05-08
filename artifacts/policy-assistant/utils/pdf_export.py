import io
import re
from fpdf import FPDF
from datetime import datetime


class PolicyPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(30, 64, 175)
        self.cell(0, 10, "AI Policy Analysis & Comparison Assistant", align="L")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, datetime.now().strftime("%B %d, %Y"), align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()} | UET Taxila — AI Course Assignment", align="C")


def _strip_markdown(text: str) -> str:
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    text = re.sub(r"#{1,6}\s*", "", text)
    return text


def generate_pdf(title: str, task_label: str, content: str, policy_input: str = "") -> bytes:
    pdf = PolicyPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.set_margins(15, 15, 15)

    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(15, 23, 42)
    pdf.multi_cell(0, 10, title, align="L")
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 8, f"Analysis Type: {task_label}", new_x="LMARGIN", new_y="NEXT")

    if policy_input and len(policy_input) < 200:
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(120, 120, 120)
        pdf.multi_cell(0, 6, f"Input: {policy_input[:150]}{'...' if len(policy_input) > 150 else ''}")

    pdf.ln(4)
    pdf.set_draw_color(220, 220, 220)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(5)

    lines = content.split("\n")

    for line in lines:
        stripped = line.strip()

        if not stripped:
            pdf.ln(2)
            continue

        if stripped.startswith("## "):
            pdf.ln(3)
            heading = _strip_markdown(stripped[3:])
            pdf.set_font("Helvetica", "B", 13)
            pdf.set_text_color(30, 64, 175)
            pdf.set_fill_color(239, 246, 255)
            pdf.multi_cell(0, 8, heading, fill=True)
            pdf.ln(1)

        elif stripped.startswith("### "):
            pdf.ln(2)
            heading = _strip_markdown(stripped[4:])
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(51, 65, 85)
            pdf.multi_cell(0, 7, heading)
            pdf.ln(1)

        elif stripped.startswith("- ") or stripped.startswith("* "):
            bullet_text = _strip_markdown(stripped[2:])
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(30, 41, 59)
            x = pdf.get_x()
            pdf.set_x(20)
            pdf.cell(5, 6, chr(149), new_x="RIGHT")
            pdf.multi_cell(0, 6, bullet_text)

        elif stripped.startswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if not cells:
                continue
            col_width = 175 // max(len(cells), 1)
            is_separator = all(set(c) <= set("-: ") for c in cells)
            if is_separator:
                continue
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(30, 41, 59)
            for i, cell in enumerate(cells):
                cell_text = _strip_markdown(cell)
                is_header_row = all(c.isupper() or len(c) <= 20 for c in cells)
                if i == 0 and len(cells) > 1:
                    pdf.set_font("Helvetica", "B", 9)
                    pdf.set_fill_color(241, 245, 249)
                    pdf.cell(col_width, 7, cell_text[:30], border=1, fill=True)
                    pdf.set_font("Helvetica", "", 9)
                else:
                    pdf.cell(col_width, 7, cell_text[:30], border=1)
            pdf.ln()

        else:
            clean = _strip_markdown(stripped)
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(30, 41, 59)
            pdf.multi_cell(0, 6, clean)

    buf = io.BytesIO()
    pdf.output(buf)
    return buf.getvalue()
