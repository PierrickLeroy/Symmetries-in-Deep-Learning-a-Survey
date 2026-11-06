"""Corpus selection and knowledge base (sec. Materials and Methods, Methodology) -- 2 design variants.

Left to right: identification (monitoring, keyword search, dedicated tools; one icon each)
-> screening on criteria (A) v (B) v (C), the rest is discarded -> collection (408) -> cited (322)
                                                                                -> knowledge base: raw.md -> summaries.md -> index.tsv
                                                                                                    summaries.md -> corpus coding (408)
Units: 1 user unit = 1 mm. Text stays <text> (TeX Gyre Pagella to match mathpazo, LM Mono for files and prompts),
so it is editable in Inkscape. Text widths are measured with the real font files to size boxes and wrap prompts.
Usage: python3 make_variants.py OUTDIR     (writes selection-flow_variant_{A,B}.svg and .png previews)
"""
import os
import subprocess
import sys
from xml.sax.saxutils import escape

from PIL import ImageFont

# ------------------------------------------------------------------ style
TEXT = "'TeX Gyre Pagella', serif"
MATH = "'TeX Gyre Pagella Math', 'TeX Gyre Pagella', serif"
MONO = "'Latin Modern Mono', monospace"
GYRE = "/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrepagella-"
FONT_FILES = {
    (TEXT, "normal", "normal"): GYRE + "regular.otf",
    (TEXT, "bold", "normal"): GYRE + "bold.otf",
    (TEXT, "normal", "italic"): GYRE + "italic.otf",
    (TEXT, "bold", "italic"): GYRE + "bolditalic.otf",
    (MATH, "normal", "normal"): "/usr/share/texmf/fonts/opentype/public/tex-gyre-math/texgyrepagella-math.otf",
    (MONO, "normal", "normal"): "/usr/share/texmf/fonts/opentype/public/lm/lmmono10-regular.otf",
}
FS_HEAD, FS_TXT, FS_SMALL = 3.2, 2.8, 2.5  # 9 pt, 8 pt, 7 pt

INK, GREY, ARROW = "#222222", "#555555", "#444444"
NODE_FILL, NODE_STROKE = "#FAF9F6", "#B9B4AA"  # warm grey, as in fig:sym-loci
GREEN, VERM, BLUE, SKY, ORANGE = "#009E73", "#D55E00", "#0072B2", "#56B4E9", "#E69F00"  # Wong palette
KB_FILL, KB_STROKE, KB_INK = "#F1F7FC", "#A8CBE5", "#1F5F8F"
PROMPT_FILL, PROMPT_STROKE = "#FEF8EC", "#E69F00"  # orange = LLM involved (prompts, sparkle of the tools icon)
DISC_FILL = "#FDF3EC"

PROMPT_SUM = ("Summarize following the structure: SUMMARY, KEY DEFINITIONS AND BACKGROUND NOTIONS, "
              "RESULTS (theoretical if any, empirical if any), METHODOLOGY, LIMITATIONS, THOUGHTS, ONE-LINE TL;DR")
PROMPT_IDX = "Extract citation_key, Title, Links, Keywords, Short comment"
CRITERIA = ["(A) peer-reviewed", "(B) > 50 citations", "(C) < 2 years old"]


def f1(v):
    return f"{v:.1f}"


_fonts = {}


def text_w(s, size, fam=TEXT, weight="normal", style="normal"):
    key = (fam, weight, style)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(FONT_FILES[key], 200)
    return _fonts[key].getlength(s) / 200 * size


def wrap(s, size, maxw, fam=MONO):
    lines, cur = [], ""
    for word in s.split():
        cand = (cur + " " + word).strip()
        if cur and text_w(cand, size, fam) > maxw:
            lines.append(cur)
            cur = word
        else:
            cur = cand
    return lines + [cur]


# ------------------------------------------------------------------ primitives
def T(x, y, s, size=FS_TXT, fam=TEXT, weight="normal", style="normal", fill=INK, anchor="start"):
    return (f'<text x="{f1(x)}" y="{f1(y)}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
            f'font-style="{style}" fill="{fill}" text-anchor="{anchor}" xml:space="preserve">{escape(s)}</text>')


def rect(x, y, w, h, fill, stroke, sw=0.3, rx=1.8, dash=None, gid=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    i = f' id="{gid}"' if gid else ""
    return (f'<rect{i} x="{f1(x)}" y="{f1(y)}" width="{f1(w)}" height="{f1(h)}" rx="{rx}" ry="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


MARKERS = {"ink": ARROW, "green": GREEN, "verm": VERM, "blue": BLUE}


def defs():
    m = "".join(f'<marker id="head-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="2.4" markerHeight="2.4" '
                f'markerUnits="userSpaceOnUse" orient="auto-start-reverse">'
                f'<path d="M 0,0.8 10,5 0,9.2 2.6,5 Z" fill="{c}"/></marker>' for k, c in MARKERS.items())
    return f"<defs>{m}</defs>"


def arrow(d, kind="ink", sw=0.35, gid=None):
    i = f' id="{gid}"' if gid else ""
    return (f'<path{i} d="{d}" fill="none" stroke="{MARKERS[kind]}" stroke-width="{sw}" '
            f'marker-end="url(#head-{kind})"/>')


def node(gid, x, y, w, h, lines, fill=NODE_FILL, stroke=NODE_STROKE, dash=None, sw=0.3):
    """Rounded box with centred lines; lines = [(text, size, weight, style, colour)], equal line pitch."""
    out = [f'<g id="{gid}">', rect(x, y, w, h, fill, stroke, sw=sw, dash=dash)]
    pitch = 1.22 * max(l[1] for l in lines)
    n = len(lines)
    for i, (s, size, weight, style, col) in enumerate(lines):
        by = y + h / 2 + (i - (n - 1) / 2) * pitch + 0.34 * size
        out.append(T(x + w / 2, by, s, size, TEXT, weight, style, col, "middle"))
    out.append("</g>")
    return "".join(out)


def count_node(gid, x, y, w, h, title, count, **kw):
    return node(gid, x, y, w, h, [(title, FS_TXT, "bold", "normal", INK), (f"({count})", FS_TXT, "normal", "normal", INK)], **kw)


def discarded_node(x, y, w, h):
    return node("node-discarded", x, y, w, h, [("Discarded", FS_TXT, "normal", "italic", VERM)],
                fill=DISC_FILL, stroke=VERM, dash="1.2,0.8")


def sparkle(cx, cy, a, fill=ORANGE):
    d = (f"M {f1(cx)},{f1(cy - a)} Q {f1(cx)},{f1(cy)} {f1(cx + a)},{f1(cy)} Q {f1(cx)},{f1(cy)} {f1(cx)},{f1(cy + a)} "
         f"Q {f1(cx)},{f1(cy)} {f1(cx - a)},{f1(cy)} Q {f1(cx)},{f1(cy)} {f1(cx)},{f1(cy - a)} Z")
    return f'<path d="{d}" fill="{fill}" stroke="none"/>'


# ------------------------------------------------------------------ icons (s = nominal width in mm)
def icon_eye(cx, cy, s=7.0):
    """Monitoring."""
    l, r, k = cx - s / 2, cx + s / 2, 0.62 * s
    d = (f"M {f1(l)},{f1(cy)} C {f1(cx - s / 4)},{f1(cy - k / 1.6)} {f1(cx + s / 4)},{f1(cy - k / 1.6)} {f1(r)},{f1(cy)} "
         f"C {f1(cx + s / 4)},{f1(cy + k / 1.6)} {f1(cx - s / 4)},{f1(cy + k / 1.6)} {f1(l)},{f1(cy)} Z")
    return (f'<g id="icon-monitoring"><path d="{d}" fill="#FFFFFF" stroke="{ARROW}" stroke-width="0.4" stroke-linejoin="round"/>'
            f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(0.2 * s)}" fill="{SKY}"/>'
            f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(0.09 * s)}" fill="{INK}"/>'
            f'<circle cx="{f1(cx + 0.06 * s)}" cy="{f1(cy - 0.07 * s)}" r="0.3" fill="#FFFFFF"/></g>')


def icon_search(cx, cy, s=7.0):
    """Keyword search: a magnifying glass over two lines of query text."""
    lx, ly, lr = cx - 0.1 * s, cy - 0.1 * s, 0.29 * s
    k = 0.7071 * lr
    return (f'<g id="icon-keyword-search">'
            f'<circle cx="{f1(lx)}" cy="{f1(ly)}" r="{f1(lr)}" fill="{SKY}" fill-opacity="0.3" stroke="{ARROW}" stroke-width="0.5"/>'
            f'<path d="M {f1(lx - 0.5 * lr)},{f1(ly - 0.22 * lr)} h {f1(lr)} M {f1(lx - 0.5 * lr)},{f1(ly + 0.28 * lr)} h {f1(0.65 * lr)}" '
            f'stroke="{ARROW}" stroke-width="0.35" stroke-linecap="round"/>'
            f'<path d="M {f1(lx + k)},{f1(ly + k)} L {f1(cx + 0.42 * s)},{f1(cy + 0.42 * s)}" stroke="{ARROW}" '
            f'stroke-width="0.95" stroke-linecap="round"/></g>')


def icon_tools(cx, cy, s=7.0):
    """Dedicated tools: a citation graph (Research Rabbit, Connected Papers) with a sparkle (LLMs)."""
    c = (cx - 0.08 * s, cy + 0.06 * s)
    pts = [(-0.42, -0.22), (-0.38, 0.36), (0.26, 0.4), (0.4, 0.02), (-0.06, -0.4)]
    pts = [(cx + a * s, cy + b * s) for a, b in pts]
    edges = [(c, p) for p in pts] + [(pts[0], pts[1]), (pts[2], pts[3]), (pts[0], pts[4])]
    e = "".join(f"M {f1(a[0])},{f1(a[1])} L {f1(b[0])},{f1(b[1])} " for a, b in edges)
    nodes = "".join(f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(0.085 * s)}" fill="{SKY}" stroke="{ARROW}" stroke-width="0.3"/>'
                    for x, y in pts)
    return (f'<g id="icon-dedicated-tools"><path d="{e}" stroke="#8A8A8A" stroke-width="0.3" fill="none"/>{nodes}'
            f'<circle cx="{f1(c[0])}" cy="{f1(c[1])}" r="{f1(0.12 * s)}" fill="{BLUE}" stroke="{ARROW}" stroke-width="0.3"/>'
            f'{sparkle(cx + 0.36 * s, cy - 0.36 * s, 0.17 * s)}</g>')


def icon_funnel(cx, cy, s=6.0):
    t, m, b, n = cy - 0.42 * s, cy + 0.04 * s, cy + 0.42 * s, 0.11 * s
    d = (f"M {f1(cx - s / 2)},{f1(t)} H {f1(cx + s / 2)} L {f1(cx + n)},{f1(m)} V {f1(b)} "
         f"L {f1(cx - n)},{f1(b - 0.12 * s)} V {f1(m)} Z")
    return f'<path id="icon-funnel" d="{d}" fill="#FFFFFF" stroke="{ARROW}" stroke-width="0.4" stroke-linejoin="round"/>'


def page(x, y, w, h, fold):
    d = f"M {f1(x)},{f1(y)} H {f1(x + w - fold)} L {f1(x + w)},{f1(y + fold)} V {f1(y + h)} H {f1(x)} Z"
    c = f"M {f1(x + w - fold)},{f1(y)} V {f1(y + fold)} H {f1(x + w)}"
    return (f'<path d="{d}" fill="#FFFFFF" stroke="{ARROW}" stroke-width="0.3" stroke-linejoin="round"/>'
            f'<path d="{c}" fill="none" stroke="{ARROW}" stroke-width="0.25" stroke-linejoin="round"/>')


def icon_files(gid, cx, cy, kind, w=7.0, h=8.8, stack=2, off=0.7):
    """Stack of per-work pages; (cx, cy) is the centre of the front page. kind: 'raw' or 'sum'."""
    x, y = cx - w / 2, cy - h / 2
    out = [f'<g id="{gid}">']
    for k in range(stack, 0, -1):
        out.append(page(x + k * off, y - k * off, w, h, 0.28 * w))
    out.append(page(x, y, w, h, 0.28 * w))
    mx, top = x + 0.17 * w, y + 0.32 * h
    if kind == "raw":  # plain text lines, a markdown heading on top
        lens = [0.38, 0.66, 0.62, 0.66, 0.5, 0.66]
        for i, L in enumerate(lens):
            col, sw = (INK, 0.5) if i == 0 else ("#A0A0A0", 0.35)
            yy = top + i * 0.11 * h
            out.append(f'<path d="M {f1(mx)},{f1(yy)} h {f1(L * w)}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>')
    else:  # structured summary: coloured section headings, each followed by a text line
        for i in range(3):
            yy = top + i * 0.22 * h
            out.append(f'<path d="M {f1(mx)},{f1(yy)} h {f1(0.3 * w)}" stroke="{BLUE}" stroke-width="0.6" stroke-linecap="round"/>')
            out.append(f'<path d="M {f1(mx)},{f1(yy + 0.1 * h)} h {f1(0.64 * w)}" stroke="#A0A0A0" stroke-width="0.35" stroke-linecap="round"/>')
    out.append("</g>")
    return "".join(out)


def icon_table(gid, cx, cy, w=8.4, h=7.2, rows=4, cols=3):
    x, y = cx - w / 2, cy - h / 2
    rh = h / rows
    out = [f'<g id="{gid}">', rect(x, y, w, h, "#FFFFFF", ARROW, sw=0.3, rx=0.6),
           f'<path d="M {f1(x + 0.15)},{f1(y + rh)} V {f1(y + 0.6)} Q {f1(x + 0.15)},{f1(y + 0.15)} {f1(x + 0.6)},{f1(y + 0.15)} '
           f'H {f1(x + w - 0.6)} Q {f1(x + w - 0.15)},{f1(y + 0.15)} {f1(x + w - 0.15)},{f1(y + 0.6)} V {f1(y + rh)} Z" fill="{SKY}" fill-opacity="0.45"/>']
    g = "".join(f"M {f1(x)},{f1(y + i * rh)} H {f1(x + w)} " for i in range(1, rows))
    g += "".join(f"M {f1(x + j * w / cols)},{f1(y)} V {f1(y + h)} " for j in range(1, cols))
    out.append(f'<path d="{g}" stroke="{ARROW}" stroke-width="0.2" fill="none"/>')
    out.append(rect(x, y, w, h, "none", ARROW, sw=0.3, rx=0.6))
    out.append("</g>")
    return "".join(out)


def file_label(cx, y, name):
    return T(cx, y, name, FS_SMALL, MONO, fill=KB_INK, anchor="middle")


def brace(x, y0, y1, w=2.4, col=ARROW):
    """Right-pointing curly brace spanning [y0, y1] at abscissa x; its tip is at (x + w, (y0 + y1) / 2)."""
    ym, q = (y0 + y1) / 2, w / 2
    d = (f"M {f1(x)},{f1(y0)} Q {f1(x + q)},{f1(y0)} {f1(x + q)},{f1(y0 + q)} V {f1(ym - q)} "
         f"Q {f1(x + q)},{f1(ym)} {f1(x + w)},{f1(ym)} Q {f1(x + q)},{f1(ym)} {f1(x + q)},{f1(ym + q)} "
         f"V {f1(y1 - q)} Q {f1(x + q)},{f1(y1)} {f1(x)},{f1(y1)}")
    return f'<path id="brace-identification" d="{d}" fill="none" stroke="{col}" stroke-width="0.35"/>'


def bubble(gid, x, y, w, text, side, base, tip, size=FS_SMALL, pad=1.6, lh=1.2, tw=1.4, r=1.4):
    """Prompt box (speech bubble) of width w; height follows the wrapped text.
    side in {'top', 'bottom', 'left', 'right'}: edge carrying the tail; base: abscissa (top/bottom) or ordinate
    (left/right) of the tail base; tip: (x, y) of the tail tip. Returns (svg, height)."""
    lines = wrap(text, size, w - 2 * pad - 2.2)
    h = 2 * pad + (len(lines) - 1) * lh * size + 0.75 * size
    X, Y = x + w, y + h
    tail = lambda a, b: f"L {f1(a[0])},{f1(a[1])} L {f1(tip[0])},{f1(tip[1])} L {f1(b[0])},{f1(b[1])} "
    d = f"M {f1(x + r)},{f1(y)} "
    if side == "top":
        d += tail((base - tw, y), (base + tw, y))
    d += f"H {f1(X - r)} A {r} {r} 0 0 1 {f1(X)},{f1(y + r)} "
    if side == "right":
        d += tail((X, base - tw), (X, base + tw))
    d += f"V {f1(Y - r)} A {r} {r} 0 0 1 {f1(X - r)},{f1(Y)} "
    if side == "bottom":
        d += tail((base + tw, Y), (base - tw, Y))
    d += f"H {f1(x + r)} A {r} {r} 0 0 1 {f1(x)},{f1(Y - r)} "
    if side == "left":
        d += tail((x, base + tw), (x, base - tw))
    d += f"V {f1(y + r)} A {r} {r} 0 0 1 {f1(x + r)},{f1(y)} Z"
    out = [f'<g id="{gid}"><path d="{d}" fill="{PROMPT_FILL}" stroke="{PROMPT_STROKE}" stroke-width="0.3" stroke-linejoin="round"/>',
           sparkle(X - 1.9, y + 1.9, 1.0)]
    for i, s in enumerate(lines):
        out.append(T(x + pad, y + pad + 0.72 * size + i * lh * size, s, size, MONO, fill="#333333"))
    out.append("</g>")
    return "".join(out), h


def bubble_h(text, w, size=FS_SMALL, pad=1.6, lh=1.2):
    return 2 * pad + (len(wrap(text, size, w - 2 * pad - 2.2)) - 1) * lh * size + 0.75 * size


def svg_doc(w, h, title, layers):
    body = "".join(f'<g id="layer-{lid}" inkscape:groupmode="layer" inkscape:label="{lab}">{"".join(c)}</g>\n'
                   for lid, lab, c in layers)
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
            f'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" width="{f1(w)}mm" height="{f1(h)}mm" '
            f'viewBox="0 0 {f1(w)} {f1(h)}" version="1.1">\n<title>{title}</title>\n'
            f'<sodipodi:namedview id="namedview" pagecolor="#ffffff" inkscape:document-units="mm" units="mm"/>\n'
            f'{defs()}\n{body}</svg>\n')


def screening_box(x, y, w, h):
    """Funnel and the three inclusion criteria; a work is kept iff (A) v (B) v (C)."""
    cx = x + w / 2
    out = [f'<g id="node-screening">', rect(x, y, w, h, NODE_FILL, NODE_STROKE), icon_funnel(cx, y + 5.2, 6.0)]
    tx = x + (w - max(text_w(c, FS_SMALL) for c in CRITERIA)) / 2
    for i, c in enumerate(CRITERIA):
        out.append(T(tx, y + 13.6 + i * 3.4, c, FS_SMALL))
    out.append("</g>")
    return "".join(out)


# ------------------------------------------------------------------ variant A: 138 mm (MDPI \textwidth), two rows
def variant_A():
    """Selection on top; the knowledge base hangs below the collection, inside a frame; outputs in a right column."""
    W, H = 138.0, 88.0
    R1, R2 = 19.0, 57.0           # selection row, knowledge-base file row
    xc, cw = 77.0, 18.0           # collection (and raw.md) centre, collection width
    xs = 98.5                     # summaries.md (and index.tsv) centre
    xo, ow = 120.6, 15.0          # output column left edge and width (cited, corpus coding)
    ident = [icon_eye(5, R1 - 11), icon_search(5, R1), icon_tools(5, R1 + 11), brace(10.6, R1 - 15, R1 + 15)]
    fx, fw, fy, fh = 25.0, 25.0, R1 - 12, 24.0
    sel = [
        arrow(f"M 14,{f1(R1)} H 24.4"),
        screening_box(fx, fy, fw, fh),
        arrow(f"M {f1(fx + fw + 1)},{f1(R1)} H {f1(xc - cw / 2 - 0.8)}", "green", gid="arrow-pass"),
        T((fx + fw + xc - cw / 2) / 2, R1 - 2, "A ∨ B ∨ C", FS_SMALL, MATH, fill=GREEN, anchor="middle"),
        arrow(f"M {f1(fx + fw / 2)},{f1(fy + fh + 0.8)} V {f1(fy + fh + 12.6)}", "verm", gid="arrow-discard"),
        T(fx + fw / 2 - 2, fy + fh + 8.0, "¬(A ∨ B ∨ C)", FS_SMALL, MATH, fill=VERM, anchor="end"),
        discarded_node(fx + 2, fy + fh + 13.5, fw - 4, 10.0),
        count_node("node-collection", xc - cw / 2, R1 - 8, cw, 16, "Collection", 408),
        arrow(f"M {f1(xc + cw / 2 + 1)},{f1(R1)} H {f1(xo - 0.6)}", gid="arrow-cited"),
        count_node("node-cited", xo, R1 - 8, ow, 16, "Cited", 322),
    ]
    yi = R2 + 23.0                # index.tsv centre
    kb = [rect(52.0, 29.5, 85.6, H - 31.0, KB_FILL, KB_STROKE, sw=0.3, rx=2.0, gid="frame-knowledge-base"),
          T(54.5, 34.6, "Knowledge base", FS_TXT, TEXT, "bold", "italic", KB_INK),
          arrow(f"M {f1(xc)},{f1(R1 + 8.6)} V {f1(R2 - 6.6)}", gid="arrow-markdown"),
          T(xc - 2, 41.0, "Markdown", FS_SMALL, TEXT, style="italic", fill=GREY, anchor="end"),
          T(xc - 2, 44.1, "conversion", FS_SMALL, TEXT, style="italic", fill=GREY, anchor="end"),
          icon_files("file-raw", xc, R2, "raw"), file_label(xc, R2 + 7.6, "raw.md"),
          icon_files("file-summaries", xs, R2, "sum"), file_label(xs, R2 + 7.6, "summaries.md"),
          icon_table("file-index", xs, yi), T(xs + 5.4, yi + 0.9, "index.tsv", FS_SMALL, MONO, fill=KB_INK),
          arrow(f"M {f1(xc + 5.5)},{f1(R2)} H {f1(xs - 4.1)}", gid="arrow-summarize"),
          arrow(f"M {f1(xs)},{f1(R2 + 9.2)} V {f1(yi - 4.0)}", gid="arrow-index")]
    b_sum, _ = bubble("prompt-summarize", 80.5, 31.5, 55.1, PROMPT_SUM, "bottom", (xc + xs) / 2 + 0.7,
                      ((xc + xs) / 2 + 0.7, R2 - 1.3))
    b_idx, _ = bubble("prompt-index", 56.5, R2 + 9.8, 36.5, PROMPT_IDX, "right", R2 + 14.4, (xs - 1.1, R2 + 14.4))
    cy = R2 + 11.5                # corpus coding centre
    out = [arrow(f"M {f1(xs + 5.5)},{f1(R2)} C {f1(xs + 13)},{f1(R2)} {f1(xo - 6.5)},{f1(cy)} {f1(xo - 0.6)},{f1(cy)}",
                 gid="arrow-taxonomize"),
           T(xs + 6.0, R2 - 2.0, "taxonomize", FS_SMALL, TEXT, style="italic", fill=GREY),
           node("node-corpus-coding", xo, cy - 7.5, ow, 15.0,
                [("Corpus", FS_TXT, "bold", "normal", INK), ("coding", FS_TXT, "bold", "normal", INK),
                 ("(408)", FS_TXT, "normal", "normal", INK)])]
    return svg_doc(W, H, "Corpus selection and knowledge base (variant A)", [
        ("identification", "Identification", ident),
        ("selection", "Screening and inclusion", sel),
        ("knowledge-base", "Knowledge base", kb),
        ("prompts", "Prompts", [b_sum, b_idx]),
        ("outputs", "Corpus coding", out)])


# ------------------------------------------------------------------ variant B: 184 mm (full width), single spine
def header(x0, x1, y, s, col=GREY):
    return (T((x0 + x1) / 2, y, s, FS_SMALL, TEXT, "bold", fill=col, anchor="middle") +
            f'<path d="M {f1(x0)},{f1(y + 1.8)} H {f1(x1)}" stroke="{col}" stroke-width="0.25"/>')


def variant_B():
    """One left-to-right spine (sources -> screening -> collection -> raw -> summaries -> corpus coding);
    discarded, cited and index.tsv branch off it; phase headers on top."""
    W, H = 184.0, 79.0
    S, ix = 41.0, 9.0             # spine ordinate, identification column centre
    fx, fw = 33.0, 25.0           # screening box
    xc, cw = 81.0, 20.0           # collection
    xr, xs = 111.0, 135.0         # raw.md, summaries.md
    xo, ow = 161.0, 22.5          # corpus coding
    heads = [header(0.5, 17.5, 6.0, "Identification"), header(fx, fx + fw, 6.0, "Screening"),
             header(xc - cw / 2, xc + cw / 2, 6.0, "Inclusion"),
             header(xc + cw / 2 + 3, W - 0.5, 6.0, "Knowledge base", KB_INK)]
    ident = [icon_eye(ix, S - 13), icon_search(ix, S), icon_tools(ix, S + 13),
             T(ix, S - 13 + 6.3, "Monitoring", FS_SMALL, anchor="middle", fill=GREY),
             T(ix, S + 6.3, "Keyword search", FS_SMALL, anchor="middle", fill=GREY),
             T(ix, S + 13 + 6.3, "Dedicated tools", FS_SMALL, anchor="middle", fill=GREY),
             brace(19.5, S - 17, S + 17)]
    fy, fh = S - 12, 24.0
    sel = [
        arrow(f"M 23,{f1(S)} H 32.4"),
        screening_box(fx, fy, fw, fh),
        arrow(f"M {f1(fx + fw + 1)},{f1(S)} H {f1(xc - cw / 2 - 0.8)}", "green", gid="arrow-pass"),
        T((fx + fw + xc - cw / 2) / 2, S - 2, "A ∨ B ∨ C", FS_SMALL, MATH, fill=GREEN, anchor="middle"),
        arrow(f"M {f1(fx + fw / 2)},{f1(fy + fh + 0.8)} V {f1(fy + fh + 12.6)}", "verm", gid="arrow-discard"),
        T(fx + fw / 2 + 2, fy + fh + 8.0, "¬(A ∨ B ∨ C)", FS_SMALL, MATH, fill=VERM),
        discarded_node(fx + 2, fy + fh + 13.5, fw - 4, 10.0),
        count_node("node-collection", xc - cw / 2, S - 8, cw, 16, "Collection", 408),
        arrow(f"M {f1(xc)},{f1(S + 8.8)} V {f1(S + 21.2)}", gid="arrow-cited"),
        count_node("node-cited", xc - cw / 2, S + 22, cw, 14, "Cited", 322),
    ]
    yi = S + 24.0                 # index.tsv centre
    mx = (xc + cw / 2 + xr - 4.5) / 2
    kb = [arrow(f"M {f1(xc + cw / 2 + 1)},{f1(S)} H {f1(xr - 4.1)}", gid="arrow-markdown"),
          T(mx, S - 5.2, "Markdown", FS_SMALL, TEXT, style="italic", fill=GREY, anchor="middle"),
          T(mx, S - 2.1, "conversion", FS_SMALL, TEXT, style="italic", fill=GREY, anchor="middle"),
          icon_files("file-raw", xr, S, "raw"), file_label(xr, S + 7.6, "raw.md"),
          icon_files("file-summaries", xs, S, "sum"), file_label(xs, S + 7.6, "summaries.md"),
          icon_table("file-index", xs, yi), T(xs + 5.4, yi + 0.9, "index.tsv", FS_SMALL, MONO, fill=KB_INK),
          arrow(f"M {f1(xr + 5.5)},{f1(S)} H {f1(xs - 4.1)}", gid="arrow-summarize"),
          arrow(f"M {f1(xs)},{f1(S + 9.2)} V {f1(yi - 4.0)}", gid="arrow-index")]
    bw = 54.0
    b_sum, _ = bubble("prompt-summarize", 106.0, S - 8.6 - bubble_h(PROMPT_SUM, bw), bw, PROMPT_SUM, "bottom",
                      (xr + xs) / 2 + 0.7, ((xr + xs) / 2 + 0.7, S - 1.3))
    b_idx, _ = bubble("prompt-index", xs + 3.2, S + 10.6, W - 0.5 - (xs + 3.2), PROMPT_IDX, "left", S + 15.2, (xs + 1.1, S + 15.2))
    out = [arrow(f"M {f1(xs + 5.5)},{f1(S)} H {f1(xo - 0.6)}", gid="arrow-taxonomize"),
           T((xs + 5.5 + xo) / 2, S - 2.0, "taxonomize", FS_SMALL, TEXT, style="italic", fill=GREY, anchor="middle"),
           count_node("node-corpus-coding", xo, S - 8, ow, 16, "Corpus coding", 408)]
    return svg_doc(W, H, "Corpus selection and knowledge base (variant B)", [
        ("headers", "Phase headers", heads),
        ("identification", "Identification", ident),
        ("selection", "Screening and inclusion", sel),
        ("knowledge-base", "Knowledge base", kb),
        ("prompts", "Prompts", [b_sum, b_idx]),
        ("outputs", "Corpus coding", out)])


# ------------------------------------------------------------------ export
INKSCAPE_ENV = {k: v for k, v in os.environ.items()
                if k not in ("GSETTINGS_SCHEMA_DIR", "GTK_PATH", "GTK_EXE_PREFIX", "GIO_MODULE_DIR",
                             "GDK_PIXBUF_MODULE_FILE", "GDK_PIXBUF_MODULEDIR", "LOCPATH")}
INKSCAPE_ENV["XDG_DATA_DIRS"] = "/usr/local/share:/usr/share"


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    for k, fn in (("A", variant_A), ("B", variant_B)):
        svg = os.path.join(outdir, f"selection-flow_variant_{k}.svg")
        with open(svg, "w", encoding="utf-8") as fh:
            fh.write(fn())
        subprocess.run(["inkscape", svg, "--export-type=png", "--export-dpi=300", "--export-background=#ffffff",
                        "-o", svg[:-4] + ".png"], env=INKSCAPE_ENV, capture_output=True, text=True, check=True)
        print(svg)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
