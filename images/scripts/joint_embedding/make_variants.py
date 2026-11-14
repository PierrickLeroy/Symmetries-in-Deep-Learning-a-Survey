"""Joint-embedding (Siamese) architectures and the blocks that break their symmetries (sec:joint-embedding).

Vertical flow: x -> two views t_1.x, t_2.x -> encoders f_theta1, f_theta2 -> z_1, z_2 -> criterion L.
The two branches mirror each other: a green dashed axis marks the branch swap (theta_1, t_1) <-> (theta_2, t_2),
a green tie between the encoders marks theta_1 = theta_2. Symmetry-breaking blocks (Paul Tol colours, as in
fig:param-space-symmetries): EMA theta_1 -> theta_2 (indigo), negatives x^- (rose), batch-statistics loss R (olive).

Variant A: 2 x 2 small multiples (a base, b EMA, c negatives, d batch statistics).
Variant B: base (a) next to one diagram (b) carrying the three blocks, with a colour key.

Units: 1 user unit = 1 mm. Text stays <text> in TeX Gyre Pagella (matches mathpazo), so it is editable.
Usage: python3 make_variants.py OUTDIR        (writes joint-embedding_variant_{A,B}.svg and .png previews)
       python3 make_variants.py --final A|B  (writes survey/images/joint-embedding.{svg,pdf})
Re-running --final overwrites joint-embedding.svg / .pdf, including Inkscape edits made to them.
"""
import math
import os
import subprocess
import sys
from xml.sax.saxutils import escape

from fontTools.ttLib import TTFont

MATH = "'TeX Gyre Pagella Math', 'TeX Gyre Pagella', serif"
TEXT = "'TeX Gyre Pagella', serif"
CAL = "'Latin Modern Math', serif"  # script letters = the cmsy \mathcal shapes kept by mathpazo
W = 138.0  # MDPI \textwidth (mm)
FS_LAB, FS_TXT, FS_ANN, FS_TAG = 3.2, 2.8, 2.47, 2.3  # 9 pt, 8 pt, 7 pt, 6.5 pt

INK, GREY, LIGHT = "#222222", "#555555", "#bbbbbb"
BASE = "#3b9fc9"  # image ink, as in fig:exactness-rotation
SYM = "#117733"   # "the symmetry holds" (green, as in fig:exactness-rotation)
EMA = "#332288"   # Paul Tol indigo   -- parameters
NEG = "#ee6677"   # Paul Tol rose     -- inputs
BAT = "#999933"   # Paul Tol olive    -- loss
TINT = {EMA: "#e6e4f0", NEG: "#fde8ea", BAT: "#f3f3e3"}

_FONT = TTFont("/usr/share/texmf/fonts/opentype/public/tex-gyre-math/texgyrepagella-math.otf")
_CMAP, _HMTX, _UPM = _FONT.getBestCmap(), _FONT["hmtx"], _FONT["head"].unitsPerEm


def f1(v):
    return f"{v:.1f}"


def f2(v):
    return f"{v:.2f}"


# ------------------------------------------------------------------ math text: tiny TeX-like markup
#   letters -> math italic, \rm{..} upright, \cal{X} script letter, _x _{..} ^x ^{..} nested scripts
ITAL = {chr(97 + i): chr(0x1D44E + i) for i in range(26)}
ITAL["h"] = "ℎ"
ITAL.update({chr(65 + i): chr(0x1D434 + i) for i in range(26)})
ITAL.update({"θ": "𝜃", "λ": "𝜆", "ξ": "𝜉", "τ": "𝜏"})
CALMAP = {"L": "ℒ", "C": "𝒞", "T": "𝒯", "D": "𝒟"}
MED, THIN = " ", " "
REL = set("=←↔≠∼∈+−")
SCRIPT = {1: 0.7, 2: 0.75}  # relative size of a script level w.r.t. its parent


def _group(s, i):
    """Return (content, next index) for a {..} group or a single character starting at s[i]."""
    if s[i] == "{":
        depth, j = 0, i
        while True:
            depth += {"{": 1, "}": -1}.get(s[j], 0)
            if depth == 0:
                return s[i + 1:j], j + 1
            j += 1
    return s[i], i + 1


def parse(s, script=False):
    """List of nodes: ('t', str, family) or ('sub'|'sup', [nodes]); no relation spacing in scripts."""
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if s.startswith("\\rm", i):
            g, i = _group(s, i + 3)
            out.append(("t", g, MATH))
        elif s.startswith("\\cal", i):
            g, i = _group(s, i + 4)
            out.append(("t", CALMAP[g], CAL))
        elif c in "_^":
            g, i = _group(s, i + 1)
            out.append(("sub" if c == "_" else "sup", parse(g, True)))
        else:
            i += 1
            if c == "-":
                c = "−"
            if c in REL and not script:
                out.append(("t", MED + c + MED, MATH))
            elif c == ",":
                out.append(("t", "," + THIN, MATH))
            elif c == "·":
                out.append(("t", " ⋅ ", MATH))
            else:
                out.append(("t", ITAL.get(c, c), MATH))
    return out


def _adv(ch):
    g = _CMAP.get(ord(ch))
    if g is None:
        return {MED: 0.25, THIN: 0.2, " ": 0.1}.get(ch, 0.55) * _UPM
    return _HMTX[g][0]


def mwidth(s, fs):
    def w(nodes, k):
        tot = 0.0
        for n in nodes:
            if n[0] == "t":
                tot += sum(_adv(c) for c in n[1]) * fs * k / _UPM
            else:
                tot += w(n[1], k * SCRIPT[1 if k == 1 else 2])
        return tot
    return w(parse(s), 1.0)


def _emit(nodes, level=0):
    out = []
    for n in nodes:
        if n[0] == "t":
            t = escape(n[1])
            out.append(t if n[2] == MATH else f'<tspan style="font-family:{CAL}">{t}</tspan>')
        else:
            pct = int(100 * SCRIPT[1 if level == 0 else 2])
            shift = "sub" if n[0] == "sub" else "super"
            out.append(f'<tspan style="font-size:{pct}%;baseline-shift:{shift}">{_emit(n[1], level + 1)}</tspan>')
    return "".join(out)


HALO = "paint-order:stroke;stroke:#ffffff;stroke-width:0.7;stroke-linejoin:round;"


class Doc:
    def __init__(self):
        self.n, self.defs = 0, []

    def uid(self, base):
        self.n += 1
        return f"{base}-{self.n}"

    def math(self, x, y, s, fs=FS_TXT, anchor="middle", color=INK, halo=False, gid="m"):
        st = (f"font-family:{MATH};font-size:{fs}px;fill:{color};text-anchor:{anchor};"
              + (HALO if halo else ""))
        return (f'<text xml:space="preserve" id="{self.uid(gid)}" x="{f2(x)}" y="{f2(y)}" style="{st}">'
                f'{_emit(parse(s))}</text>')

    def text(self, x, y, s, fs=FS_TXT, anchor="start", style="normal", weight="normal", color=INK, gid="t"):
        return (f'<text xml:space="preserve" id="{self.uid(gid)}" x="{f2(x)}" y="{f2(y)}" '
                f'style="font-family:{TEXT};font-size:{fs}px;font-style:{style};font-weight:{weight};'
                f'fill:{color};text-anchor:{anchor}">{escape(s)}</text>')


# ------------------------------------------------------------------ connectors (cubic Beziers, trimmed for the head)
HL, HW = 1.5, 1.2  # arrow head length, width
LW = 0.35          # connector width


def _bez(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    u = 1 - t
    return (u ** 3 * x0 + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t ** 3 * x3,
            u ** 3 * y0 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t ** 3 * y3)


def _split(p, t):
    """First part [0, t] of the cubic p (de Casteljau)."""
    lerp = lambda a, b: (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    a, b, c = lerp(p[0], p[1]), lerp(p[1], p[2]), lerp(p[2], p[3])
    d, e = lerp(a, b), lerp(b, c)
    return [p[0], a, d, lerp(d, e)]


def seg_line(a, b):
    return [a, (a[0] + (b[0] - a[0]) / 3, a[1] + (b[1] - a[1]) / 3),
            (a[0] + 2 * (b[0] - a[0]) / 3, a[1] + 2 * (b[1] - a[1]) / 3), b]


def seg_quad(a, q, b):
    return [a, (a[0] + 2 / 3 * (q[0] - a[0]), a[1] + 2 / 3 * (q[1] - a[1])),
            (b[0] + 2 / 3 * (q[0] - b[0]), b[1] + 2 / 3 * (q[1] - b[1])), b]


def head(tip, u, color):
    nx, ny = -u[1], u[0]
    bx, by = tip[0] - HL * u[0], tip[1] - HL * u[1]
    return (f'<path d="M {f2(tip[0])},{f2(tip[1])} L {f2(bx + HW / 2 * nx)},{f2(by + HW / 2 * ny)} '
            f'L {f2(bx - HW / 2 * nx)},{f2(by - HW / 2 * ny)} Z" style="fill:{color};stroke:none"/>')


def arrow(doc, segs, color=GREY, w=LW, heads=("end",), dash=None, gid="arrow"):
    """Path through the cubic segments segs, with filled heads; the stroke stops inside each head."""
    segs = [list(s) for s in segs]
    out = []

    def trim_end(p):
        tip = p[3]
        lo, hi = 0.0, 1.0
        for _ in range(40):
            mid = (lo + hi) / 2
            q = _bez(p, mid)
            if math.hypot(q[0] - tip[0], q[1] - tip[1]) > 0.8 * HL:
                lo = mid
            else:
                hi = mid
        q = _bez(p, lo)
        d = math.hypot(tip[0] - q[0], tip[1] - q[1])
        return _split(p, lo), tip, ((tip[0] - q[0]) / d, (tip[1] - q[1]) / d)

    if "end" in heads:
        segs[-1], tip, u = trim_end(segs[-1])
        out.append(head(tip, u, color))
    if "start" in heads:
        rev = segs[0][::-1]
        rev, tip, u = trim_end(rev)
        segs[0] = rev[::-1]
        out.append(head(tip, u, color))
    d = f"M {f2(segs[0][0][0])},{f2(segs[0][0][1])} " + " ".join(
        "C " + " ".join(f"{f2(x)},{f2(y)}" for x, y in s[1:]) for s in segs)
    da = f";stroke-dasharray:{dash}" if dash else ""
    path = f'<path d="{d}" style="fill:none;stroke:{color};stroke-width:{w};stroke-linecap:butt{da}"/>'
    return f'<g id="{doc.uid(gid)}">{path}{"".join(out)}</g>'


# ------------------------------------------------------------------ pictograms
def _scene(kind):
    """Unit-square content (y down), fills only so that it can be scaled freely."""
    if kind == "neg":  # another data point: a house
        return ('<rect x="-1" y="-1" width="3" height="3" style="fill:#e4eff6"/>'
                '<rect x="-1" y="0.86" width="3" height="2" style="fill:#9cc8a0"/>'
                '<rect x="0.27" y="0.5" width="0.46" height="0.4" style="fill:#d9c08a"/>'
                '<path d="M 0.18,0.53 L 0.5,0.24 L 0.82,0.53 Z" style="fill:#a0524a"/>'
                '<rect x="0.44" y="0.66" width="0.13" height="0.24" style="fill:#7a5a3e"/>')
    if kind == "v2":  # grey-scale
        sky, sun, mtn, hill = "#ececec", "#cdcdcd", "#8c8c8c", "#5f5f5f"
    else:
        sky, sun, mtn, hill = "#e4eff6", "#ddcc77", BASE, "#24688a"
    return (f'<rect x="-1" y="-1" width="3" height="3" style="fill:{sky}"/>'
            f'<circle cx="0.74" cy="0.27" r="0.13" style="fill:{sun}"/>'
            f'<path d="M -0.2,1.2 L 0.3,0.4 L 0.5,0.66 L 0.68,0.47 L 1.2,1.2 Z" style="fill:{mtn}"/>'
            f'<path d="M -0.2,0.86 Q 0.3,0.7 0.62,0.84 T 1.2,0.8 L 1.2,1.2 L -0.2,1.2 Z" style="fill:{hill}"/>')


EXTRA = {"x": "", "neg": "",
         "v1": " translate(0.5 0.5) rotate(14) scale(1.4) translate(-0.58 -0.5)",  # crop + rotation
         "v2": " translate(1 0) scale(-1 1)"}                                          # flip + grey-scale


def thumb(doc, cx, cy, s, kind, frame=GREY, fw=0.25):
    x0, y0 = cx - s / 2, cy - s / 2
    cid = doc.uid("clip")
    doc.defs.append(f'<clipPath id="{cid}"><rect x="{f2(x0)}" y="{f2(y0)}" width="{f2(s)}" height="{f2(s)}" '
                    f'rx="0.6"/></clipPath>')
    return (f'<g id="{doc.uid("image-" + kind)}" inkscape:label="image {kind}">'
            f'<g clip-path="url(#{cid})"><g transform="translate({f2(x0)} {f2(y0)}) scale({f2(s)}){EXTRA[kind]}">'
            f'{_scene(kind)}</g></g>'
            f'<rect x="{f2(x0)}" y="{f2(y0)}" width="{f2(s)}" height="{f2(s)}" rx="0.6" '
            f'style="fill:none;stroke:{frame};stroke-width:{fw}"/></g>')


def card_stack(doc, cx, cy, s, n=2, off=0.75):
    out = [f'<g id="{doc.uid("negatives")}" inkscape:label="negatives x-">']
    for k in range(n, 0, -1):
        out.append(f'<rect x="{f2(cx - s / 2 + k * off)}" y="{f2(cy - s / 2 - k * off)}" width="{f2(s)}" '
                   f'height="{f2(s)}" rx="0.6" style="fill:{TINT[NEG]};stroke:{NEG};stroke-width:0.3"/>')
    out.append(thumb(doc, cx, cy, s, "neg", NEG, 0.35))
    out.append("</g>")
    return "".join(out)


ENC_WT, ENC_WB = 13.0, 7.0  # encoder trapezoid top / bottom widths


def encoder(doc, cx, yt, yb, label, fill="#f4f4f4", stroke=GREY):
    d = (f"M {f2(cx - ENC_WT / 2)},{f2(yt)} L {f2(cx + ENC_WT / 2)},{f2(yt)} "
         f"L {f2(cx + ENC_WB / 2)},{f2(yb)} L {f2(cx - ENC_WB / 2)},{f2(yb)} Z")
    return (f'<g id="{doc.uid("encoder")}" inkscape:label="encoder {label}">'
            f'<path d="{d}" style="fill:{fill};stroke:{stroke};stroke-width:0.35;stroke-linejoin:round"/>'
            f'{doc.math(cx, (yt + yb) / 2 + 0.9, label, FS_TXT)}</g>')


def enc_half(y, yt, yb):
    """Half width of the encoder at height y."""
    return (ENC_WT + (ENC_WB - ENC_WT) * (y - yt) / (yb - yt)) / 2


CW, CH = 1.5, 1.8  # embedding cell
Z_GREY = ("#c9c9c9", "#8f8f8f", "#e3e3e3", "#ababab")
Z_ROSE = ("#f6b9c0", "#e0606f", "#fbd9dd", "#ee8f9a")


def vector(cx, cy, fills, stroke=GREY):
    x0 = cx - 2 * CW
    return "".join(f'<rect x="{f2(x0 + i * CW)}" y="{f2(cy - CH / 2)}" width="{CW}" height="{CH}" '
                   f'style="fill:{c};stroke:{stroke};stroke-width:0.2"/>' for i, c in enumerate(fills))


def vector_stack(doc, cx, cy, fills, back=None, n=2, off=0.55, label="embedding"):
    out = [f'<g id="{doc.uid("embedding")}" inkscape:label="{label}">']
    if back:
        for k in range(n, 0, -1):
            out.append(f'<rect x="{f2(cx - 2 * CW + k * off)}" y="{f2(cy - CH / 2 - k * off)}" width="{4 * CW}" '
                       f'height="{CH}" style="fill:{TINT[back]};stroke:{back};stroke-width:0.25"/>')
    out.append(vector(cx, cy, fills))
    out.append("</g>")
    return "".join(out)


def matrix_icon(x0, y0, c=0.72):
    """4 x 4 cross-correlation matrix pushed to the identity."""
    out = []
    for i in range(4):
        for j in range(4):
            fill = BAT if i == j else "#ffffff"
            out.append(f'<rect x="{f2(x0 + j * c)}" y="{f2(y0 + i * c)}" width="{f2(c)}" height="{f2(c)}" '
                       f'style="fill:{fill};stroke:{BAT};stroke-width:0.12"/>')
    return "".join(out)


# ------------------------------------------------------------------ one diagram
PW = 66.0   # panel width
BX = 15.0   # branch offset from the mirror axis
S_IMG, S_NEG = 7.5, 6.0
Y_X, Y_V = 10.5, 22.5
ENC_T, ENC_B = 31.0, 39.0
Y_Z = 44.0
L_T, L_H = 51.5, 6.2
R_T, R_H = 62.0, 6.2

TITLES = {
    "base": ("symmetric setup", ""),
    "ema": ("EMA", "MoCo, BYOL, DINO"),
    "neg": ("negatives", "SimCLR, MoCo"),
    "bat": ("batch statistics", "Barlow Twins, VICReg"),
    "all": ("symmetry-breaking blocks", ""),
}
BOTTOM = {
    "base": ("\\rm{branch swap }(θ_1, t_1)↔(θ_2, t_2)", SYM),
    "ema": ("θ_2←mθ_2+(1-m)θ_1", INK),
    "neg": ("z^-=f_θ(x^-), x^-≠x", INK),
    "bat": ("\\cal{L}=L(z_1, z_2)+λR(Z_1, Z_2)", INK),
}


def panel(doc, letter, px0, py0, mode):
    """mode in base | ema | neg | bat | all. Returns (svg, bottom y of the drawn content)."""
    ema, neg, bat = (mode in ("ema", "all")), (mode in ("neg", "all")), (mode in ("bat", "all"))
    cx = px0 + PW / 2
    Y = lambda v: py0 + v
    xl, xr = cx - BX, cx + BX
    back, conn, shapes, labels = [], [], [], []

    # ---- title
    name, tags = TITLES[mode]
    labels.append(doc.text(px0 + 0.5, Y(3.4), letter, FS_LAB, weight="bold", gid=f"label-{letter}"))
    t = (f'<text xml:space="preserve" id="title-{letter}" x="{f2(px0 + 4.0)}" y="{f2(Y(3.4))}" '
         f'style="font-family:{TEXT};font-size:{FS_TXT}px;fill:{INK}">'
         f'<tspan style="font-style:italic">{escape(name)}</tspan>')
    if tags:
        t += f'<tspan style="font-size:{FS_TAG}px;fill:{GREY}">{THIN}({escape(tags)})</tspan>'
    labels.append(t + "</text>")

    # ---- input and views
    shapes.append(thumb(doc, cx, Y(Y_X), S_IMG, "x"))
    labels.append(doc.math(cx - S_IMG / 2 - 1.0, Y(Y_X + 1.0), "x", FS_TXT, "end"))
    same_t = mode == "base"  # fully symmetric setup: t_1 = t_2, identical views
    for sgn, kind, lab in ((-1, "v1", "t_1·x"), (1, "v1" if same_t else "v2", "t_2·x")):
        bx = cx + sgn * BX
        p0, p3 = (cx + sgn * 1.4, Y(Y_X + S_IMG / 2)), (bx, Y(Y_V - S_IMG / 2 - 0.3))
        conn.append(arrow(doc, [[p0, (p0[0], p0[1] + 3.2), (bx, Y(Y_X + 5.2)), p3]], gid="fork"))
        shapes.append(thumb(doc, bx, Y(Y_V), S_IMG, kind))
        labels.append(doc.math(bx + sgn * (S_IMG / 2 + 0.9), Y(Y_V + 1.0), lab, FS_TXT, "start" if sgn > 0 else "end"))
        conn.append(arrow(doc, [seg_line((bx, Y(Y_V + S_IMG / 2 + 0.3)), (bx, Y(ENC_T - 0.2)))]))
    if same_t:
        xa, xb = cx - BX + S_IMG / 2 + 0.6, cx + BX - S_IMG / 2 - 0.6
        conn.append(f'<g id="{doc.uid("tie")}" inkscape:label="same augmentation">'
                    f'<path d="M {f2(xa)},{f2(Y(Y_V))} H {f2(xb)}" style="fill:none;stroke:{SYM};stroke-width:0.45"/>'
                    + "".join(f'<circle cx="{f2(x)}" cy="{f2(Y(Y_V))}" r="0.45" style="fill:{SYM}"/>'
                              for x in (xa, xb)) + "</g>")
        labels.append(doc.math(cx, Y(Y_V - 1.0), "t_1=t_2", FS_ANN, color=SYM, halo=True, gid="tie-label"))

    # ---- encoders and their relation
    teacher = dict(fill=TINT[EMA], stroke=EMA) if ema else {}
    shapes.append(encoder(doc, xl, Y(ENC_T), Y(ENC_B), "f_{θ_1}"))
    shapes.append(encoder(doc, xr, Y(ENC_T), Y(ENC_B), "f_{θ_2}", **teacher))
    ym = (ENC_T + ENC_B) / 2
    gap = enc_half(ym, ENC_T, ENC_B) + 0.6
    if ema:
        conn.append(arrow(doc, [seg_line((xl + gap, Y(ym)), (xr - gap, Y(ym)))], EMA, 0.45, gid="ema"))
        labels.append(doc.math(cx, Y(ym - 1.0), "\\rm{EMA}", FS_ANN, color=EMA, halo=True, gid="ema-label"))
    else:
        conn.append(f'<g id="{doc.uid("tie")}" inkscape:label="tied weights">'
                    f'<path d="M {f2(xl + gap)},{f2(Y(ym))} H {f2(xr - gap)}" '
                    f'style="fill:none;stroke:{SYM};stroke-width:0.45"/>'
                    + "".join(f'<circle cx="{f2(x)}" cy="{f2(Y(ym))}" r="0.45" style="fill:{SYM}"/>'
                              for x in (xl + gap, xr - gap)) + "</g>")
        labels.append(doc.math(cx, Y(ym - 1.0), "θ_1=θ_2", FS_ANN, color=SYM, halo=True, gid="tie-label"))

    # ---- negatives: other inputs, through both (shared) encoders, into the criterion
    if neg:
        shapes.append(card_stack(doc, cx, Y(Y_V + 0.4), S_NEG))
        labels.append(doc.math(cx + S_NEG / 2 + 2.6, Y(Y_V + 1.4), "x^-", FS_TXT, "start", color=NEG))
        for sgn in (-1, 1):
            a = (cx + sgn * 2.0, Y(Y_V + 0.4 + S_NEG / 2 + 0.3))
            b = (cx + sgn * (BX - ENC_WT / 2 + 1.6), Y(ENC_T - 0.2))
            conn.append(arrow(doc, [seg_line(a, b)], NEG, gid="neg-in"))
            a = (cx + sgn * (BX - ENC_WB / 2 + 0.3), Y(ENC_B + 0.3))
            b = (cx + sgn * 2.4, Y(Y_Z - CH / 2 - 0.6))
            conn.append(arrow(doc, [seg_line(a, b)], NEG, gid="neg-out"))
        shapes.append(vector_stack(doc, cx, Y(Y_Z), Z_ROSE, NEG, n=1, label="negative embeddings z-"))
        conn.append(arrow(doc, [seg_line((cx, Y(Y_Z + CH / 2 + 0.3)), (cx, Y(L_T - 0.2)))], NEG, gid="neg-loss"))

    # ---- embeddings
    for sgn, lab in ((-1, "z_1"), (1, "z_2")):
        bx = cx + sgn * BX
        conn.append(arrow(doc, [seg_line((bx, Y(ENC_B + 0.3)), (bx, Y(Y_Z - CH / 2 - 0.3)))]))
        shapes.append(vector_stack(doc, bx, Y(Y_Z), Z_GREY, BAT if bat else None, label=lab))
        labels.append(doc.math(bx + sgn * (2 * CW + 1.0 + (1.1 if bat else 0)), Y(Y_Z + 1.0), lab, FS_TXT,
                               "start" if sgn > 0 else "end"))

    # ---- criterion
    ltxt = "L(z_1, z_2, z^-)" if neg else "L(z_1, z_2)"
    lw = mwidth(ltxt, FS_TXT) + 4.0
    shapes.append(f'<g id="{doc.uid("criterion")}" inkscape:label="criterion L">'
                  f'<rect x="{f2(cx - lw / 2)}" y="{f2(Y(L_T))}" width="{f2(lw)}" height="{L_H}" rx="1.0" '
                  f'style="fill:#ffffff;stroke:{INK};stroke-width:0.35"/>'
                  f'{doc.math(cx, Y(L_T + L_H / 2 + 0.95), ltxt, FS_TXT)}</g>')
    land = 4.6 if neg else 3.2  # where the z_i arrows land on the top edge of L
    for sgn in (-1, 1):
        p0 = (cx + sgn * (BX - (1.6 if bat else 0)), Y(Y_Z + CH / 2 + 0.3))
        p3 = (cx + sgn * land, Y(L_T - 0.2))
        conn.append(arrow(doc, [[p0, (p0[0], p0[1] + 4.0), (p3[0], p3[1] - 3.2), p3]], gid="to-criterion"))
    bottom = L_T + L_H

    # ---- batch statistics: an additional loss on the batches Z_1, Z_2
    if bat:
        rtxt = "R(Z_1, Z_2)"
        mi = 4 * 0.72
        rw = mwidth(rtxt, FS_TXT) + mi + 5.0
        x0 = cx - rw / 2
        shapes.append(f'<g id="{doc.uid("regularizer")}" inkscape:label="batch-statistics loss R">'
                      f'<rect x="{f2(x0)}" y="{f2(Y(R_T))}" width="{f2(rw)}" height="{R_H}" rx="1.0" '
                      f'style="fill:{TINT[BAT]};stroke:{BAT};stroke-width:0.4"/>'
                      f'{matrix_icon(x0 + 1.6, Y(R_T + (R_H - mi) / 2))}'
                      f'{doc.math(x0 + 1.6 + mi + 1.2, Y(R_T + R_H / 2 + 0.95), rtxt, FS_TXT, "start")}</g>')
        for sgn in (-1, 1):
            x = cx + sgn * (BX + 1.6)
            a, c = (x, Y(Y_Z + CH / 2 + 0.3)), (x, Y(R_T + R_H / 2 - 2.6))
            b = (cx + sgn * (rw / 2 + 0.2), Y(R_T + R_H / 2))
            conn.append(arrow(doc, [seg_line(a, c), seg_quad(c, (x, b[1]), b)], BAT, gid="to-regularizer"))
        bottom = R_T + R_H

    # ---- branch-swap mirror axis (kept unless EMA ties the branches asymmetrically)
    if not ema:
        y_end = bottom + (1.6 if mode != "base" else 2.2)
        back.append(f'<path id="{doc.uid("mirror")}" d="M {f2(cx)},{f2(Y(5.6))} V {f2(Y(y_end))}" '
                    f'style="fill:none;stroke:{SYM};stroke-width:0.3;stroke-dasharray:1.2,0.9"/>')

    if mode in BOTTOM:
        s, col = BOTTOM[mode]
        labels.append(doc.math(cx, Y(bottom + 5.4), s, FS_TXT, color=col, gid="bottom"))
        bottom += 5.4 + 1.0

    svg = (f'<g id="panel-{letter}" inkscape:label="panel {letter} ({mode})">'
           f'<g id="panel-{letter}-axis">{"".join(back)}</g>'
           f'<g id="panel-{letter}-connectors">{"".join(conn)}</g>'
           f'<g id="panel-{letter}-shapes">{"".join(shapes)}</g>'
           f'<g id="panel-{letter}-labels">{"".join(labels)}</g></g>')
    return svg, py0 + bottom


def key(doc, x0, y0):
    rows = [(EMA, "EMA", "MoCo, BYOL, DINO"), (NEG, "negatives", "SimCLR, MoCo"),
            (BAT, "batch statistics", "Barlow Twins, VICReg")]
    out = ['<g id="key" inkscape:label="colour key">']
    for i, (col, name, tags) in enumerate(rows):
        y = y0 + i * 3.9
        out.append(f'<rect x="{f2(x0)}" y="{f2(y - 1.9)}" width="2.6" height="2.0" rx="0.3" '
                   f'style="fill:{TINT[col]};stroke:{col};stroke-width:0.35"/>')
        out.append(f'<text xml:space="preserve" id="{doc.uid("key")}" x="{f2(x0 + 4.0)}" y="{f2(y)}" '
                   f'style="font-family:{TEXT};font-size:{FS_ANN}px;fill:{INK}">{escape(name)}'
                   f'<tspan style="fill:{GREY};font-size:{FS_TAG}px">{THIN}({escape(tags)})</tspan></text>')
    out.append("</g>")
    return "".join(out), y0 + 2 * 3.9


def svg_doc(doc, w, h, title, body):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
            f'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" width="{f1(w)}mm" height="{f1(h)}mm" '
            f'viewBox="0 0 {f1(w)} {f1(h)}" version="1.1">\n<title>{title}</title>\n'
            f'<sodipodi:namedview id="namedview" pagecolor="#ffffff" inkscape:document-units="mm" units="mm"/>\n'
            f'<defs>{"".join(doc.defs)}</defs>\n'
            f'<g id="layer-figure" inkscape:groupmode="layer" inkscape:label="Figure">{body}</g>\n</svg>\n')


GAP = W - 2 * PW  # 6 mm between columns


def variant_A():
    """2 x 2 small multiples."""
    doc = Doc()
    a, ya = panel(doc, "a", 0, 0.5, "base")
    b, yb = panel(doc, "b", PW + GAP, 0.5, "ema")
    y1 = max(ya, yb) + 5.0
    c, yc = panel(doc, "c", 0, y1, "neg")
    d, yd = panel(doc, "d", PW + GAP, y1, "bat")
    return svg_doc(doc, W, max(yc, yd) + 1.0, "Joint-embedding architectures: small multiples", a + b + c + d)


def variant_B():
    """Base next to the same diagram carrying all three blocks."""
    doc = Doc()
    a, ya = panel(doc, "a", 0, 0.5, "base")
    b, yb = panel(doc, "b", PW + GAP, 0.5, "all")
    k, yk = key(doc, PW + GAP + PW / 2 - 21.0, yb + 4.6)
    return svg_doc(doc, W, max(ya, yk) + 2.0, "Joint-embedding architectures: base and symmetry-breaking blocks",
                   a + b + k)


VARIANTS = {"A": variant_A, "B": variant_B}

# ------------------------------------------------------------------ export
INKSCAPE_ENV = {k: v for k, v in os.environ.items()
                if k not in ("GSETTINGS_SCHEMA_DIR", "GTK_PATH", "GTK_EXE_PREFIX", "GIO_MODULE_DIR",
                             "GDK_PIXBUF_MODULE_FILE", "GDK_PIXBUF_MODULEDIR", "LOCPATH")}
INKSCAPE_ENV["XDG_DATA_DIRS"] = "/usr/local/share:/usr/share"


def final(name):
    """Write the chosen variant as survey/images/joint-embedding.{svg,pdf}."""
    img = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    svg = os.path.join(img, "joint-embedding.svg")
    with open(svg, "w", encoding="utf-8") as fh:
        fh.write(VARIANTS[name]())
    subprocess.run(["inkscape", svg, "--export-type=pdf", "-o", svg[:-4] + ".pdf"], env=INKSCAPE_ENV,
                   capture_output=True, text=True, check=True)
    print(svg[:-4] + ".pdf")


def main(argv):
    if argv and argv[0] == "--final":
        return final(argv[1])
    outdir = argv[0] if argv else "."
    os.makedirs(outdir, exist_ok=True)
    for name, fn in VARIANTS.items():
        svg = os.path.join(outdir, f"joint-embedding_variant_{name}.svg")
        with open(svg, "w", encoding="utf-8") as fh:
            fh.write(fn())
        subprocess.run(["inkscape", svg, "--export-type=png", "--export-dpi=300", "--export-background=#ffffff",
                        "-o", svg[:-4] + ".png"], env=INKSCAPE_ENV, capture_output=True, text=True, check=True)
        print(svg)


if __name__ == "__main__":
    main(sys.argv[1:])
