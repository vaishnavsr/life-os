#!/usr/bin/env python3
"""Inspect a user's Word resume or cover letter so it can be reused as a template.

Usage:
  python3 analyse_template.py their_resume.docx

Prints every body paragraph with its index, style, alignment, shading, tab stops,
bullet/numbering, run formatting and a text preview. It also warns about layouts
that are hard to refill reliably: tables, text boxes, columns, images, and footers
with hard-coded page totals.

Use the output to write a prototype map for fill_template.py, choosing one
example paragraph index for each role (name, contact, heading, body, bullet,
role_title, role_intro, ...).
"""
import sys
from docx import Document
from docx.oxml.ns import qn


def para_info(p):
    pPr = p._p.pPr
    shd = pPr.find(qn("w:shd")) if pPr is not None else None
    num = pPr.find(qn("w:numPr")) if pPr is not None else None
    tabs = [f"{t.alignment.name if t.alignment else '?'}@{round(t.position.inches, 2) if t.position else '?'}in"
            for t in p.paragraph_format.tab_stops]
    runs = []
    for r in p.runs[:4]:
        f = []
        if r.bold: f.append("B")
        if r.italic: f.append("I")
        if r.font.size: f.append(f"{r.font.size.pt:g}pt")
        if r.font.name: f.append(r.font.name)
        if r.font.color is not None and r.font.color.type is not None and r.font.color.rgb is not None:
            f.append(f"#{r.font.color.rgb}")
        if r.font.all_caps: f.append("CAPS")
        runs.append("/".join(f) or "plain")
    hyperlinks = len(p._p.findall(qn("w:hyperlink")))
    return {
        "style": p.style.name if p.style is not None else "",
        "align": p.alignment.name if p.alignment is not None else "",
        "shaded": shd.get(qn("w:fill")) if shd is not None else "",
        "list": "yes" if (num is not None or "List" in (p.style.name if p.style is not None else "")) else "",
        "tabs": ",".join(tabs),
        "runs": " ".join(runs),
        "links": hyperlinks,
    }


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    doc = Document(sys.argv[1])
    body = doc.element.body
    warnings = []
    if body.findall(qn("w:tbl")):
        warnings.append(f"{len(body.findall(qn('w:tbl')))} table(s) in the body: a table-based layout (e.g. two columns) can't be refilled paragraph by paragraph.")
    xml = body.xml
    if "w:txbxContent" in xml:
        warnings.append("Text boxes found: their content is invisible to paragraph-based refilling.")
    if "<w:cols " in xml and 'w:num="2"' in xml:
        warnings.append("Multi-column section found.")
    if "<w:drawing" in xml:
        warnings.append("Images or shapes found (photo, logo or icons). They will be kept only if they sit in the header or footer.")
    for i, s in enumerate(doc.sections):
        for p in s.footer.paragraphs + s.header.paragraphs:
            t = p.text
            if "/" in t and any(ch.isdigit() for ch in t.split("/")[-1]) and "NUMPAGES" not in s.footer._element.xml:
                warnings.append(f"Section {i}: header/footer '{t.strip()}' may have a hard-coded page total; fill_template.py replaces it with a NUMPAGES field.")
    sec = doc.sections[0]
    print(f"Page: {sec.page_width.mm:.0f}x{sec.page_height.mm:.0f}mm, margins L{sec.left_margin.mm:.0f} R{sec.right_margin.mm:.0f} T{sec.top_margin.mm:.0f} B{sec.bottom_margin.mm:.0f}mm, text width {(sec.page_width - sec.left_margin - sec.right_margin) / 914400:.2f}in")
    print("idx | style | align | shade | list | tabs | runs | links | text")
    for i, p in enumerate(doc.paragraphs):
        d = para_info(p)
        print(f"{i:>3} | {d['style']} | {d['align']} | {d['shaded']} | {d['list']} | {d['tabs']} | {d['runs']} | {d['links']} | {p.text[:70]!r}")
    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(" -", w)
    else:
        print("\nNo layout warnings: suitable for fill_template.py.")


if __name__ == "__main__":
    main()
