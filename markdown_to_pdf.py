#!/usr/bin/env python3
"""Reusable reportlab markdown->styled-PDF generator for digital products (e-books).

Usage:
    python markdown_to_pdf.py out.pdf in1.md [in2.md ...]

Produces: A4 doc with dark cover page (first md file's `# Title` / `## Subtitle`),
styled H1/H2/H3, justified paragraphs, bullet lists, markdown pipe-tables,
page footer with title + green bottom bar. Arial fallback on Windows; pt-BR
accents work (Latin-1) but EMOJI DOES NOT — keep PDF body emoji-free.

Deps: pip install reportlab pypdf
"""
import re
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, PageBreak, Table, TableStyle, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ---------------------------------------------------------------- paleta (troque p/ sua marca)
PRETO   = HexColor("#14171c")
VERDE   = HexColor("#16a34a")   # acento principal
VERDE_E = HexColor("#0d7a37")
CINZA   = HexColor("#5b6472")
CINZA_C = HexColor("#eef1f4")
BRANCO  = HexColor("#ffffff")
AMARELO = HexColor("#fbbf24")   # acento secundário (capa)

def reg_font(fname, name):
    for d in [r"C:\Windows\Fonts", "/usr/share/fonts/truetype/dejavu", "/System/Library/Fonts"]:
        p = os.path.join(d, fname)
        if os.path.exists(p):
            try:
                pdfmetrics.registerFont(TTFont(name, p))
                return True
            except Exception:
                pass
    return False

has_ttf = all(reg_font(f, n) for f, n in [
    ("arial.ttf", "Arial"), ("arialbd.ttf", "Arial-Bold"),
    ("ariali.ttf", "Arial-Italic")])
F, FB, FI = ("Arial", "Arial-Bold", "Arial-Italic") if has_ttf else \
            ("Helvetica", "Helvetica-Bold", "Helvetica-Oblique")

# ---------------------------------------------------------------- estilos
def styles():
    S = {}
    S["cap"]   = ParagraphStyle("cap", fontName=FB, fontSize=42, leading=48, textColor=BRANCO, alignment=TA_CENTER)
    S["sub"]   = ParagraphStyle("sub", fontName=F, fontSize=15, leading=21, textColor=HexColor("#cfe8d9"), alignment=TA_CENTER)
    S["tag"]   = ParagraphStyle("tag", fontName=F, fontSize=11, leading=16, textColor=AMARELO, alignment=TA_CENTER)
    S["h1"]    = ParagraphStyle("h1", fontName=FB, fontSize=24, leading=30, textColor=VERDE_E, spaceBefore=6, spaceAfter=14)
    S["h2"]    = ParagraphStyle("h2", fontName=FB, fontSize=16, leading=21, textColor=PRETO, spaceBefore=14, spaceAfter=6)
    S["h3"]    = ParagraphStyle("h3", fontName=FB, fontSize=12.5, leading=17, textColor=VERDE_E, spaceBefore=10, spaceAfter=4)
    S["p"]     = ParagraphStyle("p", fontName=F, fontSize=11, leading=16.5, textColor=PRETO, alignment=TA_JUSTIFY, spaceAfter=7)
    S["li"]    = ParagraphStyle("li", fontName=F, fontSize=11, leading=16.5, textColor=PRETO, alignment=TA_JUSTIFY,
                                leftIndent=14, bulletIndent=2, spaceAfter=4)
    S["th"]    = ParagraphStyle("th", fontName=FB, fontSize=9.5, leading=13, textColor=BRANCO)
    S["td"]    = ParagraphStyle("td", fontName=F, fontSize=9.5, leading=13, textColor=PRETO)
    S["quote"] = ParagraphStyle("quote", fontName=FI, fontSize=12, leading=18, textColor=VERDE_E,
                                leftIndent=16, rightIndent=16, spaceBefore=8, spaceAfter=12)
    return S

def inline(t):
    """**negrito** e *itálico* -> reportlab tags; escapa < > & (sem tocar nas tags geradas)."""
    t = re.sub(r"\*\*(.+?)\*\*", lambda m: "\x00b" + m.group(1) + "\x00B", t)
    t = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", lambda m: "\x00i" + m.group(1) + "\x00I", t)
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return t.replace("\x00b", "<b>").replace("\x00B", "</b>").replace("\x00i", "<i>").replace("\x00I", "</i>")

def render_table(flow, rows, S):
    if len(rows) < 2:
        return
    ncols = max(len(r) for r in rows)
    data = [[Paragraph(c, S["th"]) for c in rows[0]]]
    for r in rows[1:]:
        r = r + [""] * (ncols - len(r))
        data.append([Paragraph(c, S["td"]) for c in r])
    t = Table(data, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), VERDE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#eef1f4")]),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#c9d2dc")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]))
    flow.append(t)
    flow.append(Spacer(1, 10))

def parse_md(path, flow, S):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    i, in_table, tbl = 0, False, []
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1
            continue
        if ln.strip().startswith("|") and not in_table:
            in_table, tbl = True, []
            i += 1
            continue
        if in_table:
            if ln.strip().startswith("|"):
                cells = [c.strip() for c in ln.strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    tbl.append(cells)
                i += 1
                continue
            if tbl:
                render_table(flow, tbl, S)
                tbl = []
            in_table = False
            continue
        if ln.startswith("---"):
            flow.append(HRFlowable(width="100%", thickness=1, color=CINZA_C, spaceBefore=10, spaceAfter=14))
        elif ln.startswith("# "):   flow.append(Paragraph(inline(ln[2:]), S["h1"]))
        elif ln.startswith("## "):  flow.append(Paragraph(inline(ln[3:]), S["h2"]))
        elif ln.startswith("### "): flow.append(Paragraph(inline(ln[4:]), S["h3"]))
        elif ln.startswith("- ") or ln.startswith("* "):
            flow.append(Paragraph(inline(ln[2:]), S["li"], bulletText="\u2022"))
        elif ln.startswith("> "):   flow.append(Paragraph(inline(ln[2:]), S["quote"]))
        else:                       flow.append(Paragraph(inline(ln), S["p"]))
        i += 1
    if tbl:
        render_table(flow, tbl, S)

def cover(flow, S, title, subtitle, tagline=""):
    flow.append(Spacer(1, 90 * mm))
    flow.append(Paragraph(title, S["cap"]))
    flow.append(Spacer(1, 8 * mm))
    flow.append(Paragraph(subtitle, S["sub"]))
    if tagline:
        flow.append(Spacer(1, 30 * mm))
        flow.append(Paragraph(tagline, S["tag"]))
    flow.append(PageBreak())

def build(out_pdf, md_files, title, subtitle, tagline=""):
    S = styles()
    doc = BaseDocTemplate(out_pdf, pagesize=A4,
                          leftMargin=20 * mm, rightMargin=20 * mm,
                          topMargin=18 * mm, bottomMargin=18 * mm,
                          title=title, author=title)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")

    def on_page(canv, doc_):
        canv.saveState()
        if doc_.page > 1:
            canv.setFillColor(CINZA)
            canv.setFont(F, 8)
            canv.drawCentredString(A4[0] / 2, 10 * mm, f"{title} — página {doc_.page}")
            canv.setFillColor(VERDE)
            canv.rect(0, 0, A4[0], 3.2 * mm, stroke=0, fill=1)
        canv.restoreState()

    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=on_page)])
    flow = []
    cover(flow, S, title, subtitle, tagline)
    for m in md_files:
        parse_md(m, flow, S)
        flow.append(PageBreak())
    doc.build(flow)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("uso: python markdown_to_pdf.py out.pdf in1.md [in2.md ...] [--title 'X'] [--subtitle 'Y'] [--tagline 'Z']")
    out = sys.argv[1]
    ins = [a for a in sys.argv[2:] if a.endswith(".md")]
    args = sys.argv[2:]
    def arg(name, default):
        return args[args.index(name) + 1] if name in args else default
    build(out, ins,
          title=arg("--title", "IA QUE PAGA"),
          subtitle=arg("--subtitle", "O Guia Definitivo para Gerar Renda Extra com Inteligência Artificial"),
          tagline=arg("--tagline", "Renda extra \u2022 Produtos digitais \u2022 Automação \u2022 Liberdade"))
    from pypdf import PdfReader
    print(f"OK — {len(PdfReader(out).pages)} páginas em {out}")
