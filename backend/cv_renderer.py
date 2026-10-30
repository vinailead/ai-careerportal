"""
1:1 Exact-Format CV Renderer (PDF & Google Docs .docx) for Vinoth Nataraj.
Replicates the exact typography (Calibri / Calibri-Bold), coordinates, horizontal
rules, bullet hanging indents, and embedded hyperlinks of Vinoth_Nataraj_Senior_Manager.pdf.
"""

import os
from typing import Dict, Any, List, Tuple
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# Register genuine Microsoft Calibri fonts installed on macOS
CALIBRI_REGULAR_PATH = "/Applications/Microsoft Word.app/Contents/Resources/DFonts/Calibri.ttf"
CALIBRI_BOLD_PATH = "/Applications/Microsoft Word.app/Contents/Resources/DFonts/Calibrib.ttf"

FONT_REG = "Helvetica"
FONT_BOLD = "Helvetica-Bold"

if os.path.exists(CALIBRI_REGULAR_PATH) and os.path.exists(CALIBRI_BOLD_PATH):
    try:
        pdfmetrics.registerFont(TTFont("Calibri", CALIBRI_REGULAR_PATH))
        pdfmetrics.registerFont(TTFont("Calibri-Bold", CALIBRI_BOLD_PATH))
        FONT_REG = "Calibri"
        FONT_BOLD = "Calibri-Bold"
    except Exception:
        pass

PAGE_W = 595.32
PAGE_H = 841.92
LEFT_MARGIN = 72.0
BULLET_TEXT_X = 86.2
RIGHT_MARGIN = 523.5
RULE_LEFT = 69.0
RULE_RIGHT = 526.5
MAX_TEXT_W = RIGHT_MARGIN - LEFT_MARGIN
MAX_BULLET_W = RIGHT_MARGIN - BULLET_TEXT_X


def _wrap_PlainText(text: str, font_name: str, font_size: float, max_width: float) -> List[str]:
    words = text.split()
    lines: List[str] = []
    current = ""
    for w in words:
        cand = f"{current} {w}".strip() if current else w
        if pdfmetrics.stringWidth(cand, font_name, font_size) <= max_width:
            current = cand
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def _draw_mixed_bullet(
    c: canvas.Canvas,
    y: float,
    bold_prefix: str,
    regular_text: str,
    font_size: float = 10.5,
    line_h: float = 12.8,
) -> float:
    """
    Draws a bullet point at x=72.0 and hanging-indented text at x=86.2,
    where `bold_prefix` is rendered in Calibri-Bold followed immediately by `regular_text` in Calibri.
    Returns the new y coordinate (top-down coordinate system converted inside helper).
    """
    # Convert top-down y to ReportLab bottom-up y
    rl_y = PAGE_H - y
    c.setFont(FONT_REG, font_size)
    c.drawString(LEFT_MARGIN, rl_y, "•")

    # Tokenize words with font tags: (word, font_name)
    tokens: List[Tuple[str, str]] = []
    if bold_prefix:
        for w in bold_prefix.split():
            tokens.append((w, FONT_BOLD))
    for w in regular_text.split():
        tokens.append((w, FONT_REG))

    # Build wrapped lines of (word, font_name)
    lines: List[List[Tuple[str, str]]] = []
    cur_line: List[Tuple[str, str]] = []
    cur_w = 0.0
    space_w = pdfmetrics.stringWidth(" ", FONT_REG, font_size)

    for word, fn in tokens:
        w_width = pdfmetrics.stringWidth(word, fn, font_size)
        needed = w_width if not cur_line else (cur_w + space_w + w_width)
        if needed <= MAX_BULLET_W:
            cur_line.append((word, fn))
            cur_w = needed
        else:
            lines.append(cur_line)
            cur_line = [(word, fn)]
            cur_w = w_width
    if cur_line:
        lines.append(cur_line)

    for idx, line_tokens in enumerate(lines):
        line_rl_y = PAGE_H - (y + idx * line_h)
        cur_x = BULLET_TEXT_X
        for word, fn in line_tokens:
            c.setFont(fn, font_size)
            c.drawString(cur_x, line_rl_y, word)
            cur_x += pdfmetrics.stringWidth(word, fn, font_size) + space_w

    return y + len(lines) * line_h


def _draw_section_header(c: canvas.Canvas, y: float, title: str, font_size: float = 10.6) -> float:
    """Draws an uppercase/bold section header and the full-width 0.71pt black horizontal line below it."""
    rl_y = PAGE_H - y
    c.setFont(FONT_BOLD, font_size)
    c.drawString(LEFT_MARGIN, rl_y, title)
    line_y = y + 4.5
    rl_line_y = PAGE_H - line_y
    c.setLineWidth(0.71)
    c.setStrokeColorRGB(0, 0, 0)
    c.line(RULE_LEFT, rl_line_y, RULE_RIGHT, rl_line_y)
    return line_y + 13.5


def render_cv_pdf(cv_data: Dict[str, Any], output_path: str) -> str:
    """
    Renders `cv_data` to `output_path` as an exact 2-page visual match of
    Vinoth_Nataraj_Senior_Manager.pdf with Independent AI Product Development
    placed under PROFESSIONAL WORK EXPERIENCE.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    c = canvas.Canvas(output_path, pagesize=(PAGE_W, PAGE_H))
    header = cv_data["header"]
    c.setTitle(f"{header['name']} - {cv_data.get('name', 'CV')}")
    c.setAuthor(header["name"])

    # ================= PAGE 1 =================
    # 1. Centered Name (16pt Calibri-Bold at y=68)
    y = 66.0
    c.setFont(FONT_BOLD, 16.0)
    c.drawCentredString(PAGE_W / 2.0, PAGE_H - y, header["name"])

    # 2. Centered Contact Line (9.5pt Calibri-Bold at y=83.5) with clickable links
    y = 83.0
    contact_parts = [
        (f"{header['location']} | ", None),
        (header["email"], f"mailto:{header['email']}"),
        (f" | {header['phone']} | ", None),
        (header["linkedin_label"], header["linkedin_url"]),
        (" | ", None),
        (header["github_label"], header["github_url"]),
        (" |", None),
    ]
    c.setFont(FONT_BOLD, 9.5)
    total_contact_w = sum(pdfmetrics.stringWidth(txt, FONT_BOLD, 9.5) for txt, _ in contact_parts)
    cur_x = (PAGE_W - total_contact_w) / 2.0
    rl_contact_y = PAGE_H - y
    for txt, url in contact_parts:
        w = pdfmetrics.stringWidth(txt, FONT_BOLD, 9.5)
        c.drawString(cur_x, rl_contact_y, txt)
        if url:
            c.linkURL(url, (cur_x, rl_contact_y - 2, cur_x + w, rl_contact_y + 9), relative=0)
        cur_x += w

    # Full-width horizontal line below contact header (y=90.5)
    c.setLineWidth(0.71)
    c.line(RULE_LEFT, PAGE_H - 90.0, RULE_RIGHT, PAGE_H - 90.0)

    # 3. Executive Summary (10.5pt Calibri)
    y = 104.5
    summary_lines = _wrap_PlainText(cv_data["summary"], FONT_REG, 10.5, MAX_TEXT_W)
    c.setFont(FONT_REG, 10.5)
    for line in summary_lines:
        c.drawString(LEFT_MARGIN, PAGE_H - y, line)
        y += 13.0

    # 4. CORE COMPETENCIES
    y += 6.0
    y = _draw_section_header(c, y, cv_data["competencies_header"], font_size=10.6)
    for comp in cv_data["competencies"]:
        y = _draw_mixed_bullet(c, y, comp["label"], comp["text"], font_size=10.4, line_h=12.6)
        y += 1.8

    # 5. PROFESSIONAL WORK EXPERIENCE (Page 1: Independent AI Product Development + VERIZON)
    y += 6.0
    y = _draw_section_header(c, y, "PROFESSIONAL WORK EXPERIENCE", font_size=11.0)

    # Role 1: Independent AI Product Development (Jan 2026- Present)
    ind_role = cv_data["experience"][0]
    c.setFont(FONT_BOLD, 10.6)
    c.drawString(LEFT_MARGIN, PAGE_H - y, ind_role["company"])
    y += 13.5
    c.setFont(FONT_BOLD, 10.6)
    c.drawString(LEFT_MARGIN, PAGE_H - y, ind_role["title"])
    # Add clickable link for github.com/vinailead
    title_w = pdfmetrics.stringWidth(ind_role["title"], FONT_BOLD, 10.6)
    c.linkURL("https://github.com/vinailead", (LEFT_MARGIN, PAGE_H - y - 2, LEFT_MARGIN + title_w, PAGE_H - y + 9), relative=0)
    c.drawRightString(518.0, PAGE_H - y, ind_role["dates"])
    y += 13.5
    for b in ind_role["bullets"]:
        y = _draw_mixed_bullet(c, y, "", b, font_size=10.4, line_h=12.5)
        y += 1.6

    # Role 2: VERIZON | Chennai (Aug 2022- Dec 2025)
    y += 5.5
    vz_role = cv_data["experience"][1]
    c.setFont(FONT_BOLD, 11.0)
    c.drawString(LEFT_MARGIN, PAGE_H - y, vz_role["company"])
    y += 14.0
    c.setFont(FONT_BOLD, 10.8)
    c.drawString(LEFT_MARGIN, PAGE_H - y, vz_role["title"])
    c.setFont(FONT_BOLD, 10.6)
    c.drawRightString(518.0, PAGE_H - y, vz_role["dates"])
    y += 14.0
    for b in vz_role["bullets"]:
        y = _draw_mixed_bullet(c, y, "", b, font_size=10.35, line_h=12.4)
        y += 2.2

    c.showPage()

    # ================= PAGE 2 =================
    y = 66.0
    y = _draw_section_header(c, y, "PROFESSIONAL WORK EXPERIENCE", font_size=10.8)

    # Role 3: CCLYTICX SERVICES PVT LTD | Chennai
    cc_role = cv_data["experience"][2]
    c.setFont(FONT_BOLD, 10.6)
    c.drawString(LEFT_MARGIN, PAGE_H - y, cc_role["company"])
    y += 13.5

    for idx, sub in enumerate(cc_role["sub_roles"]):
        if idx > 0:
            y += 5.0
        c.setFont(FONT_BOLD, 10.6)
        c.drawString(LEFT_MARGIN, PAGE_H - y, sub["title"])
        c.drawRightString(519.0, PAGE_H - y, sub["dates"])
        y += 14.0
        for b in sub["bullets"]:
            y = _draw_mixed_bullet(c, y, "", b, font_size=10.5, line_h=12.8)
            y += 3.0

    # EDUCATION
    y += 10.0
    y = _draw_section_header(c, y, "EDUCATION", font_size=10.6)
    for edu in cv_data["education"]:
        rl_y = PAGE_H - y
        c.setFont(FONT_REG, 10.6)
        c.drawString(LEFT_MARGIN, rl_y, "•")
        c.setFont(FONT_BOLD, 10.6)
        c.drawString(BULLET_TEXT_X, rl_y, edu["degree"])
        c.setFont(FONT_REG, 10.6)
        c.drawRightString(519.5, rl_y, edu["dates"])
        y += 13.5
        c.setFont(FONT_REG, 10.6)
        c.drawString(BULLET_TEXT_X, PAGE_H - y, edu["institution"])
        y += 15.0

    # TECHNICAL SKILLS & TOOLS
    y += 6.0
    y = _draw_section_header(c, y, "TECHNICAL SKILLS & TOOLS", font_size=10.6)
    for sk in cv_data["skills"]:
        y = _draw_mixed_bullet(c, y, sk["label"], sk["text"], font_size=10.5, line_h=13.0)
        y += 2.0

    # CERTIFICATIONS & COURSES
    y += 8.0
    y = _draw_section_header(c, y, "CERTIFICATIONS & COURSES", font_size=10.6)
    for cert in cv_data["certifications"]:
        y = _draw_mixed_bullet(c, y, "", cert, font_size=10.5, line_h=13.0)
        y += 2.0

    c.save()
    return output_path


# ============================================================================
# GOOGLE DOCS / WORD (.DOCX) 1:1 RENDERER
# ============================================================================

def _add_bottom_border(paragraph):
    """Adds a full-width solid black bottom border to a Word/Google Docs paragraph."""
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "2")
    bottom.set(qn("w:color"), "000000")
    pBdr.append(bottom)
    pPr.append(pBdr)


def _add_hyperlink(paragraph, text: str, url: str, bold: bool = True, size_pt: float = 9.5):
    """Adds a clickable hyperlink inside a python-docx paragraph."""
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)

    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    rFonts = OxmlElement("w:rFonts")
    rFonts.set(qn("w:ascii"), "Calibri")
    rFonts.set(qn("w:hAnsi"), "Calibri")
    rPr.append(rFonts)
    if bold:
        b = OxmlElement("w:b")
        rPr.append(b)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int(size_pt * 2)))
    rPr.append(sz)
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "000000")
    rPr.append(color)

    new_run.append(rPr)
    t = OxmlElement("w:t")
    t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def render_cv_docx(cv_data: Dict[str, Any], output_path: str) -> str:
    """
    Renders `cv_data` into a Google Docs / Microsoft Word (.docx) document
    matching the exact visual structure, typography, borders, and layout of
    Vinoth_Nataraj_Senior_Manager.pdf.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc = docx.Document()

    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10.5)
    style.font.color.rgb = RGBColor(0, 0, 0)

    header = cv_data["header"]

    # 1. Name
    p_name = doc.add_paragraph()
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_name.paragraph_format.space_before = Pt(0)
    p_name.paragraph_format.space_after = Pt(2)
    r_name = p_name.add_run(header["name"])
    r_name.bold = True
    r_name.font.name = "Calibri"
    r_name.font.size = Pt(16)

    # 2. Contact bar + bottom border
    p_contact = doc.add_paragraph()
    p_contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_contact.paragraph_format.space_before = Pt(0)
    p_contact.paragraph_format.space_after = Pt(8)
    _add_bottom_border(p_contact)

    def add_contact_run(txt: str):
        r = p_contact.add_run(txt)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)

    add_contact_run(f"{header['location']} | ")
    _add_hyperlink(p_contact, header["email"], f"mailto:{header['email']}")
    add_contact_run(f" | {header['phone']} | ")
    _add_hyperlink(p_contact, header["linkedin_label"], header["linkedin_url"])
    add_contact_run(" | ")
    _add_hyperlink(p_contact, header["github_label"], header["github_url"])
    add_contact_run(" |")

    # 3. Summary
    p_sum = doc.add_paragraph()
    p_sum.paragraph_format.space_before = Pt(4)
    p_sum.paragraph_format.space_after = Pt(8)
    r_sum = p_sum.add_run(cv_data["summary"])
    r_sum.font.name = "Calibri"
    r_sum.font.size = Pt(10.5)

    def add_section_heading(title: str):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(6)
        _add_bottom_border(p)
        r = p.add_run(title)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)

    def add_bullet_line(bold_prefix: str, text: str):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.2)
        p.paragraph_format.first_line_indent = Inches(-0.2)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2.5)
        rb = p.add_run("•\t")
        rb.font.name = "Calibri"
        rb.font.size = Pt(10.5)
        if bold_prefix:
            rp = p.add_run(f"{bold_prefix} ")
            rp.bold = True
            rp.font.name = "Calibri"
            rp.font.size = Pt(10.5)
        rt = p.add_run(text)
        rt.font.name = "Calibri"
        rt.font.size = Pt(10.5)

    def add_role_title_dates(title: str, dates: str, bold_dates: bool = True):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.tab_stops.add_tab_stop(Inches(6.27), WD_TAB_ALIGNMENT.RIGHT)
        rt = p.add_run(title)
        rt.bold = True
        rt.font.name = "Calibri"
        rt.font.size = Pt(10.5)
        rd = p.add_run(f"\t{dates}")
        rd.bold = bold_dates
        rd.font.name = "Calibri"
        rd.font.size = Pt(10.5)

    # 4. CORE COMPETENCIES
    add_section_heading(cv_data["competencies_header"])
    for comp in cv_data["competencies"]:
        add_bullet_line(comp["label"], comp["text"])

    # 5. PROFESSIONAL WORK EXPERIENCE
    add_section_heading("PROFESSIONAL WORK EXPERIENCE")

    # Independent AI Product Development
    ind_role = cv_data["experience"][0]
    p_ind_co = doc.add_paragraph()
    p_ind_co.paragraph_format.space_before = Pt(2)
    p_ind_co.paragraph_format.space_after = Pt(1)
    r_ind_co = p_ind_co.add_run(ind_role["company"])
    r_ind_co.bold = True
    r_ind_co.font.size = Pt(10.5)
    add_role_title_dates(ind_role["title"], ind_role["dates"])
    for b in ind_role["bullets"]:
        add_bullet_line("", b)

    # Verizon
    vz_role = cv_data["experience"][1]
    p_vz_co = doc.add_paragraph()
    p_vz_co.paragraph_format.space_before = Pt(6)
    p_vz_co.paragraph_format.space_after = Pt(1)
    r_vz_co = p_vz_co.add_run(vz_role["company"])
    r_vz_co.bold = True
    r_vz_co.font.size = Pt(11)
    add_role_title_dates(vz_role["title"], vz_role["dates"])
    for b in vz_role["bullets"]:
        add_bullet_line("", b)

    # CCLYTICX
    cc_role = cv_data["experience"][2]
    p_cc_co = doc.add_paragraph()
    p_cc_co.paragraph_format.space_before = Pt(6)
    p_cc_co.paragraph_format.space_after = Pt(1)
    r_cc_co = p_cc_co.add_run(cc_role["company"])
    r_cc_co.bold = True
    r_cc_co.font.size = Pt(10.5)
    for sub in cc_role["sub_roles"]:
        add_role_title_dates(sub["title"], sub["dates"])
        for b in sub["bullets"]:
            add_bullet_line("", b)

    # 6. EDUCATION
    add_section_heading("EDUCATION")
    for edu in cv_data["education"]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.2)
        p.paragraph_format.first_line_indent = Inches(-0.2)
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.tab_stops.add_tab_stop(Inches(6.27), WD_TAB_ALIGNMENT.RIGHT)
        rb = p.add_run("•\t")
        rb.font.size = Pt(10.5)
        rdeg = p.add_run(edu["degree"])
        rdeg.bold = True
        rdeg.font.size = Pt(10.5)
        rdat = p.add_run(f"\t{edu['dates']}")
        rdat.font.size = Pt(10.5)

        p_inst = doc.add_paragraph()
        p_inst.paragraph_format.left_indent = Inches(0.2)
        p_inst.paragraph_format.space_before = Pt(0)
        p_inst.paragraph_format.space_after = Pt(4)
        rinst = p_inst.add_run(edu["institution"])
        rinst.font.size = Pt(10.5)

    # 7. TECHNICAL SKILLS & TOOLS
    add_section_heading("TECHNICAL SKILLS & TOOLS")
    for sk in cv_data["skills"]:
        add_bullet_line(sk["label"], sk["text"])

    # 8. CERTIFICATIONS & COURSES
    add_section_heading("CERTIFICATIONS & COURSES")
    for cert in cv_data["certifications"]:
        add_bullet_line("", cert)

    doc.save(output_path)
    return output_path
