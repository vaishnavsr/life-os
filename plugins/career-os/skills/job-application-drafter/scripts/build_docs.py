#!/usr/bin/env python3
"""Career OS document builder.

Builds a resume and/or cover letter .docx from a JSON content file, using a
clean, ATS-friendly layout. Convert to PDF afterwards with LibreOffice.

Usage:
  python3 build_docs.py content.json OUT_DIR

content.json:
{
  "style": {"font": "Calibri", "accent_hex": "1F3864", "page_size": "A4", "base_pt": 10},
  "files": {"resume": "2026-Resume-Acme-Strategy_Mgr-JDS", "cover_letter": "2026-Cover_Letter-Acme-Strategy_Mgr-JDS"},
  "owner": {"name": "Jane Doe Smith", "contact": ["Melbourne, Australia", "+61 400 000 000",
            {"text": "jane@example.com", "url": "mailto:jane@example.com"},
            {"text": "linkedin.com/in/jane", "url": "https://linkedin.com/in/jane"}]},
  "resume": {
    "summary": "Paragraph …",
    "selected_impact": ["…", "…"],
    "capabilities": ["Corporate Strategy", "Commercial Modelling"],
    "roles": [{"title": "Senior Manager, Strategy", "org": "Acme", "location": "Australia",
               "dates": "2023 – 2025", "intro": "One line on scope.", "bullets": ["…"]}],
    "early_career": "Analyst, Foo; Engineer, Bar",
    "education": ["MBA, Some University", "Bachelor of …"],
    "extra_sections": [{"heading": "Certifications", "bullets": ["…"]}]
  },
  "cover_letter": {
    "date": "10 Nov 2026",
    "recipient": ["Hiring Manager", "Acme", "1 Example St", "Melbourne VIC 3000"],
    "subject": "Application for Strategy Manager",
    "salutation": "Dear Hiring Manager,",
    "paragraphs": ["…", "…"],
    "closing": "Warm regards,",
    "signature": "Jane"
  }
}
Any section may be omitted. Section headings can be renamed via resume.headings
(keys: summary, selected_impact, capabilities, experience, early_career, education).
"""
import json
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT  # noqa: F401  (kept for users extending the script)
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Mm, Inches

PAGE = {"A4": (Mm(210), Mm(297)), "LETTER": (Inches(8.5), Inches(11))}
DEFAULT_HEADINGS = {
    "summary": "SUMMARY",
    "selected_impact": "Selected impact:",
    "capabilities": "CORE CAPABILITIES",
    "experience": "PROFESSIONAL WORK HISTORY",
    "early_career": "EARLY CAREER",
    "education": "EDUCATION",
}


def hex_rgb(h):
    h = h.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def setup_doc(style):
    doc = Document()
    w, h = PAGE.get(style.get("page_size", "A4").upper(), PAGE["A4"])
    for s in doc.sections:
        s.page_width, s.page_height = w, h
        s.left_margin = s.right_margin = Mm(16)
        s.top_margin = Mm(14)
        s.bottom_margin = Mm(14)
        s.footer_distance = Mm(7)
    normal = doc.styles["Normal"]
    normal.font.name = style.get("font", "Calibri")
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), style.get("font", "Calibri"))
    normal.font.size = Pt(style.get("base_pt", 10))
    normal.paragraph_format.space_after = Pt(2)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.line_spacing = 1.05
    lb = doc.styles["List Bullet"]
    lb.font.name = style.get("font", "Calibri")
    lb.font.size = Pt(style.get("base_pt", 10))
    lb.paragraph_format.space_after = Pt(1)
    return doc


def text_width(doc):
    s = doc.sections[0]
    return s.page_width - s.left_margin - s.right_margin


def shade(paragraph, fill_hex):
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    pPr.append(shd)


def add_hyperlink(paragraph, text, url, color_hex):
    part = paragraph.part
    r_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    col = OxmlElement("w:color")
    col.set(qn("w:val"), color_hex)
    rPr.append(col)
    run.append(rPr)
    t = OxmlElement("w:t")
    t.text = text
    t.set(qn("xml:space"), "preserve")
    run.append(t)
    link.append(run)
    paragraph._p.append(link)


def add_field(run, instr):
    for kind, val in (("begin", None), ("instr", instr), ("separate", None), ("text", "1"), ("end", None)):
        if kind == "instr":
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = f" {val} "
        elif kind == "text":
            el = OxmlElement("w:t")
            el.text = val
        else:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
        run._r.append(el)


def footer(doc, name, with_pages=True):
    f = doc.sections[0].footer
    p = f.paragraphs[0]
    p.style = doc.styles["Normal"]  # the built-in Footer style carries centre/right tabs that misplace the page number
    p.paragraph_format.tab_stops.add_tab_stop(text_width(doc), WD_TAB_ALIGNMENT.RIGHT)
    r = p.add_run(name.upper())
    r.font.size = Pt(8)
    if with_pages:
        p.add_run("\t").font.size = Pt(8)
        a = p.add_run(); a.font.size = Pt(8); add_field(a, "PAGE")
        p.add_run("/").font.size = Pt(8)
        b = p.add_run(); b.font.size = Pt(8); add_field(b, "NUMPAGES")


def header_block(doc, owner, style):
    accent = style.get("accent_hex", "1F3864")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(owner["name"].upper())
    r.bold = True
    r.font.size = Pt(18)
    r.font.color.rgb = hex_rgb(accent)
    p.paragraph_format.space_after = Pt(2)
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for i, item in enumerate(owner.get("contact", [])):
        if i:
            c.add_run("  |  ")
        if isinstance(item, dict) and item.get("url"):
            add_hyperlink(c, item["text"], item["url"], accent)
        else:
            c.add_run(item["text"] if isinstance(item, dict) else item)
    c.paragraph_format.space_after = Pt(6)


def section_heading(doc, text, style):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(style.get("base_pt", 10) + 1.5)
    r.font.color.rgb = hex_rgb(style.get("accent_hex", "1F3864"))
    shade(p, "D9D9D9")
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    return p


def bullets(doc, items):
    for it in items:
        p = doc.add_paragraph(style="List Bullet")
        p.add_run(it)


def role_block(doc, role, style):
    p = doc.add_paragraph()
    p.paragraph_format.tab_stops.add_tab_stop(text_width(doc), WD_TAB_ALIGNMENT.RIGHT)
    shade(p, "EFEFEF")
    t = p.add_run(role["title"])
    t.bold = True
    org = ", ".join(x for x in [role.get("org"), role.get("location")] if x)
    if org:
        p.add_run(", " + org)
    if role.get("dates"):
        p.add_run("\t" + role["dates"])
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.keep_with_next = True
    if role.get("intro"):
        i = doc.add_paragraph(role["intro"])
        i.paragraph_format.keep_with_next = bool(role.get("bullets"))
    bullets(doc, role.get("bullets", []))


def build_resume(c, out):
    style, owner, rs = c.get("style", {}), c["owner"], c["resume"]
    H = {**DEFAULT_HEADINGS, **rs.get("headings", {})}
    doc = setup_doc(style)
    footer(doc, owner["name"])
    header_block(doc, owner, style)
    if rs.get("summary"):
        section_heading(doc, H["summary"], style)
        doc.add_paragraph(rs["summary"])
    if rs.get("selected_impact"):
        p = doc.add_paragraph()
        p.add_run(H["selected_impact"]).bold = True
        p.paragraph_format.space_before = Pt(4)
        bullets(doc, rs["selected_impact"])
    if rs.get("capabilities"):
        section_heading(doc, H["capabilities"], style)
        doc.add_paragraph(" | ".join(rs["capabilities"]))
    if rs.get("roles"):
        section_heading(doc, H["experience"], style)
        for role in rs["roles"]:
            role_block(doc, role, style)
    if rs.get("early_career"):
        section_heading(doc, H["early_career"], style)
        doc.add_paragraph(rs["early_career"])  # plain, no bold, no years by default
    for extra in rs.get("extra_sections", []):
        section_heading(doc, extra["heading"], style)
        if extra.get("text"):
            doc.add_paragraph(extra["text"])
        bullets(doc, extra.get("bullets", []))
    if rs.get("education"):
        section_heading(doc, H["education"], style)
        bullets(doc, rs["education"])
    path = Path(out) / (c.get("files", {}).get("resume", "resume") + ".docx")
    doc.save(path)
    return path


def build_cover_letter(c, out):
    style, owner, cl = c.get("style", {}), c["owner"], c["cover_letter"]
    doc = setup_doc(style)
    footer(doc, owner["name"], with_pages=False)
    header_block(doc, owner, style)
    d = doc.add_paragraph(cl.get("date", ""))
    d.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for line in cl.get("recipient", []):
        p = doc.add_paragraph(line)
        p.paragraph_format.space_after = Pt(0)
    if cl.get("subject"):
        s = doc.add_paragraph()
        s.paragraph_format.space_before = Pt(10)
        s.add_run(cl["subject"]).bold = True
    sal = doc.add_paragraph(cl.get("salutation", "Dear Hiring Manager,"))
    sal.paragraph_format.space_before = Pt(8)
    for para in cl.get("paragraphs", []):
        p = doc.add_paragraph(para)
        p.paragraph_format.space_after = Pt(8)
    clos = doc.add_paragraph(cl.get("closing", "Kind regards,"))
    clos.paragraph_format.space_before = Pt(4)
    clos.paragraph_format.space_after = Pt(14)
    doc.add_paragraph(cl.get("signature", owner["name"]))
    path = Path(out) / (c.get("files", {}).get("cover_letter", "cover_letter") + ".docx")
    doc.save(path)
    return path


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    c = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    made = []
    if c.get("resume"):
        made.append(build_resume(c, out))
    if c.get("cover_letter"):
        made.append(build_cover_letter(c, out))
    for m in made:
        print(m)


if __name__ == "__main__":
    main()
