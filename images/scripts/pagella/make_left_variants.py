"""Left panel of fig:param-space-symmetries -- 3 variants (layout x style), Inkscape-editable SVG.

Units: 1 user unit = 1 mm. All text stays <text> in TeX Gyre Pagella Math (matches mathpazo).
Usage: python3 make_left_variants.py OUTDIR
"""
import math
import os
import re
import subprocess
import sys
from xml.sax.saxutils import escape

from fontTools.ttLib import TTFont

PT = 0.3528
FONT_FILE = "/usr/share/texmf/fonts/opentype/public/tex-gyre-math/texgyrepagella-math.otf"
MATH = "'TeX Gyre Pagella Math', 'TeX Gyre Pagella', serif"
BOLD = "'TeX Gyre Pagella', serif"
TEXTWIDTH = 138.0  # MDPI \textwidth (mm)

_font = TTFont(FONT_FILE)
_cmap, _hmtx, _upm = _font.getBestCmap(), _font["hmtx"], _font["head"].unitsPerEm

# Colour-blind-safe set (Paul Tol muted/bright): min pairwise dE >= 22 in normal, protan, deutan vision.
COL = {1: "#332288", 2: "#3b9fc9", 3: "#117733", 4: "#882255", 5: "#999933", 6: "#ee6677"}
INK, GREY = "#222222", "#555555"


def f1(v):
    return f"{v:.1f}"


# ------------------------------------------------------------------ math text
ITALIC_GREEK = {"θ": "\U0001D703", "η": "\U0001D702", "σ": "\U0001D70E"}
HAIR, THIN, MED = " ", " ", " "
OPS = set("+=<>←↔⇒∈≡")


def _italic(c):
    if c == "h":
        return "ℎ"
    if "a" <= c <= "z":
        return chr(0x1D44E + ord(c) - 97)
    if "A" <= c <= "Z":
        return chr(0x1D434 + ord(c) - 65)
    return c


def _convert(chunk, sp):
    out = []
    for tok in re.findall(r"\\[A-Za-z]+|[A-Za-z]+|.", chunk):
        if tok.startswith("\\"):
            out.append(tok[1:])
        elif tok.isascii() and tok.isalpha():
            out.append(_italic(tok) if len(tok) == 1 else tok)
        elif tok in ITALIC_GREEK:
            out.append(ITALIC_GREEK[tok])
        elif tok == "ŷ":
            out.append("\U0001D466̂")
        elif tok == "'":
            out.append("′")
        elif tok == "-":
            out.append(sp + "−" + sp)
        elif tok in OPS:
            out.append(sp + tok + sp)
        else:
            out.append(tok)
    return "".join(out)


def parse(s, sp):
    runs, i = [], 0
    while i < len(s):
        if s[i] in "_^":
            mode = "sub" if s[i] == "_" else "sup"
            i += 1
            if s[i] == "{":
                j = s.index("}", i)
                content, i = s[i + 1 : j], j + 1
            else:
                content, i = s[i], i + 1
            runs.append((_convert(content, sp), mode))
        else:
            j = i
            while j < len(s) and s[j] not in "_^":
                j += 1
            runs.append((_convert(s[i:j], sp), "n"))
            i = j
    return runs


def _adv(ch):
    g = _cmap.get(ord(ch))
    if g is None:
        return {HAIR: 0.1, THIN: 0.2, MED: 0.25}.get(ch, 0.5) * _upm
    return 0 if 0x300 <= ord(ch) <= 0x36F else _hmtx[g][0]


def width(s, fs, sp=THIN):
    return sum(sum(_adv(c) for c in t) * fs * (1.0 if m == "n" else 0.7) / _upm for t, m in parse(s, sp))


class Doc:
    """Collects SVG pieces plus geometry used by the validator."""

    def __init__(self):
        self.n = 0
        self.texts = {}  # id -> container id (frame) or None
        self.segments = []  # (x1, y1, x2, y2) lines that text must not cross
        self.boxes = {}  # id -> (x, y, w, h) frames / tags / legend rects
        self.markers = {}

    def uid(self, base):
        self.n += 1
        return f"{base}-{self.n}"

    def text(self, x, y, s, fs, fill=INK, anchor="start", sp=THIN, vcenter=False, extra="",
             label=None, family=MATH, weight="normal", container=None, idbase="t"):
        if vcenter:
            y += 0.33 * fs
        body = []
        for t, mode in parse(s, sp):
            t = escape(t)
            if mode == "n":
                body.append(t)
            else:
                shift = "sub" if mode == "sub" else "super"
                body.append(f'<tspan style="font-size:70%;baseline-shift:{shift}">{t}</tspan>')
        tid = self.uid(idbase)
        self.texts[tid] = container
        lab = f' inkscape:label="{escape(label)}"' if label else ""
        return (
            f'<text xml:space="preserve" id="{tid}" x="{f1(x)}" y="{f1(y)}"{lab} '
            f'style="font-family:{family};font-weight:{weight};font-size:{fs:.2f}px;fill:{fill};'
            f'text-anchor:{anchor}"{extra}>' + "".join(body) + "</text>"
        )

    def line(self, x1, y1, x2, y2, color, w, guard=True):
        if guard:
            self.segments.append((x1, y1, x2, y2))
        return (f'<path d="M {f1(x1)},{f1(y1)} L {f1(x2)},{f1(y2)}" '
                f'style="fill:none;stroke:{color};stroke-width:{w:.2f};stroke-linecap:round"/>')

    def marker(self, color):
        mid = f"arrowhead-{color.lstrip('#')}"
        self.markers[mid] = (
            f'<marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="1.5" markerHeight="1.5" '
            f'orient="auto-start-reverse" markerUnits="userSpaceOnUse" style="overflow:visible">'
            f'<path d="M 0,0 L 10,5 L 0,10 Z" style="fill:{color};stroke:none"/></marker>')
        return mid

    def swap_arc(self, x, ya, yb, color, bulge=2.2, w=0.4):
        mid = self.marker(color)
        # polyline approximation for the validator
        pts = [(x + 0.75 * bulge * 4 * t * (1 - t), ya + (yb - ya) * (3 * t * t - 2 * t ** 3))
               for t in [i / 8 for i in range(9)]]
        self.segments += [(*pts[i], *pts[i + 1]) for i in range(8)]
        return (f'<path d="M {f1(x)},{f1(ya)} C {f1(x + bulge)},{f1(ya)} {f1(x + bulge)},{f1(yb)} {f1(x)},{f1(yb)}" '
                f'style="fill:none;stroke:{color};stroke-width:{w:.2f};marker-start:url(#{mid});marker-end:url(#{mid})"/>')

    def rect(self, rid, x, y, w, h, style, rx=0.0, label=None, record=True):
        if record:
            self.boxes[rid] = (x, y, w, h)
        lab = f' inkscape:label="{escape(label)}"' if label else ""
        return (f'<rect id="{rid}"{lab} x="{f1(x)}" y="{f1(y)}" width="{f1(w)}" height="{f1(h)}" '
                f'rx="{rx:.1f}" style="{style}"/>')


# ------------------------------------------------------------------ network
class Geom:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def net_points(ox, g):
    n1 = ox + g.E + g.r
    n2 = n1 + 2 * g.r + g.E
    return n1, n2, n2 + g.r + g.F


def draw_net(doc, ox, oy, g, spec, cont, softmax=False):
    n1, n2, xf = net_points(ox, g)
    out = []
    for (lab, col), (xa, xb) in zip((spec["th1"], spec["th2"]), ((ox, n1 - g.r), (n1 + g.r, n2 - g.r))):
        out.append(doc.line(xa, oy, xb, oy, col or GREY, g.lwc if col else g.lw))
    ends = []
    for k, (lab, col) in zip((-1, 0, 1), spec["eta"]):
        ex, ey = xf, oy + k * g.dy
        dx, dyy = ex - n2, ey - oy
        n = math.hypot(dx, dyy)
        out.append(doc.line(n2 + g.r * dx / n, oy + g.r * dyy / n, ex, ey, col or GREY, g.lwc if col else g.lw))
        ends.append((ex, ey))
    for cx in (n1, n2):
        out.append(f'<circle cx="{f1(cx)}" cy="{f1(oy)}" r="{g.r:.1f}" '
                   f'style="fill:#ffffff;stroke:{GREY};stroke-width:{g.lw:.2f}"/>')
        out.append(doc.text(cx, oy, "σ", g.sfs, INK, "middle", vcenter=True, container=cont, idbase="sigma"))
    lab, col = spec["input"]
    out.append(doc.text(ox - 0.6, oy, lab, g.fs, col or INK, "end", sp=HAIR, vcenter=True,
                        container=cont, idbase="input"))
    for (lab, col), xm, nm in zip((spec["th1"], spec["th2"]), (ox + g.E / 2, n1 + g.r + g.E / 2), ("th1", "th2")):
        out.append(doc.text(xm, oy - 0.9, lab, g.fs, col or INK, "middle", sp=HAIR, container=cont, idbase=nm))
    if not softmax:
        for i, ((lab, col), (ex, ey)) in enumerate(zip(spec["eta"], ends)):
            out.append(doc.text(ex + 0.6, ey, lab, g.fs, col or INK, "start", sp=HAIR, vcenter=True,
                                container=cont, idbase=f"eta{i + 1}"))
    return "\n".join(out), ends


# ------------------------------------------------------------------ content (same for all variants)
c = COL
SUBPLOTS = {
    1: dict(name="(1) symmetric state", input=("x", None), th1=("θ_1", None), th2=("θ_2", None),
            eta=[("η_1", c[1]), ("η_2", c[1]), ("η_3", None)], swap=(0, 1),
            notes=["η_1=η_2 ⇒ gθ=θ"]),
    2: dict(name="(2) functional symmetry", input=("x", None), th1=("θ_1", None), th2=("θ_2", None),
            eta=[("η_1+Δ", c[2]), ("η_2+Δ", c[2]), ("η_3+Δ", c[2])],
            notes=["η←η+Δ𝟏", "softmax(z+c𝟏)=softmax(z)  ∀c"]),
    3: dict(name="(3) loss symmetry through f", input=("x", None), th1=("θ_1", None), th2=("θ_2", None),
            eta=[("η_1", None), ("η_2", c[3]), ("η_3", c[3])], swap=(1, 2),
            notes=["ℒ=CE(ŷ, y)=−log ŷ_1"]),
    4: dict(name="(4) general loss symmetry", input=("x=1", None), th1=("θ_1", None), th2=("θ_2=1", None),
            eta=[("η_1+Δ/3", c[4]), ("0+Δ/3", c[4]), ("η_3+Δ/3", c[4])],
            notes=["(\\i) η_2←0,  (\\ii) η←η+(Δ/3)𝟏", "ℒ=CE+‖θ‖_1,  Δ=log(5/2)"]),
    5: dict(name="(5) data-dependent symmetry", input=("x=0", c[5]), th1=("θ_1+Δ_1", c[5]),
            th2=("θ_2+Δ_2", c[5]), eta=[("η_1+Δ_3", c[5]), ("η_2+Δ_4", c[5]), ("η_3+Δ_5", c[5])],
            notes=["X'={0}", "𝒩(0)=𝟏/3 for all θ"]),
    6: dict(name="(6) instance-dependent symmetry", input=("x", None), th1=("θ_1+Δ_1", c[6]),
            th2=("θ_2+Δ_2", c[6]), eta=[("η_1+Δ_3", c[6]), ("η_2+Δ_4", c[6]), ("η_3+Δ_5", c[6])],
            notes=["θ, gθ∈U={θ_2<0}", "𝒩≡𝟏/3 on U"]),
}
LINKS = [(1, 2), (1, 4), (2, 3), (2, 5), (2, 6)]  # (subset, superset)

MINI = Geom(E=0, r=1.2, F=4.6, dy=3.0, fs=6.3 * PT, sfs=6.0 * PT, lw=0.28, lwc=0.5)
BIG = Geom(E=12.0, r=2.3, F=13.0, dy=5.6, fs=8.5 * PT, sfs=7.5 * PT, lw=0.33, lwc=0.6)
NOTE_FS, SETUP_FS, LEG_FS = 6.0 * PT, 8.0 * PT, 6.0 * PT
PAD, TOP, MARGIN = 1.5, 2.4, 2.5

MINI.E = max(width(s[k][0], MINI.fs, HAIR) for s in SUBPLOTS.values() for k in ("th1", "th2")) + 1.1
IN_W = max(width(s["input"][0], MINI.fs, HAIR) for s in SUBPLOTS.values()) + 0.6
ETA_W = max(width(l, MINI.fs, HAIR) for s in SUBPLOTS.values() for l, _ in s["eta"])
NOTE_W = max(width(n, NOTE_FS) for s in SUBPLOTS.values() for n in s["notes"])
_, _, XF_REL = net_points(0, MINI)
W = max(IN_W + XF_REL + 0.6 + ETA_W, NOTE_W) + 2 * PAD


def frame_h(n):
    return TOP + 2 * MINI.dy + 1.1 * MINI.fs + 0.9 + n * 1.3 * NOTE_FS + PAD - 0.4


# ------------------------------------------------------------------ variants
VARIANTS = {
    "A": dict(
        title="Cross (your sketch) + colour-accented",
        grid={3: (1, 0), 5: (0, 1), 2: (1, 1), 6: (2, 1), 1: (1, 2), 4: (1, 3)},
        links="adjacent", gap_h=6.2, gap_v=7.0, legend=(0, 2), style="accent"),
    "B": dict(
        title="Hasse diagram (larger sets higher) + clean minimal",
        grid={5: (0, 0), 3: (1, 0), 6: (2, 0), 2: (1, 1), 4: (2, 1), 1: (1, 2)},
        links="lines", gap_h=6.2, gap_v=11.0, legend=(0, 2), style="minimal"),
    "C": dict(
        title="Left-to-right chain (θ → f → ℒ) + muted warm",
        grid={4: (0, 0), 5: (1, 0), 1: (0, 1), 2: (1, 1), 3: (2, 1), 6: (1, 2)},
        links="adjacent", gap_h=6.2, gap_v=7.0, legend=(2, 2), style="warm"),
}
STYLES = {
    "accent": dict(bg=None, frame=lambda cl: f"fill:{cl};fill-opacity:0.07;stroke:{cl};stroke-width:0.35",
                   rx=1.6, tag="outline", sep=True, glyph=GREY),
    "minimal": dict(bg=None, frame=lambda cl: "fill:none;stroke:#c4c4c4;stroke-width:0.25",
                    rx=1.0, tag="filled", sep=False, glyph=GREY),
    "warm": dict(bg="#f8f6f3", frame=lambda cl: f"fill:#ffffff;stroke:{cl};stroke-width:0.3",
                 rx=0.8, tag="filled", sep=False, glyph="#6b6258"),
}
TAG = 3.6


def build_setup(doc, sx0):
    out = []
    sy0 = MARGIN + BIG.dy + 4.2
    spec = dict(input=("x", None), th1=("θ_1", None), th2=("θ_2", None),
                eta=[("η_1", None), ("η_2", None), ("η_3", None)])
    body, ends = draw_net(doc, sx0, sy0, BIG, spec, None, softmax=True)
    out.append(body)
    n1, n2, xf = net_points(sx0, BIG)
    for k, (lab, _), (ex, ey) in zip((-1, 0, 1), spec["eta"], ends):
        px, py = n2 + 0.7 * (ex - n2), sy0 + 0.7 * (ey - sy0)
        yb = py - (1.7 if k < 0 else 0.9) if k < 1 else py + 1.3 + 0.7 * BIG.fs
        out.append(doc.text(px, yb, lab, BIG.fs, INK, "middle", sp=HAIR, idbase=f"setup-eta{k + 2}"))
    bw, bh = 4.4, 2 * BIG.dy + 4.6
    out.append(doc.rect("setup-softmax-box", xf, sy0 - bh / 2, bw, bh,
                        f"fill:#ffffff;stroke:{GREY};stroke-width:{BIG.lw:.2f}", rx=0.6, record=False))
    out.append(doc.text(xf + bw / 2, sy0, "softmax", 7.0 * PT, INK, "middle", vcenter=True, idbase="setup-softmax",
                        extra=f' transform="rotate(-90 {f1(xf + bw / 2)} {f1(sy0)})"'))
    for k in (-1, 0, 1):
        y = sy0 + k * BIG.dy
        out.append(doc.line(xf + bw, y, xf + bw + 3.0, y, GREY, BIG.lw))
        out.append(doc.text(xf + bw + 3.6, y, f"ŷ_{k + 2}", BIG.fs, INK, "start", vcenter=True,
                            idbase=f"setup-yhat{k + 2}"))
    tx = xf + bw + 3.6 + width("ŷ_1", BIG.fs) + 7.0
    lines = ["𝒩(x)=softmax(η σ(θ_2 σ(θ_1x))),  σ=\\ReLU",
             "ℒ(θ)=CE(𝒩(x), y),  y=[1, 0, 0]^⊤",
             "θ_1=1,  η_1=η_2=log 2,  η_3=0",
             "θ_2, x generic unless specified"]
    lh = 1.45 * SETUP_FS
    ty0 = sy0 - 1.5 * lh + 0.33 * SETUP_FS
    for i, s in enumerate(lines):
        out.append(doc.text(tx, ty0 + i * lh, s, SETUP_FS, INK, "start", sp=MED, idbase="setup-text"))
    right = tx + max(width(s, SETUP_FS, MED) for s in lines)
    return "\n".join(out), sx0 - IN_W, right, sy0 + bh / 2


def legend(doc, x, y, style):
    """Visual-code key. (x, y) = top-left."""
    out = ['<g id="legend" inkscape:label="legend">']
    lh, tx = 3.6, x + 8.0
    yy = y + 1.4
    out.append(doc.line(x, yy, x + 5.2, yy, GREY, MINI.lwc, guard=False))
    out.append(doc.text(tx, yy, "parameter changed by g", LEG_FS, INK, vcenter=True, idbase="legend"))
    yy += lh
    out.append(doc.line(x, yy, x + 4.0, yy - 1.2, GREY, MINI.lwc, guard=False))
    out.append(doc.line(x, yy, x + 4.0, yy + 1.2, GREY, MINI.lwc, guard=False))
    seg_backup = list(doc.segments)
    out.append(doc.swap_arc(x + 4.8, yy - 1.2, yy + 1.2, GREY, bulge=1.7, w=0.35))
    doc.segments = seg_backup
    out.append(doc.text(tx, yy, "two parameters swapped by g", LEG_FS, INK, vcenter=True, idbase="legend"))
    yy += lh
    out.append(doc.text(x, yy, "Δ_i∈ℝ", LEG_FS, INK, vcenter=True, idbase="legend"))
    out.append(doc.text(tx, yy, "arbitrary shifts", LEG_FS, INK, vcenter=True, idbase="legend"))
    out.append("</g>")
    return "\n".join(out), yy + 1.5 - y


def number_tag(doc, k, fx, fy, kind):
    cl = COL[k]
    x, y = fx - 1.2, fy - 1.2
    if kind == "outline":
        r = doc.rect(f"s{k}-tag", x, y, TAG, TAG, f"fill:#ffffff;stroke:{cl};stroke-width:0.45", rx=0.4)
        fill = cl
    else:
        r = doc.rect(f"s{k}-tag", x, y, TAG, TAG, f"fill:{cl};stroke:none", rx=0.4)
        fill = "#ffffff"
    t = doc.text(x + TAG / 2, y + TAG / 2, str(k), 7.5 * PT, fill, "middle", vcenter=True,
                 family=BOLD, weight="bold", idbase=f"s{k}-number", container=f"s{k}-tag")
    return f'<g id="s{k}-number-group" inkscape:label="number">{r}{t}</g>'


def _glyph_bounds(ch):
    from fontTools.pens.boundsPen import BoundsPen
    gs = _font.getGlyphSet()
    pen = BoundsPen(gs)
    gs[_cmap[ord(ch)]].draw(pen)
    return pen.bounds  # xMin, yMin, xMax, yMax (font units)


_SUBSET_BOUNDS = _glyph_bounds("⊂")


def subset_glyph(doc, cx, cy, ang, color, lid):
    """'⊂' with its outline centred exactly on (cx, cy), rotated so the open side points along ang."""
    fs = 12 * PT
    x0, y0, x1, y1 = (v * fs / _upm for v in _SUBSET_BOUNDS)
    return doc.text(cx - (x0 + x1) / 2, cy + (y0 + y1) / 2, "⊂", fs, color, "start", idbase=lid,
                    extra=f' transform="rotate({ang:.1f} {f1(cx)} {f1(cy)})"')


def build(vkey):
    V, S = VARIANTS[vkey], STYLES[VARIANTS[vkey]["style"]]
    doc = Doc()
    grid, gap_h, gap_v = V["grid"], V["gap_h"], V["gap_v"]
    nrows = max(r for _, r in grid.values()) + 1
    row_n = {r: max(len(SUBPLOTS[k]["notes"]) for k, (cc, rr) in grid.items() if rr == r) for r in range(nrows)}
    row_h = {r: frame_h(n) for r, n in row_n.items()}

    # setup block, centred
    _, sl, sr, _ = build_setup(Doc(), 0.0)
    page_w = max(TEXTWIDTH, 3 * W + 2 * gap_h + 2 * MARGIN)
    label_w = 6.0  # room for panel label "a"
    sx0 = max(label_w + MARGIN - sl, (page_w - (sr - sl)) / 2 - sl)
    setup_svg, _, _, setup_bottom = build_setup(doc, sx0)

    grid_y0 = setup_bottom + (8.5 if S["sep"] else 7.5)
    grid_x0 = (page_w - (3 * W + 2 * gap_h)) / 2
    row_y, y = {}, grid_y0
    for r in range(nrows):
        row_y[r] = y
        y += row_h[r] + gap_v
    page_h = y - gap_v + MARGIN + 0.5

    frames, subs = {}, []
    for k in sorted(SUBPLOTS):
        s, cl = SUBPLOTS[k], COL[k]
        cc, rr = grid[k]
        fx, fy, fh = grid_x0 + cc * (W + gap_h), row_y[rr], row_h[rr]
        frames[k] = (fx, fy, W, fh)
        cont = f"s{k}-frame"
        g = [f'<g id="subplot-{k}" inkscape:label="{escape(s["name"])}">',
             doc.rect(cont, fx, fy, W, fh, S["frame"](cl), rx=S["rx"], label="frame")]
        ox, oy = fx + PAD + IN_W, fy + TOP + MINI.dy + 0.55 * MINI.fs
        body, ends = draw_net(doc, ox, oy, MINI, s, cont)
        g.append(f'<g id="s{k}-network" inkscape:label="network">{body}')
        if "swap" in s:
            a, b = s["swap"]
            lw_ = max(width(s["eta"][i][0], MINI.fs, HAIR) for i in (a, b))
            g.append(doc.swap_arc(ends[a][0] + 0.6 + lw_ + 0.7, ends[a][1], ends[b][1], cl))
        g.append("</g>")
        nb = oy + MINI.dy + 0.55 * MINI.fs + 0.9 + 0.75 * NOTE_FS
        for i, n in enumerate(s["notes"]):
            g.append(doc.text(fx + PAD, nb + i * 1.3 * NOTE_FS, n, NOTE_FS, INK, label=f"note {i + 1}",
                              container=cont, idbase=f"s{k}-note"))
        g.append(number_tag(doc, k, fx, fy, S["tag"]))
        g.append("</g>")
        subs.append("\n".join(g))

    # inclusion symbols
    incl = []
    for sub, sup in LINKS:
        (c1, r1), (c2, r2) = grid[sub], grid[sup]
        x1, y1, w1, h1 = frames[sub]
        x2, y2, w2, h2 = frames[sup]
        lid = f"incl-{sub}-in-{sup}"
        if V["links"] == "adjacent":
            if r1 == r2:
                cx, cy = ((x1 + w1 + x2) / 2 if c2 > c1 else (x2 + w2 + x1) / 2), y1 + h1 / 2
                ang = 0 if c2 > c1 else 180
            else:
                cx = x1 + w1 / 2
                cy = (y2 + h2 + y1) / 2 if r2 < r1 else (y1 + h1 + y2) / 2
                ang = -90 if r2 < r1 else 90
            incl.append(f'<g id="{lid}" inkscape:label="({sub}) ⊂ ({sup})">'
                        + subset_glyph(doc, cx, cy, ang, S["glyph"], lid) + "</g>")
        else:  # Hasse lines from top edge of subset to bottom edge of superset
            fs_ = 0.5 if c1 == c2 else (0.8 if c2 > c1 else 0.2)
            fe_ = 0.5 if c1 == c2 else (0.2 if c2 > c1 else 0.8)
            ax, ay = x1 + fs_ * w1, y1 - 1.0
            bx, by = x2 + fe_ * w2, y2 + h2 + 1.0
            L = math.hypot(bx - ax, by - ay)
            ux, uy = (bx - ax) / L, (by - ay) / L
            mx, my = (ax + bx) / 2, (ay + by) / 2
            gap = 2.1
            ang = math.degrees(math.atan2(by - ay, bx - ax))
            incl.append(f'<g id="{lid}" inkscape:label="({sub}) ⊂ ({sup})">'
                        + doc.line(ax, ay, mx - gap * ux, my - gap * uy, "#888888", 0.3)
                        + doc.line(mx + gap * ux, my + gap * uy, bx, by, "#888888", 0.3)
                        + subset_glyph(doc, mx, my, ang, S["glyph"], lid) + "</g>")

    # legend in an empty cell
    lc, lr = V["legend"]
    lx = grid_x0 + lc * (W + gap_h) + PAD
    leg_svg, leg_h = legend(doc, lx, 0, S)  # measure
    ly = row_y[lr] + (row_h[lr] - leg_h) / 2
    leg_svg, _ = legend(doc, lx, ly, S)

    bg = (f'<g id="layer-background" inkscape:groupmode="layer" inkscape:label="Background" sodipodi:insensitive="true">'
          f'<rect id="background" x="0" y="0" width="{f1(page_w)}" height="{f1(page_h)}" style="fill:{S["bg"]};stroke:none"/></g>'
          if S["bg"] else "")
    sep = (doc.line(MARGIN, setup_bottom + 3.0, page_w - MARGIN, setup_bottom + 3.0, "#bbbbbb", 0.25, guard=False)
           if S["sep"] else "")
    panel_label = doc.text(MARGIN, MARGIN + 3.2, "\\a", 10 * PT, INK, family=BOLD, weight="bold", idbase="panel-label")

    svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
     width="{f1(page_w)}mm" height="{f1(page_h)}mm" viewBox="0 0 {f1(page_w)} {f1(page_h)}" version="1.1">
<title>Parameter-space symmetries, left panel, variant {vkey}: {escape(V['title'])}</title>
<sodipodi:namedview id="namedview" pagecolor="#ffffff" inkscape:document-units="mm" units="mm"/>
<defs>
{chr(10).join(doc.markers.values())}
</defs>
{bg}
<g id="layer-setup" inkscape:groupmode="layer" inkscape:label="Setup">
{panel_label}
<g id="setup-network" inkscape:label="network N">
{setup_svg}
</g>
{sep}
</g>
<g id="layer-subplots" inkscape:groupmode="layer" inkscape:label="Subplots">
{chr(10).join(subs)}
</g>
<g id="layer-inclusions" inkscape:groupmode="layer" inkscape:label="Inclusions">
{chr(10).join(incl)}
</g>
<g id="layer-legend" inkscape:groupmode="layer" inkscape:label="Legend">
{leg_svg}
</g>
</svg>
"""
    return svg, doc, (page_w, page_h)


# ------------------------------------------------------------------ validation (real bboxes from Inkscape)
INKSCAPE_ENV = {k: v for k, v in os.environ.items()
                if k not in ("GSETTINGS_SCHEMA_DIR", "GTK_PATH", "GTK_EXE_PREFIX", "GIO_MODULE_DIR",
                             "GDK_PIXBUF_MODULE_FILE", "GDK_PIXBUF_MODULEDIR", "LOCPATH")}
INKSCAPE_ENV["XDG_DATA_DIRS"] = "/usr/local/share:/usr/share"


def inkscape(*args):
    return subprocess.run(["inkscape", *args], env=INKSCAPE_ENV, capture_output=True, text=True).stdout


def seg_hits_box(seg, b):
    x1, y1, x2, y2 = seg
    bx, by, bw, bh = b
    for i in range(41):
        t = i / 40
        x, y = x1 + t * (x2 - x1), y1 + t * (y2 - y1)
        if bx < x < bx + bw and by < y < by + bh:
            return True
    return False


def overlap(a, b, tol=0.0):
    return (a[0] + tol < b[0] + b[2] and b[0] + tol < a[0] + a[2]
            and a[1] + tol < b[1] + b[3] and b[1] + tol < a[1] + a[3])


def validate(path, doc):
    px = 96 / 25.4
    bb = {}
    for ln in inkscape(path, "--query-all").splitlines():
        p = ln.split(",")
        if len(p) == 5:
            bb[p[0]] = tuple(float(v) / px for v in p[1:])
    issues = []
    tids = [t for t in doc.texts if t in bb]
    for t in tids:
        cont = doc.texts[t]
        x, y, w, h = bb[t]
        if cont and not cont.endswith("-tag"):
            fx, fy, fw, fh = doc.boxes[cont]
            m = min(x - fx, y - fy, fx + fw - x - w, fy + fh - y - h)
            if m < 1.0:
                issues.append(f"{t}: only {m:.2f} mm from frame {cont}")
        for rid, rb in doc.boxes.items():
            if rid != cont and rid.endswith("-tag") and overlap(bb[t], rb):
                issues.append(f"{t} overlaps tag {rid}")
            if cont is None and not rid.endswith("-tag") and overlap(bb[t], rb, tol=-0.8):
                issues.append(f"{t} within 0.8 mm of / overlaps {rid}")
        shrunk = (x + 0.12, y + 0.12, w - 0.24, h - 0.24)
        for seg in doc.segments:
            if seg_hits_box(seg, shrunk):
                issues.append(f"{t} crossed by a line at ({seg[0]:.1f},{seg[1]:.1f})")
                break
    for i, a in enumerate(tids):
        for b in tids[i + 1:]:
            if overlap(bb[a], bb[b], tol=0.05):
                issues.append(f"text overlap: {a} / {b}")
    return issues


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    prefix = sys.argv[2] if len(sys.argv) > 2 else "left"
    for v in VARIANTS:
        svg, doc, (pw, ph) = build(v)
        path = os.path.join(outdir, f"{prefix}_{v}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg)
        issues = validate(path, doc)
        print(f"[{v}] {path}: {pw:.1f} x {ph:.1f} mm -- {len(issues)} layout issue(s)")
        for it in issues[:30]:
            print("   ", it)
