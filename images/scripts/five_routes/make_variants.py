"""Five routes to invariance: where the group G enters a single training pipeline -- 3 design variants.

Pipeline  D -> f_theta -> R_hat(theta), with G entering at five points:
  1 equivariant architecture  the backbone itself, H subseteq C_G(X, Y)
  2 data augmentation         a sampled g applied to the data, risk averaged over orbits
  3 symmetrization            a wrapper rho_X(g) . f . rho_Y(g)^-1 averaged over G
  4 canonicalization          c = s o pi inserted before the backbone
  5 soft penalty              lambda R(theta) added to the risk
Colours split the routes in two families (Paul Tol, as in the other survey figures):
  green  #117733  model level      (1, 3, 4): every f_theta is G-invariant, exactly;
  indigo #332288  parameter level  (2, 5):    only the selected theta, approximately.

Variant A: one pipeline, model-level cards above, parameter-level cards below, leaders to the entry points.
Variant B: five small multiples, one row per route (same pipeline, the changed block coloured).
Variant C: one pipeline with numbered badges, and a key table (route, entry point, formula).

Units: 1 user unit = 1 mm. Text stays <text> in TeX Gyre Pagella (matches mathpazo), so it is editable;
formulas are laid out with the real font metrics (fontTools) by a small LaTeX-subset engine.
Usage: python3 make_variants.py OUTDIR        (writes five-routes_variant_{A,B,C}.svg and .png previews)
       python3 make_variants.py --final A|B|C (writes survey/images/five-routes.{svg,pdf})
Re-running --final overwrites five-routes.svg / .pdf, including Inkscape edits made to them.
"""
import math
import os
import re
import subprocess
import sys
from xml.sax.saxutils import escape

from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont

W = 138.0  # MDPI \textwidth (mm)
MATH = "'TeX Gyre Pagella Math', 'TeX Gyre Pagella', serif"
TEXT = "'TeX Gyre Pagella', serif"
CAL = "'Latin Modern Math', serif"  # its script letters are the cmsy \mathcal shapes that mathpazo keeps
FS_LAB, FS_TXT, FS_ANN, FS_TAG = 3.2, 2.8, 2.47, 2.2  # 9 pt, 8 pt, 7 pt, 6.2 pt

INK, GREY, MID, LIGHT, RULE = "#222222", "#555555", "#888888", "#bbbbbb", "#e2e2de"
GREEN = "#117733"   # model level: "the symmetry holds" (as in fig:exactness-rotation)
INDIGO = "#332288"  # parameter level: Paul Tol indigo, "parameters" (as in fig:joint-embedding)
TINT = {GREEN: "#e7f1ea", INDIGO: "#e6e4f0"}
WARM = "#FAF9F6"

TEX = "/usr/share/texmf/fonts/opentype/public"
FONT_FILES = {"math": f"{TEX}/tex-gyre-math/texgyrepagella-math.otf",
              "cal": f"{TEX}/lm-math/latinmodern-math.otf",
              "rm": f"{TEX}/tex-gyre/texgyrepagella-regular.otf",
              "bf": f"{TEX}/tex-gyre/texgyrepagella-bold.otf",
              "it": f"{TEX}/tex-gyre/texgyrepagella-italic.otf"}
FAMILY = {"math": MATH, "cal": CAL, "rm": TEXT, "bf": TEXT, "it": TEXT}


def f1(v):
    return f"{v:.1f}"


def f2(v):
    return f"{v:.2f}"


# ================================================================== font metrics
class Metrics:
    def __init__(self, path):
        font = TTFont(path)
        self.upm = font["head"].unitsPerEm
        self.cmap, self.hmtx, self.gs = font.getBestCmap(), font["hmtx"], font.getGlyphSet()
        self.mc, self.ital, self.top = None, {}, {}
        if "MATH" in font:
            t = font["MATH"].table
            self.mc = t.MathConstants
            gi = t.MathGlyphInfo
            if gi.MathItalicsCorrectionInfo:
                ic = gi.MathItalicsCorrectionInfo
                self.ital = {g: r.Value for g, r in zip(ic.Coverage.glyphs, ic.ItalicsCorrection)}
            if gi.MathTopAccentAttachment:
                ta = gi.MathTopAccentAttachment
                self.top = {g: r.Value for g, r in zip(ta.TopAccentCoverage.glyphs, ta.TopAccentAttachment)}
        self._b = {}

    def glyph(self, ch):
        if ord(ch) not in self.cmap:
            raise KeyError(f"glyph U+{ord(ch):04X} {ch!r} missing")
        return self.cmap[ord(ch)]

    def adv(self, ch):
        return self.hmtx[self.glyph(ch)][0] / self.upm

    def bounds(self, ch):
        if ch not in self._b:
            pen = BoundsPen(self.gs)
            self.gs[self.glyph(ch)].draw(pen)
            b = pen.bounds or (0, 0, 0, 0)
            self._b[ch] = tuple(v / self.upm for v in b)
        return self._b[ch]

    def const(self, name):
        v = getattr(self.mc, name)
        return getattr(v, "Value", v) / self.upm if name != "ScriptPercentScaleDown" else v / 100

    def italic(self, ch):
        return self.ital.get(self.glyph(ch), 0) / self.upm

    def top_attach(self, ch):
        g = self.glyph(ch)
        return self.top[g] / self.upm if g in self.top else None


FM = {k: Metrics(p) for k, p in FONT_FILES.items()}
MC = FM["math"]


# ================================================================== boxes
class Box:
    """w: advance; asc/desc: ink extent above/below the baseline (desc >= 0); ops relative to (0, baseline).
    ops: ("t", x, y, text, font, size) or ("r", x, y, w, h) (filled rule)."""

    def __init__(self, w=0.0, asc=0.0, desc=0.0, ops=None, kind="ord", ital=0.0, top=None):
        self.w, self.asc, self.desc, self.ops = w, asc, desc, ops or []
        self.kind, self.ital, self.top = kind, ital, top  # atom class, italic correction, top-accent attach x


def glyph_run(s, font, size, kind="ord"):
    m = FM[font]
    w = sum(m.adv(c) for c in s) * size
    bs = [m.bounds(c) for c in s if not c.isspace()]
    asc = max([b[3] for b in bs] + [0]) * size
    desc = max([-b[1] for b in bs] + [0]) * size
    ital = m.italic(s[-1]) * size if s and m.mc else 0.0
    top = None
    if len(s) == 1 and m.mc:
        t = m.top_attach(s)
        top = t * size if t is not None else None
    return Box(w, asc, desc, [("t", 0.0, 0.0, s, font, size)], kind, ital, top)


def shifted(box, dx, dy):
    out = []
    for op in box.ops:
        if op[0] == "t":
            out.append(("t", op[1] + dx, op[2] + dy, *op[3:]))
        else:
            out.append(("r", op[1] + dx, op[2] + dy, *op[3:]))
    return out


def hcat(boxes, kind="ord"):
    x, ops, asc, desc = 0.0, [], 0.0, 0.0
    for b in boxes:
        ops += shifted(b, x, 0.0)
        asc, desc = max(asc, b.asc), max(desc, b.desc)
        x += b.w
    last = boxes[-1] if boxes else Box()
    return Box(x, asc, desc, ops, kind, last.ital)


# ================================================================== LaTeX subset -> boxes
ITAL = {chr(97 + i): chr(0x1D44E + i) for i in range(26)}
ITAL["h"] = "ℎ"
ITAL.update({chr(65 + i): chr(0x1D434 + i) for i in range(26)})
GREEK = {"theta": "𝜃", "rho": "𝜌", "lambda": "𝜆", "pi": "𝜋", "mu": "𝜇", "sigma": "𝜎", "epsilon": "𝜖",
         "varphi": "𝜑", "phi": "𝜙"}
CALX = {"B": "ℬ", "E": "ℰ", "F": "ℱ", "H": "ℋ", "I": "ℐ", "L": "ℒ", "M": "ℳ", "R": "ℛ"}
BBX = {"C": "ℂ", "H": "ℍ", "N": "ℕ", "P": "ℙ", "Q": "ℚ", "R": "ℝ", "Z": "ℤ"}
SYMS = {"subseteq": ("⊆", "rel"), "in": ("∈", "rel"), "sim": ("∼", "rel"), "circ": ("∘", "bin"),
        "cdot": ("⋅", "bin"), "to": ("→", "rel"), "mapsto": ("↦", "rel"), "le": ("≤", "rel"),
        "sum": ("∑", "op"), "times": ("×", "bin")}
SPACES = {",": 3 / 18, ":": 4 / 18, ";": 5 / 18, "!": -3 / 18, " ": 0.25, "quad": 1.0}
CHARCLS = {"=": "rel", "<": "rel", ">": "rel", "+": "bin", "-": "bin", "(": "open", ")": "close",
           "[": "open", "]": "close", ",": "punct", ";": "punct", "|": "ord"}
TOKEN = re.compile(r"\\[A-Za-z]+|\\.|[{}_^]|\s+|.")


def tokenize(s):
    return TOKEN.findall(s)


class Parser:
    def __init__(self, src):
        self.t, self.i = tokenize(src), 0

    def peek(self, raw=False):
        if not raw:
            while self.i < len(self.t) and self.t[self.i].isspace():
                self.i += 1
        return self.t[self.i] if self.i < len(self.t) else None

    def take(self):
        tok = self.t[self.i]
        self.i += 1
        return tok

    def group_raw(self):
        """Raw text of a {...} group (for \\text, \\mathcal...), or a single token."""
        if self.peek() != "{":
            return self.take()
        self.take()
        depth, out = 1, []  # whitespace tokens are kept: this is raw text
        while True:
            tok = self.take()
            if tok == "{":
                depth += 1
            elif tok == "}":
                depth -= 1
                if depth == 0:
                    return "".join(out)
            out.append(tok)

    def arg(self, size, level):
        if self.peek() == "{":
            self.take()
            b = self.seq(size, level, close="}")
            return b
        return self.atom(size, level)

    def seq(self, size, level, close=None):
        atoms = []
        while self.peek() is not None and self.peek() != close:
            a = self.atom(size, level)
            if a is None:
                continue
            a = self.scripts(a, size, level)
            atoms.append(a)
        if close:
            self.take()
        return space_atoms(atoms, size, level)

    def scripts(self, base, size, level):
        sub = sup = None
        while self.peek() in ("_", "^"):
            which = self.take()
            ss = size * MC.const("ScriptPercentScaleDown")
            arg = self.arg(ss, level + 1)
            if which == "_":
                sub = arg
            else:
                sup = arg
        if sub is None and sup is None:
            return base
        return attach_scripts(base, sub, sup, size)

    def atom(self, size, level):
        tok = self.take()
        if tok.startswith("\\"):
            name = tok[1:]
            if name in SPACES:
                return Box(SPACES[name] * size, kind="space")
            if name in GREEK:
                return glyph_run(GREEK[name], "math", size)
            if name in SYMS:
                ch, kind = SYMS[name]
                return glyph_run(ch, "math", size, kind)
            if name == "mathcal":
                return glyph_run("".join(CALX.get(c, chr(0x1D49C + ord(c) - 65)) for c in self.group_raw()),
                                 "cal", size)
            if name == "mathbb":
                return glyph_run("".join(BBX.get(c, chr(0x1D538 + ord(c) - 65)) for c in self.group_raw()),
                                 "math", size)
            if name in ("mathrm", "operatorname"):
                return glyph_run(self.group_raw(), "math", size)
            if name in ("text", "textit", "textbf"):
                font = {"text": "rm", "textit": "it", "textbf": "bf"}[name]
                return glyph_run(self.group_raw().replace("~", " "), font, size)
            if name in ("hat", "bar", "tilde"):
                base = self.arg(size, level)
                return accent(base, {"hat": "ˆ", "bar": "¯", "tilde": "˜"}[name], size)
            if name in ("frac", "tfrac"):
                ss = size * MC.const("ScriptPercentScaleDown")
                num = self.arg(ss, level + 1)
                den = self.arg(ss, level + 1)
                return fraction(num, den, size)
            if name in ("big", "Big", "left", "right"):
                return None  # delimiters are kept at text size
            if name in ("{", "}", "|"):
                return glyph_run(name if name != "|" else "‖", "math", size, "open" if name == "{" else "close")
            raise ValueError(f"unknown command {tok}")
        if tok == "{":
            return self.seq(size, level, close="}")
        if tok in ITAL:
            return glyph_run(ITAL[tok], "math", size)
        if tok == "-":
            return glyph_run("−", "math", size, "bin")
        return glyph_run(tok, "math", size, CHARCLS.get(tok, "ord"))


THIN, MED, THICK = 3 / 18, 4 / 18, 5 / 18
SPACE_TABLE = {  # TeX inter-atom spacing (text style); script styles keep only the op-related thin spaces
    ("ord", "op"): THIN, ("ord", "bin"): MED, ("ord", "rel"): THICK, ("ord", "inner"): THIN,
    ("op", "ord"): THIN, ("op", "op"): THIN, ("op", "rel"): THICK, ("op", "inner"): THIN,
    ("bin", "ord"): MED, ("bin", "op"): MED, ("bin", "open"): MED, ("bin", "inner"): MED,
    ("rel", "ord"): THICK, ("rel", "op"): THICK, ("rel", "open"): THICK, ("rel", "inner"): THICK,
    ("close", "op"): THIN, ("close", "bin"): MED, ("close", "rel"): THICK, ("close", "inner"): THIN,
    ("punct", "ord"): THIN, ("punct", "op"): THIN, ("punct", "rel"): THIN, ("punct", "open"): THIN,
    ("punct", "close"): THIN, ("punct", "punct"): THIN, ("punct", "inner"): THIN,
    ("inner", "ord"): THIN, ("inner", "op"): THIN, ("inner", "bin"): MED, ("inner", "rel"): THICK,
    ("inner", "open"): THIN, ("inner", "punct"): THIN, ("inner", "inner"): THIN,
    ("bin", "bin"): 0, ("rel", "rel"): 0,
}
SCRIPT_KEEP = {("ord", "op"), ("op", "ord"), ("op", "op"), ("close", "op")}


def space_atoms(atoms, size, level):
    real = [a for a in atoms if a.kind != "space"]
    # bin -> ord when it cannot be binary (TeX rules 5 and 6)
    prev = None
    for a in real:
        if a.kind == "bin" and (prev is None or prev.kind in ("bin", "op", "rel", "open", "punct")):
            a.kind = "ord"
        if a.kind in ("rel", "close", "punct") and prev is not None and prev.kind == "bin":
            prev.kind = "ord"
        prev = a
    if real and real[-1].kind == "bin":
        real[-1].kind = "ord"
    out, prev = [], None
    for a in atoms:
        if a.kind == "space":
            out.append(a)
            continue
        if prev is not None:
            pair = (prev.kind, a.kind)
            gap = SPACE_TABLE.get(pair, 0.0)
            if level > 0 and pair not in SCRIPT_KEEP:
                gap = 0.0
            if gap:
                out.append(Box(gap * size, kind="space"))
        out.append(a)
        prev = a
    kind = "ord"
    if len(real) == 1:
        kind = real[0].kind
    b = hcat(out, kind)
    if len(real) == 1:
        b.top = real[0].top
    return b


def attach_scripts(base, sub, sup, size):
    gap_after = MC.const("SpaceAfterScript") * size
    parts = [("base", base)]
    ops = list(base.ops)
    w = base.w
    asc, desc = base.asc, base.desc
    sub_dy = MC.const("SubscriptShiftDown") * size
    sup_dy = MC.const("SuperscriptShiftUp") * size
    if sub is not None:
        sub_dy = max(sub_dy, sub.asc - MC.const("SubscriptTopMax") * size)
    if sup is not None:
        sup_dy = max(sup_dy, sup.desc + MC.const("SuperscriptBottomMin") * size)
    if sub is not None and sup is not None:
        gap = (sup_dy - sup.desc) - (sub.asc - sub_dy)
        need = MC.const("SubSuperscriptGapMin") * size
        if gap < need:
            sub_dy += need - gap
    ext = 0.0
    if sup is not None:
        x = base.w + (base.ital if base.kind != "op" else 0.0)
        ops += shifted(sup, x, -sup_dy)
        asc = max(asc, sup_dy + sup.asc)
        ext = max(ext, x + sup.w)
    if sub is not None:
        x = base.w
        ops += shifted(sub, x, sub_dy)
        desc = max(desc, sub_dy + sub.desc)
        ext = max(ext, x + sub.w)
    del parts
    return Box(ext + gap_after, asc, desc, ops, base.kind, 0.0)


def fraction(num, den, size):
    axis = MC.const("AxisHeight") * size
    rule = MC.const("FractionRuleThickness") * size
    nu = MC.const("FractionNumeratorShiftUp") * size
    dd = MC.const("FractionDenominatorShiftDown") * size
    gmin = MC.const("FractionNumeratorGapMin") * size
    nu = max(nu, axis + rule / 2 + gmin + num.desc)
    dd = max(dd, den.asc + gmin - axis + rule / 2)
    pad = 0.12 * size
    w = max(num.w, den.w) + 2 * pad
    ops = shifted(num, (w - num.w) / 2, -nu) + shifted(den, (w - den.w) / 2, dd)
    ops.append(("r", 0.0, -axis - rule / 2, w, rule))
    sp = THIN * size * 0.5
    b = Box(w, nu + num.asc, dd + den.desc, shifted(Box(ops=ops), sp, 0), "inner")
    b.w += 2 * sp
    return b


def accent(base, ch, size):
    m = MC
    bx0, by0, bx1, by1 = (v * size for v in m.bounds(ch))
    attach = base.top if base.top is not None else base.w / 2 + 0.08 * size
    x = attach - (bx0 + bx1) / 2
    abh = m.const("AccentBaseHeight") * size
    dy = max(0.0, base.asc - abh)  # accents are designed to sit on a base of height AccentBaseHeight
    ops = list(base.ops) + [("t", x, -dy, ch, "math", size)]
    asc = max(base.asc, dy + by1)
    return Box(base.w, asc, base.desc, ops, base.kind, base.ital, base.top)


def tex(src, size=FS_TXT):
    return Parser(src).seq(size, 0)


# ================================================================== SVG emitters
class Doc:
    """Collects layers, plus the geometry used by the validator."""

    def __init__(self):
        self.layers = []       # (id, label, [svg strings])
        self.texts = {}        # text id -> container id (or None)
        self.frames = {}       # container id -> (x, y, w, h)
        self.segments = []     # line segments that text must not cross
        self.ids = set()

    def uid(self, base):
        gid, k = base, 2
        while gid in self.ids:
            gid, k = f"{base}-{k}", k + 1
        self.ids.add(gid)
        return gid

    def layer(self, lid, label):
        parts = []
        self.layers.append((lid, label, parts))
        return parts


def math_svg(doc, gid, box, x, y, anchor="start", color=INK, container=None, weight=None):
    """Render a Box with its baseline at y; anchor start/middle/end on its advance width."""
    if anchor == "middle":
        x -= box.w / 2
    elif anchor == "end":
        x -= box.w
    gid = doc.uid(gid)
    spans, rules = [], []
    for op in box.ops:
        if op[0] == "t":
            _, dx, dy, s, font, size = op
            st = f"font-family:{FAMILY[font]};font-size:{f2(size)}px"
            if font == "bf" or weight == "bold":
                st += ";font-weight:bold"
            if font == "it":
                st += ";font-style:italic"
            spans.append(f'<tspan x="{f2(x + dx)}" y="{f2(y + dy)}" style="{st}">{escape(s)}</tspan>')
        else:
            _, dx, dy, w, h = op
            rules.append(f'<rect id="{gid}-rule{len(rules)}" x="{f2(x + dx)}" y="{f2(y + dy)}" width="{f2(w)}" '
                         f'height="{f2(h)}" style="fill:{color};stroke:none"/>')
    doc.texts[f"{gid}-t"] = container
    t = (f'<text id="{gid}-t" xml:space="preserve" style="font-style:normal;font-weight:normal;fill:{color};'
         f'stroke:none">{"".join(spans)}</text>')
    return f'<g id="{gid}">{t}{"".join(rules)}</g>'


def text_svg(doc, gid, s, x, y, size=FS_TXT, font="rm", anchor="start", color=INK, container=None):
    return math_svg(doc, gid, glyph_run(s, font, size), x, y, anchor, color, container)


def rect(doc, gid, x, y, w, h, stroke=GREY, fill="#ffffff", sw=0.3, rx=1.2, dash=None, frame=True, opacity=1.0):
    gid = doc.uid(gid)
    if frame:
        doc.frames[gid] = (x, y, w, h)
    d = f";stroke-dasharray:{dash}" if dash else ""
    fo = f";fill-opacity:{opacity}" if opacity < 1 else ""
    return (f'<rect id="{gid}" x="{f1(x)}" y="{f1(y)}" width="{f1(w)}" height="{f1(h)}" rx="{f1(rx)}" '
            f'style="fill:{fill}{fo};stroke:{stroke};stroke-width:{sw}{d}"/>')


def head(x, y, ux, uy, color, L=1.4, Wd=1.1):
    """Filled arrowhead with its tip at (x, y), pointing along the unit vector (ux, uy)."""
    bx, by = x - L * ux, y - L * uy
    px, py = -uy * Wd / 2, ux * Wd / 2
    return (f'<path d="M {f2(x)},{f2(y)} L {f2(bx + px)},{f2(by + py)} L {f2(bx - px)},{f2(by - py)} Z" '
            f'style="fill:{color};stroke:none"/>')


def arrow(doc, gid, x1, y, x2, color=GREY, sw=0.35, tip=True):
    gid = doc.uid(gid)
    doc.segments.append((x1, y, x2, y))
    end = x2 - (1.2 if tip else 0)
    h = head(x2, y, 1, 0, color) if tip else ""
    return (f'<g id="{gid}"><path d="M {f2(x1)},{f2(y)} L {f2(end)},{f2(y)}" '
            f'style="fill:none;stroke:{color};stroke-width:{sw}"/>{h}</g>')


def leader(doc, gid, x1, y1, x2, y2, color, dot=True):
    """Dotted leader from a card (x1, y1) to an entry point (x2, y2), vertical tangents at both ends."""
    gid = doc.uid(gid)
    ym = (y1 + y2) / 2
    n = 12
    for k in range(n):  # polyline approximation of the Bezier, for the validator
        t0, t1 = k / n, (k + 1) / n
        doc.segments.append((*bez(x1, y1, x2, y2, ym, t0), *bez(x1, y1, x2, y2, ym, t1)))
    d = (f"M {f2(x1)},{f2(y1)} C {f2(x1)},{f2(ym)} {f2(x2)},{f2(ym)} {f2(x2)},{f2(y2)}"
         if abs(x1 - x2) > 0.05 else f"M {f2(x1)},{f2(y1)} L {f2(x2)},{f2(y2)}")
    dt = f'<circle cx="{f2(x2)}" cy="{f2(y2)}" r="0.75" style="fill:{color};stroke:#ffffff;stroke-width:0.25"/>'
    return (f'<g id="{gid}"><path d="{d}" style="fill:none;stroke:{color};stroke-width:0.4;'
            f'stroke-dasharray:0.1,0.9;stroke-linecap:round"/>{dt if dot else ""}</g>')


def bez(x1, y1, x2, y2, ym, t):
    p = [(x1, y1), (x1, ym), (x2, ym), (x2, y2)]
    c = [(1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3]
    return sum(ci * q[0] for ci, q in zip(c, p)), sum(ci * q[1] for ci, q in zip(c, p))


def badge(doc, gid, cx, cy, n, color, r=1.9):
    gid = doc.uid(gid)
    size = 2.5
    b = glyph_run(str(n), "bf", size)
    by0, by1 = FM["bf"].bounds(str(n))[1] * size, FM["bf"].bounds(str(n))[3] * size
    y = cy + (by0 + by1) / 2
    doc.frames[gid] = (cx - r, cy - r, 2 * r, 2 * r)
    t = math_svg(doc, f"{gid}-n", b, cx, y, "middle", "#ffffff", container=None)
    doc.texts[f"{gid}-n-t"] = "badge"
    return (f'<g id="{gid}"><circle cx="{f2(cx)}" cy="{f2(cy)}" r="{f2(r)}" style="fill:{color};stroke:none"/>'
            f'{t}</g>')


def box_label(doc, gid, src, cx, cy, size=FS_TXT, color=INK, container=None):
    """Formula centred (on its ink) at (cx, cy)."""
    b = tex(src, size)
    y = cy + (b.asc - b.desc) / 2
    return math_svg(doc, gid, b, cx, y, "middle", color, container)


def svg_doc(doc, w, h, title, bg=None):
    body = "".join(f'<g id="layer-{lid}" inkscape:groupmode="layer" inkscape:label="{lab}">{"".join(p)}</g>\n'
                   for lid, lab, p in doc.layers)
    back = (f'<rect id="background" x="0" y="0" width="{f1(w)}" height="{f1(h)}" style="fill:{bg};stroke:none"/>'
            if bg else "")
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
            f'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" width="{f1(w)}mm" height="{f1(h)}mm" '
            f'viewBox="0 0 {f1(w)} {f1(h)}" version="1.1">\n<title>{title}</title>\n'
            f'<sodipodi:namedview id="namedview" pagecolor="#ffffff" inkscape:document-units="mm" units="mm"/>\n'
            f'{back}{body}</svg>\n')


# ================================================================== content
ROUTES = {  # n: (name, family colour, entry point (short), formula lines)
    1: ("Equivariant architecture", GREEN, "the hypothesis class",
        [r"\mathcal{H}\subseteq C_G(\mathcal{X},\mathcal{Y})"]),
    2: ("Data augmentation", INDIGO, "the risk, via the data",
        [r"\hat{R}_G(\theta)=\tfrac{1}{n}\sum_i\mathbb{E}_g\,L(f_\theta(\rho_X(g)x_i),\,\rho_Y(g)y_i)"]),
    3: ("Averaging", GREEN, "around the backbone",
        [r"\bar{f}(x)=\tfrac{1}{|G|}\sum_g\rho_Y(g)^{-1}f(\rho_X(g)x)"]),
    4: ("Canonicalization", GREEN, "before the backbone",
        [r"f\circ c\;\;\text{with}\;\;c=s\circ\pi"]),
    5: ("Soft penalty", INDIGO, "the loss",
        [r"\mathcal{L}(\theta)=\hat{R}(\theta)+\lambda\,\mathcal{R}(\theta)",
         r"\mathcal{R}(\theta)=\mathbb{E}_{x,g}\,d_Y(f_\theta(\rho_X(g)x),\,\rho_Y(g)f_\theta(x))"]),
}
FAMILIES = [(GREEN, r"\textbf{Model level:}\text{~exact, for every~}\theta"),
            (INDIGO, r"\textbf{Parameter level:}\text{~learned, approximate}")]


def fit(src, width, size=FS_TXT, smin=2.45):
    """Largest size <= size (step 0.05) at which the formula fits in width."""
    s = size
    while s > smin and tex(src, s).w > width:
        s -= 0.05
    return s


# ------------------------------------------------------------------ the full pipeline (variants A and C)
def full_pipeline(doc, y, x0, colored=True):
    """D -> (g) -> [c] -> [rho_X(g) -> f_theta -> rho_Y(g)^-1] -> [R_hat(theta)][+lambda R(theta)].
    Optional blocks (one per route) are dashed in their family colour. Returns the entry points."""
    L_mod, L_box, L_arr, L_conn = (doc.layer("modules", "G-modules (dashed)"), doc.layer("blocks", "Pipeline blocks"),
                                   doc.layer("connectors", "Connectors"), doc.layer("blocklabels", "Block labels"))
    h = 8.0
    gap = 11.0
    # x layout
    xD, wD = x0, 9.0
    gx = xD + wD + gap + 2.6                      # g node centre (DA)
    xc, wc = gx + 2.6 + gap, 7.0                  # canonicalizer
    xW = xc + wc + gap                            # wrapper (symmetrization)
    in_w, wf = 11.5, 10.0
    out_w = 13.0
    wW = in_w + wf + out_w
    xf = xW + in_w
    xL, wL = xW + wW + gap, 11.0                  # risk box
    wP = 15.0                                     # penalty extension
    gcol = GREEN if colored else GREY
    icol = INDIGO if colored else GREY
    # blocks
    L_box.append(rect(doc, "block-data", xD, y - h / 2, wD, h))
    L_lab_append = L_conn.append
    L_conn.append(box_label(doc, "label-data", r"\mathcal{D}", xD + wD / 2, y, container="block-data"))
    L_mod.append(f'<circle id="{doc.uid("module-g")}" cx="{f2(gx)}" cy="{f2(y)}" r="2.6" '
                 f'style="fill:{TINT[INDIGO]};stroke:{icol};stroke-width:0.3;stroke-dasharray:1.0,0.6"/>')
    doc.frames["module-g"] = (gx - 1.9, y - 1.9, 3.8, 3.8)
    L_conn.append(box_label(doc, "label-g", "g", gx, y, container="module-g", color=INDIGO))
    L_mod.append(rect(doc, "module-c", xc, y - h / 2, wc, h, stroke=gcol, fill=TINT[GREEN], dash="1.0,0.6"))
    L_conn.append(box_label(doc, "label-c", "c", xc + wc / 2, y, container="module-c", color=GREEN))
    hW = 13.0
    L_mod.append(rect(doc, "module-wrapper", xW, y - hW / 2, wW, hW, stroke=gcol, fill=TINT[GREEN], dash="1.0,0.6",
                      rx=1.8))
    L_box.append(rect(doc, "block-f", xf, y - h / 2, wf, h))
    L_conn.append(box_label(doc, "label-f", r"f_\theta", xf + wf / 2, y, container="block-f"))
    L_box.append(rect(doc, "block-risk", xL, y - h / 2, wL, h))
    L_conn.append(box_label(doc, "label-risk", r"\hat{R}(\theta)", xL + wL / 2, y, container="block-risk"))
    L_mod.append(rect(doc, "module-penalty", xL + wL, y - h / 2, wP, h, stroke=icol, fill=TINT[INDIGO],
                      dash="1.0,0.6"))
    L_conn.append(box_label(doc, "label-penalty", r"+\,\lambda\mathcal{R}(\theta)", xL + wL + wP / 2, y,
                            container="module-penalty", color=INDIGO))
    # connectors
    L_arr.append(arrow(doc, "conn-data-g", xD + wD, y, gx - 2.6))
    L_arr.append(arrow(doc, "conn-g-c", gx + 2.6, y, xc))
    L_arr.append(arrow(doc, "conn-c-wrap", xc + wc, y, xf))
    L_arr.append(arrow(doc, "conn-wrap-risk", xf + wf, y, xL))
    # labels inside the wrapper, above the line
    ly = y - 1.3
    L_conn.append(math_svg(doc, "label-rhoX", tex(r"\rho_X(g)", FS_TAG), xW + in_w / 2, ly, "middle", GREEN,
                           container="module-wrapper"))
    L_conn.append(math_svg(doc, "label-rhoY", tex(r"\rho_Y(g)^{-1}", FS_TAG), xf + wf + out_w / 2, ly, "middle",
                           GREEN, container="module-wrapper"))
    L_conn.append(math_svg(doc, "label-x", tex("x", FS_ANN), (xD + wD + gx - 2.6) / 2, y - 1.4, "middle", GREY))
    del L_lab_append
    return {"data": (xD + wD / 2, y - h / 2), "g": (gx, y - 2.6), "c": (xc + wc / 2, y - h / 2),
            "f": (xf + wf / 2, y - h / 2), "wrap": (xW + wW - 4.0, y - hW / 2),
            "pen": (xL + wL + wP / 2, y - h / 2), "pen_bot": (xL + wL + wP / 2, y + h / 2),
            "g_bot": (gx, y + 2.6), "wrap_top": y - hW / 2, "wrap_bot": y + hW / 2, "right": xL + wL + wP,
            "risk": (xL + wL / 2, y - h / 2)}


ENTRY = {1: "f", 2: "g", 3: "wrap", 4: "c", 5: "pen"}


# ------------------------------------------------------------------ variant A: cards + leaders
def card(doc, n, x, y, w, h, style="tint"):
    name, col, _, lines = ROUTES[n]
    L = doc.layer(f"card-{n}", f"Card {n}: {name}")
    fid = f"card-{n}"
    L.append(rect(doc, fid, x, y, w, h, stroke=col, fill=TINT[col] if style == "tint" else "#ffffff", sw=0.3,
                  rx=1.5, opacity=0.55 if style == "tint" else 1.0))
    L.append(badge(doc, f"card-{n}-badge", x + 3.2, y + 3.4, n, col))
    L.append(text_svg(doc, f"card-{n}-name", name, x + 6.2, y + 4.35, FS_TXT, "bf", color=INK, container=fid))
    nl = len(lines)
    step = 4.4
    y0 = y + 11.0 if nl > 1 or h < 16 else y + 11.0 + step / 2  # one-line formula of a tall card: centred
    for i, src in enumerate(lines):
        s = fit(src, w - 4.0)
        L.append(math_svg(doc, f"card-{n}-formula{i + 1}", tex(src, s), x + w / 2, y0 + i * step, "middle", INK,
                          container=fid))
    return L


def variant_A():
    doc = Doc()
    m = 3.0
    top_y, top_h = 6.2, 14.6
    pipe_y = top_y + top_h + 15.5
    E = full_pipeline(doc, pipe_y, 4.0)
    bot_y, bot_h = pipe_y + 6.5 + 9.0, 18.6
    # cards: top = model level, bottom = parameter level
    wt = (W - 2 * m - 2 * 3.0) / 3
    tops = {4: m, 1: m + wt + 3.0, 3: m + 2 * (wt + 3.0)}
    for n, x in tops.items():
        card(doc, n, x, top_y, wt, top_h)
    wb = (W - 2 * m - 3.0) / 2
    bots = {2: m, 5: m + wb + 3.0}
    for n, x in bots.items():
        card(doc, n, x, bot_y, wb, bot_h)
    # family headers
    Lh = doc.layer("families", "Family headers")
    Lh.append(math_svg(doc, "header-model", tex(FAMILIES[0][1], FS_ANN), m, top_y - 2.2, "start", GREEN))
    Lh.append(math_svg(doc, "header-param", tex(FAMILIES[1][1], FS_ANN), m, bot_y + bot_h + 4.0, "start", INDIGO))
    # leaders
    Ll = doc.layer("leaders", "Leaders (card -> entry point)")
    for n, x in tops.items():
        ex, ey = E[ENTRY[n]]
        sx = min(max(ex, x + 6.0), x + wt - 6.0)
        Ll.append(leader(doc, f"leader-{n}", sx, top_y + top_h, ex, ey, ROUTES[n][1]))
    for n, x in bots.items():
        key = {2: "g_bot", 5: "pen_bot"}[n]
        ex, ey = E[key]
        sx = min(max(ex, x + 6.0), x + wb - 6.0)
        Ll.append(leader(doc, f"leader-{n}", sx, bot_y, ex, ey, ROUTES[n][1]))
    H = bot_y + bot_h + 6.0
    return doc, H, "Five routes to invariance: cards and pipeline"


# ------------------------------------------------------------------ variant B: small multiples
MINI_W = 8.0 + 10.0 + 6.0 + 10.0 + 9.0 + 15.0 + 13.0  # mini pipeline width before stretching (mm)


def mini_pipeline(doc, n, y, x0, extra=0.0):
    """Same pipeline in every row; only the block where G enters is present and coloured.
    extra (mm) lengthens the connectors: 1/4 before the slot, 1/4 after it, 1/2 before the loss."""
    col = ROUTES[n][1]
    Lb = doc.layer(f"row-{n}-pipeline", f"Row {n}: pipeline")
    h = 6.4
    xD, wD = x0, 8.0
    xs = xD + wD + 10.0 + extra / 4  # slot for the g node / canonicalizer
    ws = 6.0
    xf, wf = xs + ws + 10.0 + extra / 4, 9.0
    xL, wL = xf + wf + 15.0 + extra / 2, 13.0
    pre = f"row{n}"
    Lb.append(rect(doc, f"{pre}-data", xD, y - h / 2, wD, h))
    Lb.append(box_label(doc, f"{pre}-label-data", r"\mathcal{D}", xD + wD / 2, y, FS_ANN, container=f"{pre}-data"))
    if n == 1:
        Lb.append(rect(doc, f"{pre}-f", xf, y - h / 2, wf, h, stroke=col, fill=TINT[col], sw=0.45))
        Lb.append(box_label(doc, f"{pre}-label-f", r"f_\theta", xf + wf / 2, y, FS_ANN, col, f"{pre}-f"))
    else:
        Lb.append(rect(doc, f"{pre}-f", xf, y - h / 2, wf, h))
        Lb.append(box_label(doc, f"{pre}-label-f", r"f_\theta", xf + wf / 2, y, FS_ANN, container=f"{pre}-f"))
    if n == 5:
        Lb.append(rect(doc, f"{pre}-loss", xL, y - h / 2, wL, h, stroke=col, fill=TINT[col], sw=0.45))
        Lb.append(box_label(doc, f"{pre}-label-loss", r"\mathcal{L}+\lambda\mathcal{R}", xL + wL / 2, y, FS_ANN,
                            col, f"{pre}-loss"))
    else:
        Lb.append(rect(doc, f"{pre}-loss", xL, y - h / 2, wL, h))
        Lb.append(box_label(doc, f"{pre}-label-loss", r"\mathcal{L}", xL + wL / 2, y, FS_ANN,
                            container=f"{pre}-loss"))
    if n == 2:
        cx = xs + ws / 2
        Lb.append(f'<circle id="{doc.uid(pre + "-g")}" cx="{f2(cx)}" cy="{f2(y)}" r="2.5" '
                  f'style="fill:{TINT[col]};stroke:{col};stroke-width:0.45"/>')
        doc.frames[f"{pre}-g"] = (cx - 1.8, y - 1.8, 3.6, 3.6)
        Lb.append(box_label(doc, f"{pre}-label-g", "g", cx, y, FS_ANN, col, f"{pre}-g"))
        Lb.append(arrow(doc, f"{pre}-conn1", xD + wD, y, cx - 2.5))
        Lb.append(arrow(doc, f"{pre}-conn2", cx + 2.5, y, xf))
    elif n == 4:
        Lb.append(rect(doc, f"{pre}-c", xs, y - h / 2, ws, h, stroke=col, fill=TINT[col], sw=0.45))
        Lb.append(box_label(doc, f"{pre}-label-c", "c", xs + ws / 2, y, FS_ANN, col, f"{pre}-c"))
        Lb.append(arrow(doc, f"{pre}-conn1", xD + wD, y, xs))
        Lb.append(arrow(doc, f"{pre}-conn2", xs + ws, y, xf))
    elif n == 3:
        pad = 5.2
        hW = h + 3.2
        Lb.insert(0, rect(doc, f"{pre}-wrap", xf - pad, y - hW / 2, wf + 2 * pad, hW, stroke=col, fill=TINT[col],
                          sw=0.45, rx=1.6))
        Lb.append(arrow(doc, f"{pre}-conn1", xD + wD, y, xf))
        Lb.append(math_svg(doc, f"{pre}-label-gin", tex("g", FS_TAG), xf - pad / 2, y - 1.4, "middle", col,
                           f"{pre}-wrap"))
        Lb.append(math_svg(doc, f"{pre}-label-gout", tex("g^{-1}", FS_TAG), xf + wf + pad / 2, y - 1.4, "middle",
                           col, f"{pre}-wrap"))
    else:
        Lb.append(arrow(doc, f"{pre}-conn1", xD + wD, y, xf))
    Lb.append(arrow(doc, f"{pre}-conn3", xf + wf, y, xL))
    return xL + wL


def variant_B():
    doc = Doc()
    h = 11.0
    y = 2.0
    x0 = 8.5
    name_w = max(glyph_run(ROUTES[n][0], "bf", FS_TXT).w for n in ROUTES)
    xt = W - 2.0 - name_w                     # names: left-aligned column flush with the right margin
    extra = xt - 7.0 - (x0 + MINI_W)          # the pipelines stretch to keep a 7 mm gap before the names
    cap = FM["bf"].bounds("H")[3] * FS_TXT    # names are centred on their cap height
    Lr = doc.layer("rules", "Row rules")
    for n in range(1, 6):
        name, col = ROUTES[n][:2]
        cy = y + h / 2
        Lt = doc.layer(f"row-{n}-text", f"Row {n}: badge and name")
        Lt.append(badge(doc, f"row{n}-badge", 3.6, cy, n, col))
        mini_pipeline(doc, n, cy, x0, extra)
        Lt.append(text_svg(doc, f"row{n}-name", name, xt, cy + cap / 2, FS_TXT, "bf", color=INK))
        y += h
        if n < 5:
            Lr.append(f'<line id="{doc.uid(f"rule-{n}")}" x1="1.0" y1="{f1(y)}" x2="{f1(W - 1.0)}" y2="{f1(y)}" '
                      f'style="stroke:{RULE};stroke-width:0.25"/>')
    # legend
    Lg = doc.layer("legend", "Legend")
    ly = y + 4.6
    x = 2.0
    for col, src in FAMILIES:
        Lg.append(rect(doc, f"legend-swatch-{col[1:]}", x, ly - 2.3, 3.6, 2.6, stroke=col, fill=TINT[col], sw=0.45,
                       rx=0.5, frame=False))
        b = tex(src, FS_ANN)
        Lg.append(math_svg(doc, f"legend-{col[1:]}", b, x + 5.0, ly, "start", col))
        x += 5.0 + b.w + 7.0
    H = ly + 3.0
    return doc, H, "Five routes to invariance: small multiples"


# ------------------------------------------------------------------ variant C: badges + key table
def variant_C():
    doc = Doc()
    band_y, band_h = 2.0, 27.0
    Lbg = doc.layer("band", "Pipeline band")
    Lbg.append(rect(doc, "band", 1.0, band_y, W - 2.0, band_h, stroke="none", fill=WARM, rx=2.0, frame=False))
    pipe_y = band_y + 17.0
    E = full_pipeline(doc, pipe_y, 6.5)
    Lb = doc.layer("badges", "Entry badges")
    by = E["wrap_top"] - 4.6
    for n in range(1, 6):
        ex, ey = E[ENTRY[n]]
        col = ROUTES[n][1]
        x2 = ex
        Lb.append(f'<line id="{doc.uid(f"tick-{n}")}" x1="{f2(ex)}" y1="{f2(by + 1.9)}" x2="{f2(x2)}" '
                  f'y2="{f2(ey)}" style="stroke:{col};stroke-width:0.35"/>')
        doc.segments.append((ex, by + 1.9, x2, ey))
        Lb.append(badge(doc, f"entry-badge-{n}", ex, by, n, col))
    # key table
    Lk = doc.layer("key", "Key table")
    cols = [2.0, 8.0, 44.0, 76.0]  # badge, name, entry, formula
    ty = band_y + band_h + 6.2
    Lk.append(text_svg(doc, "head-route", "route", cols[1], ty, FS_TAG, "it", color=MID))
    Lk.append(math_svg(doc, "head-entry", tex(r"\textit{where~}G\textit{~enters}", FS_TAG), cols[2], ty, "start",
                       MID))
    Lk.append(text_svg(doc, "head-formula", "formula", cols[3], ty, FS_TAG, "it", color=MID))
    y = ty + 1.6
    Lk.append(f'<line id="rule-head" x1="1.0" y1="{f1(y)}" x2="{f1(W - 1.0)}" y2="{f1(y)}" '
              f'style="stroke:{LIGHT};stroke-width:0.3"/>')
    for n in range(1, 6):
        name, col, entry, lines = ROUTES[n]
        h = 6.4 + 4.4 * (len(lines) - 1)
        cy = y + 3.2 + 0.4
        Lk.append(badge(doc, f"key-badge-{n}", cols[0] + 2.0, cy - 0.95, n, col, r=1.7))
        Lk.append(text_svg(doc, f"key-name-{n}", name, cols[1], cy, FS_TXT, "bf"))
        Lk.append(text_svg(doc, f"key-entry-{n}", entry, cols[2], cy, FS_TXT, "rm", color=GREY))
        for i, src in enumerate(lines):
            s = fit(src, W - cols[3] - 2.0, FS_TXT)
            Lk.append(math_svg(doc, f"key-formula-{n}-{i + 1}", tex(src, s), cols[3], cy + 4.4 * i, "start"))
        y += h
        Lk.append(f'<line id="{doc.uid(f"rule-{n}")}" x1="1.0" y1="{f1(y)}" x2="{f1(W - 1.0)}" y2="{f1(y)}" '
                  f'style="stroke:{RULE if n < 5 else LIGHT};stroke-width:{0.25 if n < 5 else 0.3}"/>')
    Lg = doc.layer("legend", "Legend")
    ly = y + 4.4
    x = 2.0
    for col, src in FAMILIES:
        Lg.append(f'<circle cx="{f2(x + 1.3)}" cy="{f2(ly - 0.9)}" r="1.3" style="fill:{col};stroke:none"/>')
        b = tex(src, FS_ANN)
        Lg.append(math_svg(doc, f"legend-{col[1:]}", b, x + 3.6, ly, "start", col))
        x += 3.6 + b.w + 7.0
    H = ly + 2.6
    return doc, H, "Five routes to invariance: badges and key"


VARIANTS = {"A": variant_A, "B": variant_B, "C": variant_C}


# ================================================================== validation (real bboxes from Inkscape)
INKSCAPE_ENV = {k: v for k, v in os.environ.items()
                if k not in ("GSETTINGS_SCHEMA_DIR", "GTK_PATH", "GTK_EXE_PREFIX", "GIO_MODULE_DIR",
                             "GDK_PIXBUF_MODULE_FILE", "GDK_PIXBUF_MODULEDIR", "LOCPATH")}
INKSCAPE_ENV["XDG_DATA_DIRS"] = "/usr/local/share:/usr/share"


def inkscape(*args):
    return subprocess.run(["inkscape", *args], env=INKSCAPE_ENV, capture_output=True, text=True).stdout


def overlap(a, b, tol=0.0):
    return (a[0] + tol < b[0] + b[2] and b[0] + tol < a[0] + a[2]
            and a[1] + tol < b[1] + b[3] and b[1] + tol < a[1] + a[3])


def seg_hits(seg, b):
    x1, y1, x2, y2 = seg
    for i in range(41):
        t = i / 40
        x, y = x1 + t * (x2 - x1), y1 + t * (y2 - y1)
        if b[0] < x < b[0] + b[2] and b[1] < y < b[1] + b[3]:
            return True
    return False


def validate(path, doc, page):
    px = 96 / 25.4
    bb = {}
    for ln in inkscape(path, "--query-all").splitlines():
        p = ln.split(",")
        if len(p) == 5:
            bb[p[0]] = tuple(float(v) / px for v in p[1:])
    issues = []
    tids = [t for t in doc.texts if t in bb]
    missing = [t for t in doc.texts if t not in bb]
    if missing:
        issues.append(f"no bbox for {missing[:5]}")
    for t in tids:
        x, y, w, h = bb[t]
        if x < 0.5 or y < 0.5 or x + w > page[0] - 0.5 or y + h > page[1] - 0.5:
            issues.append(f"{t} outside the page margin")
        cont = doc.texts[t]
        if cont and cont in doc.frames:
            fx, fy, fw, fh = doc.frames[cont]
            mg = min(x - fx, y - fy, fx + fw - x - w, fy + fh - y - h)
            if mg < 0.5:
                issues.append(f"{t}: only {mg:.2f} mm inside {cont}")
        for fid, fb in doc.frames.items():
            if fid == cont or cont == "badge" and t.startswith(fid):
                continue
            if t.startswith(fid + "-"):  # own badge / own frame
                continue
            if not (cont and fid == cont) and overlap(bb[t], fb, tol=0.05) and not (
                    cont and overlap(doc.frames.get(cont, (0, 0, 0, 0)), fb)):
                issues.append(f"{t} overlaps frame {fid}")
        shrunk = (x + 0.12, y + 0.12, w - 0.24, h - 0.24)
        for seg in doc.segments:
            if seg_hits(seg, shrunk):
                issues.append(f"{t} crossed by a line at ({seg[0]:.1f},{seg[1]:.1f})")
                break
    for i, a in enumerate(tids):
        for b in tids[i + 1:]:
            if overlap(bb[a], bb[b], tol=0.05):
                issues.append(f"text overlap: {a} / {b}")
    return issues


def build(name):
    doc, H, title = VARIANTS[name]()
    return svg_doc(doc, W, H, title), doc, (W, H)


def final(name):
    img = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    svg_path = os.path.join(img, "five-routes.svg")
    svg, _, _ = build(name)
    with open(svg_path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    subprocess.run(["inkscape", svg_path, "--export-type=pdf", "-o", svg_path[:-4] + ".pdf"], env=INKSCAPE_ENV,
                   capture_output=True, text=True, check=True)
    print(svg_path[:-4] + ".pdf")


def main(argv):
    if argv and argv[0] == "--final":
        return final(argv[1] if len(argv) > 1 else "B")
    outdir = argv[0] if argv else "."
    os.makedirs(outdir, exist_ok=True)
    for name in VARIANTS:
        svg, doc, page = build(name)
        path = os.path.join(outdir, f"five-routes_variant_{name}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg)
        issues = validate(path, doc, page)
        subprocess.run(["inkscape", path, "--export-type=png", "--export-dpi=300", "--export-background=#ffffff",
                        "-o", path[:-4] + ".png"], env=INKSCAPE_ENV, capture_output=True, text=True, check=True)
        print(f"[{name}] {path}: {page[0]:.1f} x {page[1]:.1f} mm -- {len(issues)} layout issue(s)")
        for it in issues[:40]:
            print("   ", it)


if __name__ == "__main__":
    main(sys.argv[1:])
