#!/usr/bin/env python3
"""Refill a user's own Word resume / cover letter with new content, keeping their formatting.

Usage:
  python3 fill_template.py map.json content.json OUT_DIR

map.json says which paragraph in the user's file is the example of each kind
(indices come from analyse_template.py):
{
  "resume": {
    "template": "/path/TEMPLATE-Resume.docx",
    "prototypes": {"name": 0, "contact": 1, "heading": 2, "body": 3, "label": 5,
                   "bullet": 6, "role_title": 13, "role_intro": 14, "spacer": 19},
    "keep_contact": true,            # reuse the contact paragraph exactly (keeps hyperlinks)
    "name_text": null,               # optional override for the name line, e.g. "JANE DOE (JD)"
    "role_title_pattern": "title_bold_org_plain",   # or "all_bold"
    "date_tab_inches": null,         # right tab for dates; null = text width
    "spacer_after_role": true,
    "uppercase_headings": true
  },
  "cover_letter": {
    "template": "/path/TEMPLATE-Cover_Letter.docx",
    "prototypes": {"name": 0, "contact": 1, "date": 3, "address": 5, "subject": 10,
                   "salutation": 12, "body": 14, "closing": 20, "signature": 22, "blank": 4,
                   "address_table": null},   # index of a template table holding the address block, if any
    "keep_contact": true
  }
}
Omitted prototypes fall back to "body" ("label" falls back to "body" in bold).

content.json uses the same format as build_docs.py (owner, files, resume, cover_letter).
"""
import copy
import json
import sys
from pathlib import Path

import docx
from docx.enum.text import WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.text.run import Run

HEADINGS = {"summary": "SUMMARY", "selected_impact": "Selected impact:", "capabilities": "CORE CAPABILITIES",
            "experience": "PROFESSIONAL WORK HISTORY", "early_career": "EARLY CAREER", "education": "EDUCATION"}


class Filler:
    def __init__(self, template, prototypes):
        self.doc = docx.Document(template)
        paras = self.doc.paragraphs
        self.proto = {k: copy.deepcopy(paras[i]._p) for k, i in prototypes.items()
                      if i is not None and not k.endswith("_table")}
        self.tables = [copy.deepcopy(t._tbl) for t in self.doc.tables]
        body = self.doc.element.body
        self.sect = body.find(qn("w:sectPr"))
        for child in list(body):
            if child is not self.sect:
                body.remove(child)

    def add(self, kind, texts=None, keep_original=False):
        src = self.proto.get(kind)
        if src is None:
            src = self.proto["body"]
        el = copy.deepcopy(src)
        self.sect.addprevious(el)
        p = Paragraph(el, self.doc._body)
        if texts is not None and not keep_original:
            self.set_runs(p, texts)
        return p

    @staticmethod
    def set_runs(p, texts):
        """texts: list of (text, bold or None). Reuse the first run's formatting."""
        runs = p._p.findall(qn("w:r"))
        if runs:
            proto_r = copy.deepcopy(runs[0])
        else:
            # Empty prototype: borrow the paragraph-mark formatting so text keeps the template's font.
            proto_r = OxmlElement("w:r")
            pPr = p._p.pPr
            mark = pPr.find(qn("w:rPr")) if pPr is not None else None
            if mark is not None:
                rpr = copy.deepcopy(mark)
                rpr.tag = qn("w:rPr")
                for bad in rpr.findall(qn("w:ins")) + rpr.findall(qn("w:del")):
                    rpr.remove(bad)
                proto_r.append(rpr)
        for el in list(p._p):
            if el.tag in (qn("w:r"), qn("w:hyperlink")):
                p._p.remove(el)
        for t, b in texts:
            r = copy.deepcopy(proto_r)
            for el in list(r):
                if el.tag != qn("w:rPr"):
                    r.remove(el)
            p._p.append(r)
            run = Run(r, p)
            run.text = t
            if b is not None:
                run.bold = b
        return p

    def add_table_lines(self, table_index, lines, cell=(0, 0)):
        """Clone a table from the template (e.g. an address block) and put one line per paragraph in a cell."""
        tbl = copy.deepcopy(self.tables[table_index])
        self.sect.addprevious(tbl)
        from docx.table import Table
        t = Table(tbl, self.doc._body)
        c = t.cell(*cell)
        paras = c.paragraphs
        proto_p = copy.deepcopy(paras[0]._p)
        for p in paras[1:]:
            p._p.getparent().remove(p._p)
        self.set_runs(paras[0], [(lines[0] if lines else "", None)])
        last = paras[0]._p
        for line in lines[1:]:
            el = copy.deepcopy(proto_p)
            last.addnext(el)
            self.set_runs(Paragraph(el, c), [(line, None)])
            last = el
        return t

    def text_width(self):
        s = self.doc.sections[0]
        return s.page_width - s.left_margin - s.right_margin

    def ensure_right_tab(self, p, inches=None):
        pos = docx.shared.Inches(inches) if inches else self.text_width()
        for t in p.paragraph_format.tab_stops:
            if t.alignment == WD_TAB_ALIGNMENT.RIGHT:
                return
        p.paragraph_format.tab_stops.add_tab_stop(pos, WD_TAB_ALIGNMENT.RIGHT)

    def fix_page_totals(self):
        """Replace a hard-coded total in 'x/3'-style footers with a NUMPAGES field."""
        for s in self.doc.sections:
            for part in (s.footer, s.header):
                if "NUMPAGES" in part._element.xml:
                    continue
                for p in part.paragraphs:
                    runs = p.runs
                    for i, r in enumerate(runs):
                        prev = "".join(x.text for x in runs[:i])
                        if r.text.strip().isdigit() and (prev.rstrip().endswith("/") or prev.rstrip().lower().endswith("of")):
                            rpr = copy.deepcopy(r._r.rPr) if r._r.rPr is not None else None
                            r.text = ""
                            for kind, val in (("begin", None), ("instr", " NUMPAGES "), ("separate", None), ("t", "1"), ("end", None)):
                                nr = OxmlElement("w:r")
                                if rpr is not None:
                                    nr.append(copy.deepcopy(rpr))
                                if kind == "instr":
                                    el = OxmlElement("w:instrText"); el.set(qn("xml:space"), "preserve"); el.text = val
                                elif kind == "t":
                                    el = OxmlElement("w:t"); el.text = val
                                else:
                                    el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), kind)
                                nr.append(el)
                                r._r.addprevious(nr)
                            break

    def save(self, path):
        self.fix_page_totals()
        self.doc.save(path)


def fill_resume(m, c, out):
    f = Filler(m["template"], m["prototypes"])
    rs, owner = c["resume"], c["owner"]
    H = {**HEADINGS, **rs.get("headings", {})}
    up = m.get("uppercase_headings", True)
    head = lambda t: f.add("heading", [(t.upper() if up else t, True)])
    f.add("name", [(m.get("name_text") or owner["name"].upper(), None)])
    if m.get("keep_contact", True) and "contact" in f.proto:
        f.add("contact", keep_original=True)
    else:
        f.add("contact", [("  |  ".join(x["text"] if isinstance(x, dict) else x for x in owner.get("contact", [])), None)])
    if rs.get("summary"):
        head(H["summary"]); f.add("body", [(rs["summary"], False)])
    if rs.get("selected_impact"):
        f.add("label", [(H["selected_impact"], True)])
        for b in rs["selected_impact"]:
            f.add("bullet", [(b, False)])
    if rs.get("capabilities"):
        head(H["capabilities"]); f.add("body", [(" | ".join(rs["capabilities"]), False)])
    if rs.get("roles"):
        head(H["experience"])
        for role in rs["roles"]:
            org = ", ".join(x for x in [role.get("org"), role.get("location")] if x)
            if m.get("role_title_pattern", "title_bold_org_plain") == "all_bold":
                texts = [(role["title"] + (", " + org if org else ""), True)]
            else:
                texts = [(role["title"] + ("," if org else ""), True), ((" " + org) if org else "", False)]
            if role.get("dates"):
                texts.append(("\t" + role["dates"], False))
            p = f.add("role_title", texts)
            f.ensure_right_tab(p, m.get("date_tab_inches"))
            if role.get("intro"):
                f.add("role_intro", [(role["intro"], False)])
            for b in role.get("bullets", []):
                f.add("bullet", [(b, False)])
            if m.get("spacer_after_role", True) and "spacer" in f.proto:
                f.add("spacer", [])
    if rs.get("early_career"):
        head(H["early_career"]); f.add("body", [(rs["early_career"], False)])
    for extra in rs.get("extra_sections", []):
        head(extra["heading"])
        if extra.get("text"):
            f.add("body", [(extra["text"], False)])
        for b in extra.get("bullets", []):
            f.add("bullet", [(b, False)])
    if rs.get("education"):
        head(H["education"])
        for b in rs["education"]:
            f.add("bullet", [(b, False)])
    path = Path(out) / (c.get("files", {}).get("resume", "resume") + ".docx")
    f.save(path)
    return path


def fill_cover_letter(m, c, out):
    f = Filler(m["template"], m["prototypes"])
    cl, owner = c["cover_letter"], c["owner"]
    if "name" in f.proto:
        f.add("name", [(m.get("name_text") or owner["name"].upper(), None)])
    if "contact" in f.proto:
        if m.get("keep_contact", True):
            f.add("contact", keep_original=True)
        else:
            f.add("contact", [("  |  ".join(x["text"] if isinstance(x, dict) else x for x in owner.get("contact", [])), None)])
    if "blank" in f.proto and ("name" in f.proto or "contact" in f.proto):
        f.add("blank", [])
    f.add("date", [(cl.get("date", ""), None)])
    if "blank" in f.proto:
        f.add("blank", [])
    if m["prototypes"].get("address_table") is not None:
        f.add_table_lines(m["prototypes"]["address_table"], cl.get("recipient", []))
    else:
        for line in cl.get("recipient", []):
            f.add("address", [(line, None)])
    if "blank" in f.proto:
        f.add("blank", [])
    if cl.get("subject"):
        f.add("subject", [(cl["subject"], None)])
        if "blank" in f.proto:
            f.add("blank", [])
    f.add("salutation", [(cl.get("salutation", "Dear Hiring Manager,"), None)])
    for para in cl.get("paragraphs", []):
        if "blank" in f.proto:
            f.add("blank", [])
        f.add("body", [(para, None)])
    if "blank" in f.proto:
        f.add("blank", [])
    f.add("closing", [(cl.get("closing", "Kind regards,"), None)])
    if "blank" in f.proto:
        f.add("blank", [])
    f.add("signature", [(cl.get("signature", owner["name"]), None)])
    path = Path(out) / (c.get("files", {}).get("cover_letter", "cover_letter") + ".docx")
    f.save(path)
    return path


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    m = json.loads(Path(sys.argv[1]).read_text())
    c = json.loads(Path(sys.argv[2]).read_text())
    out = Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
    if m.get("resume") and c.get("resume"):
        print(fill_resume(m["resume"], c, out))
    if m.get("cover_letter") and c.get("cover_letter"):
        print(fill_cover_letter(m["cover_letter"], c, out))


if __name__ == "__main__":
    main()
