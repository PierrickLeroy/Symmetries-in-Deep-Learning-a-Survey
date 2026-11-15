"""One rotation, several forms (ex:one-rotation-several-forms) -- 3 design variants, 69 x 69 mm (half \\textwidth).

G = C_4 = {e, r, r^2, r^3} acts on the input space X = R^2 by rho_X(r) = R_{pi/2}. The input x is the position of a
laser lamp in the upper-left corner of a square canvas; the lamp aims a purple ray through the origin, so the ray
carries an orientation. The three rotated copies r x, r^2 x, r^3 x are drawn faded, each tagged with its element.
Outputs, one per item of the example; f(g x) is drawn for the four g (f(x) opaque, the three others faded):
  1 orientation  Y = [0, 2 pi):  four distinct arrows,            rho_Y(G) = C_4
  2 axis         Y = [0, pi):    two axes, e ~ r^2 and r ~ r^3,   rho_Y(G) = C_2
  3 class        Y = {on, off}:  the four copies share the label, rho_Y(G) = {id}
A grey arc marks the action of r in each space (rho_X(r) on the canvas, rho_Y(r) on each output).

Variant A: input on top, the three outputs in a row below.
Variant B: 2 x 2 grid, input in the top-left cell.
Variant C: input on the left, the three outputs stacked in a column on the right.
Variant D: the input canvas alone fills the figure; e is the upper-right lamp (r, r^2, r^3 follow counter-clockwise).
Every ray is solid from its lamp, through the origin, to the aperture of the opposite lamp.

Units: 1 user unit = 1 mm. Text stays <text> in TeX Gyre Pagella (matches mathpazo), so it is editable.
Colours follow the other survey figures (Paul Tol neutrals, light-grey domains); the ray is purple.
Usage: python3 make_variants.py OUTDIR           (writes one-rotation_variant_{A,B,C,D}.svg and .png previews)
       python3 make_variants.py --final A|B|C|D  (writes survey/images/one-rotation.{svg,pdf}; default D)
Re-running --final overwrites one-rotation.svg / .pdf, including Inkscape edits made to them.
"""
import math
import os
import subprocess
import sys

MATH = "'TeX Gyre Pagella Math', 'TeX Gyre Pagella', serif"
TEXT = "'TeX Gyre Pagella', serif"
CAL = "'Latin Modern Math', serif"  # its script letters are the cmsy \mathcal shapes that mathpazo keeps
W = H = 69.0  # half MDPI \textwidth (138 mm), square
FS_LAB, FS_TXT, FS_ANN, FS_TAG = 3.2, 2.8, 2.47, 2.2  # 9 pt, 8 pt, 7 pt, 6.2 pt

INK, GREY, MID, LIGHT = "#222222", "#555555", "#888888", "#bbbbbb"
DOM_FILL, DOM_STROKE = "#f3f3f3", "#d6d6d6"  # domains, as in fig:exactness-rotation
PURPLE = "#8a3ab9"  # the light ray
PURPLE_TINT = "#f1e7f7"
GHOST = 0.3  # opacity of the rotated copies g x, g != e
TH = " "  # thin space


def f2(v):
    return f"{v:.2f}"


# ------------------------------------------------------------------ primitives
def pt(cx, cy, r, a):
    """Point at math angle a (deg, counter-clockwise from +x) on the circle (cx, cy, r); SVG y points down."""
    return cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a))


def head(x, y, tx, ty, color, L=1.5, Wd=1.2):
    """Filled arrow head with tip at (x, y) pointing along the unit vector (tx, ty)."""
    nx, ny = -ty, tx
    bx, by = x - L * tx, y - L * ty
    return (f'<path d="M {f2(x)},{f2(y)} L {f2(bx + Wd / 2 * nx)},{f2(by + Wd / 2 * ny)} '
            f'L {f2(bx - Wd / 2 * nx)},{f2(by - Wd / 2 * ny)} Z" style="fill:{color};stroke:none"/>')


def arc(gid, cx, cy, r, a0, a1, color=GREY, w=0.3, heads=("end",), L=1.3, Wd=1.05):
    """Counter-clockwise arc from a0 to a1 (deg), with arrow heads; the stroke stops under each head."""
    span = (a1 - a0) % 360 or 360
    trim = math.degrees(0.9 * L / r)
    s0 = a0 + (trim if "start" in heads else 0)
    s1 = a0 + span - (trim if "end" in heads else 0)
    (x0, y0), (x1, y1) = pt(cx, cy, r, s0), pt(cx, cy, r, s1)
    large = 1 if (s1 - s0) > 180 else 0
    out = [f'<g id="{gid}">',
           f'<path d="M {f2(x0)},{f2(y0)} A {f2(r)} {f2(r)} 0 {large} 0 {f2(x1)},{f2(y1)}" '
           f'style="fill:none;stroke:{color};stroke-width:{w};stroke-linecap:butt"/>']
    for which in heads:
        a = a0 if which == "start" else a0 + span
        sgn = -1 if which == "start" else 1
        x, y = pt(cx, cy, r, a)
        out.append(head(x, y, -math.sin(math.radians(a)) * sgn, -math.cos(math.radians(a)) * sgn, color, L, Wd))
    out.append("</g>")
    return "".join(out)


def text(x, y, s, size=FS_TXT, anchor="middle", family=TEXT, style="normal", weight="normal", color=INK, gid=None):
    i = f' id="{gid}"' if gid else ""
    return (f'<text{i} x="{f2(x)}" y="{f2(y)}" style="font-family:{family};font-size:{size}px;font-style:{style};'
            f'font-weight:{weight};fill:{color};text-anchor:{anchor}">{s}</text>')


def math_text(x, y, parts, size=FS_TXT, anchor="middle", color=INK, gid=None):
    """parts: list of (string, kind), kind in n (math italic font), rm (text font), cal (\\mathcal), sub, sup.
    Scripts are tspans shifted with dy (portable to Ipe / browsers)."""
    shift = {"n": 0.0, "rm": 0.0, "cal": 0.0, "sub": 0.22 * size, "sup": -0.36 * size}
    cur, spans = 0.0, []
    for s, kind in parts:
        st = []
        if kind == "cal":
            st.append(f"font-family:{CAL}")
        if kind == "rm":
            st.append(f"font-family:{TEXT}")
        if kind in ("sub", "sup"):
            st.append(f"font-size:{f2(0.7 * size)}px")
        dy = f' dy="{f2(shift[kind] - cur)}"' if abs(shift[kind] - cur) > 1e-9 else ""
        sty = f' style="{";".join(st)}"' if st else ""
        spans.append(f"<tspan{dy}{sty}>{s}</tspan>")
        cur = shift[kind]
    i = f' id="{gid}"' if gid else ""
    return (f'<text{i} x="{f2(x)}" y="{f2(y)}" style="font-family:{MATH};font-size:{size}px;fill:{color};'
            f'text-anchor:{anchor}">{"".join(spans)}</text>')


def centred(x, y, parts, size, gid, color=INK, anchor="middle"):
    """math_text whose x-height is centred at y (labels next to a point)."""
    return math_text(x, y + 0.24 * size, parts, size, anchor, color, gid)


ELEM = {0: [("𝑒", "n")], 1: [("𝑟", "n")], 2: [("𝑟", "n"), ("2", "sup")], 3: [("𝑟", "n"), ("3", "sup")]}
NAME = {0: "e", 1: "r", 2: "r2", 3: "r3"}


def header(x, y, num, name, gid):
    """Panel header in the style of the other figures: bold number, italic name."""
    return (text(x, y, num, FS_LAB, "start", weight="bold", gid=f"{gid}-num")
            + text(x + 2.4, y, name, FS_TXT, "start", style="italic", gid=f"{gid}-name"))


# ------------------------------------------------------------------ input: lamp + ray on the canvas
def lamp(gid, x, y, a_svg, sc=1.0, opacity=1.0):
    """Laser lamp centred at (x, y), emitting along local +x, turned by a_svg deg (SVG, clockwise).
    Local extent: x in [-3, 2.2] (aperture at x = 2.2), y in [-1.2, 1.2]."""
    body = ('<rect x="-3" y="-1.2" width="4" height="2.4" rx="0.45" style="fill:#4a4a4a;stroke:none"/>'
            '<path d="M -2.3,-1.2 V 1.2 M -1.7,-1.2 V 1.2" style="fill:none;stroke:#8c8c8c;stroke-width:0.2"/>'
            '<rect x="1" y="-0.75" width="1.05" height="1.5" style="fill:#2b2b2b;stroke:none"/>'
            f'<rect x="1.9" y="-0.45" width="0.3" height="0.9" style="fill:{PURPLE};stroke:none"/>')
    op = f";opacity:{opacity}" if opacity < 1 else ""
    return (f'<g id="{gid}" transform="translate({f2(x)},{f2(y)}) rotate({f2(a_svg)}) scale({f2(sc)})" '
            f'style="fill:none{op}">{body}</g>')


def ray(gid, p0, p1, sc=1.0, opacity=1.0):
    """Solid ray from the aperture p0 (through the origin) to p1: a soft glow under a thin core."""
    d = f"M {f2(p0[0])},{f2(p0[1])} L {f2(p1[0])},{f2(p1[1])}"
    op = f";opacity:{opacity}" if opacity < 1 else ""
    return (f'<g id="{gid}" style="fill:none{op}">'
            f'<path id="{gid}-glow" d="{d}" style="fill:none;stroke:{PURPLE};stroke-width:{f2(1.5 * sc)};'
            f'stroke-opacity:0.22;stroke-linecap:butt"/>'
            f'<path id="{gid}-core" d="{d}" style="fill:none;stroke:{PURPLE};stroke-width:{f2(0.45 * sc)};'
            f'stroke-linecap:butt"/></g>')


def canvas(pre, cx, cy, s, sc=1.0, arc_label=False, th0=135, fs=FS_TXT, arc_sc=1.0):
    """Square canvas of side s centred on the origin (cx, cy). The lamp of g = r^k sits in corner th0 + 90 k deg
    (th0 = 135: upper left for e; th0 = 45: upper right; then counter-clockwise), aims at the origin, and is
    tagged outside its corner. Its ray ends at the aperture of the opposite lamp."""
    x0, y0 = cx - s / 2, cy - s / 2
    out = [f'<g id="{pre}" inkscape:label="input canvas">',
           f'<rect id="{pre}-domain" x="{f2(x0)}" y="{f2(y0)}" width="{f2(s)}" height="{f2(s)}" '
           f'style="fill:{DOM_FILL};stroke:{DOM_STROKE};stroke-width:0.25"/>']
    half_diag = s / math.sqrt(2)
    d = half_diag - 4.2 * sc  # lamp centre: rear end ~1 mm inside the corner
    # the ray starts inside its own aperture and stops inside the opposite one: overlapping (not abutting) shapes
    # avoid anti-aliasing seams
    ext = d - 1.9 * sc
    labels = []
    for k in (1, 2, 3, 0):  # faded copies first, e on top
        th = th0 + 90 * k
        lx, ly = pt(cx, cy, d, th)
        ux, uy = -math.cos(math.radians(th)), math.sin(math.radians(th))  # towards the origin (SVG)
        a_svg = math.degrees(math.atan2(uy, ux))
        p0 = (lx + ux * 2.0 * sc, ly + uy * 2.0 * sc)
        p1 = (cx + ux * ext, cy + uy * ext)
        op = 1.0 if k == 0 else GHOST
        g = f"{pre}-{NAME[k]}"
        out.append(f'<g id="{g}" inkscape:label="{NAME[k]} x">')
        out.append(ray(f"{g}-ray", p0, p1, sc, op))
        out.append(lamp(f"{g}-lamp", lx, ly, a_svg, sc, op))
        out.append("</g>")
        tx, ty = pt(cx, cy, half_diag + 0.82 * fs, th)
        labels.append(centred(tx, ty, ELEM[k], fs, f"{pre}-label-{NAME[k]}"))
    out.append(f'<circle id="{pre}-origin" cx="{f2(cx)}" cy="{f2(cy)}" r="{f2(0.4 * arc_sc)}" '
               f'style="fill:{INK};stroke:none"/>')
    rr = 0.3 * s
    out.append(arc(f"{pre}-rot", cx, cy, rr, th0 + 14, th0 + 90 - 14, w=0.3 * arc_sc, L=1.3 * arc_sc,
                   Wd=1.05 * arc_sc))
    if arc_label:
        lx, ly = pt(cx, cy, rr + 1.0, th0 + 45)
        labels.append(math_text(lx, ly + 0.24 * FS_ANN, [("𝑅", "n"), ("𝜋/2", "sub")], FS_ANN, "end",
                                GREY, f"{pre}-rot-label"))
    out += labels
    out.append("</g>")
    return "".join(out)


# ------------------------------------------------------------------ outputs
def disk(gid, cx, cy, R):
    return (f'<circle id="{gid}" cx="{f2(cx)}" cy="{f2(cy)}" r="{f2(R)}" '
            f'style="fill:{DOM_FILL};stroke:{DOM_STROKE};stroke-width:0.25"/>')


def out_orientation(pre, cx, cy, R):
    """Y = [0, 2 pi): f(r^k x) is the arrow at angle 315 + 90 k deg (the direction of the ray r^k x)."""
    out = [f'<g id="{pre}" inkscape:label="output 1: orientation">', disk(f"{pre}-domain", cx, cy, R)]
    out.append(arc(f"{pre}-rot", cx, cy, 0.5 * R, 315 + 16, 405 - 16, L=1.1, Wd=0.9))
    labels = []
    for k in (1, 2, 3, 0):
        phi = 315 + 90 * k
        tx, ty = math.cos(math.radians(phi)), -math.sin(math.radians(phi))  # unit direction (SVG)
        x1, y1 = pt(cx, cy, R - 0.1, phi)
        xs, ys = pt(cx, cy, R - 1.3, phi)
        op = "" if k == 0 else f";opacity:{GHOST}"
        out.append(f'<g id="{pre}-{NAME[k]}" style="fill:none{op}">'
                   f'<path d="M {f2(cx)},{f2(cy)} L {f2(xs)},{f2(ys)}" '
                   f'style="fill:none;stroke:{PURPLE};stroke-width:0.45;stroke-linecap:butt"/>'
                   f'{head(x1, y1, tx, ty, PURPLE, 1.5, 1.2)}</g>')
        lx, ly = pt(cx, cy, R + 2.0, phi)
        labels.append(centred(lx, ly, ELEM[k], FS_ANN, f"{pre}-label-{NAME[k]}"))
    out.append(f'<circle cx="{f2(cx)}" cy="{f2(cy)}" r="0.4" style="fill:{INK};stroke:none"/>')
    out += labels
    out.append("</g>")
    return "".join(out)


def out_axis(pre, cx, cy, R):
    """Y = [0, pi): f(r^k x) is the undirected axis at angle 135 + 90 k mod 180 deg; e ~ r^2 and r ~ r^3."""
    out = [f'<g id="{pre}" inkscape:label="output 2: axis">', disk(f"{pre}-domain", cx, cy, R)]
    out.append(arc(f"{pre}-rot", cx, cy, 0.5 * R, 135 + 16, 225 - 16, L=1.1, Wd=0.9))
    labels = []
    for k, phi, lab in ((1, 45, [("𝑟,", "n"), (TH + "𝑟", "n"), ("3", "sup")]),
                        (0, 135, [("𝑒,", "n"), (TH + "𝑟", "n"), ("2", "sup")])):
        (xa, ya), (xb, yb) = pt(cx, cy, R - 0.3, phi), pt(cx, cy, R - 0.3, phi + 180)
        op = "" if k == 0 else f";opacity:{GHOST}"
        out.append(f'<g id="{pre}-{NAME[k]}" style="fill:none{op}">'
                   f'<path d="M {f2(xa)},{f2(ya)} L {f2(xb)},{f2(yb)}" '
                   f'style="fill:none;stroke:{PURPLE};stroke-width:0.45;stroke-linecap:round"/></g>')
        lx, ly = pt(cx, cy, R + 2.9, phi)
        labels.append(centred(lx, ly, lab, FS_ANN, f"{pre}-label-{NAME[k]}"))
    out.append(f'<circle cx="{f2(cx)}" cy="{f2(cy)}" r="0.4" style="fill:{INK};stroke:none"/>')
    out += labels
    out.append("</g>")
    return "".join(out)


def tag(gid, cx, cy, s, w, h, stroke, fill, color, opacity=1.0):
    op = f";opacity:{opacity}" if opacity < 1 else ""
    return (f'<g id="{gid}" style="fill:none{op}"><rect x="{f2(cx - w / 2)}" y="{f2(cy - h / 2)}" width="{f2(w)}" '
            f'height="{f2(h)}" rx="0.8" style="fill:{fill};stroke:{stroke};stroke-width:0.35"/>'
            + text(cx, cy + 0.3 * FS_ANN, s, FS_ANN, color=color, gid=f"{gid}-text") + "</g>")


def out_class(pre, cx, cy, R):
    """Y = {on, off}: the four f(r^k x) are the same label; the loop is rho_Y(r) = id."""
    w, h = 6.4, 3.3
    yon, yoff = cy - 0.9, cy + 3.9
    out = [f'<g id="{pre}" inkscape:label="output 3: class">',
           f'<rect id="{pre}-domain" x="{f2(cx - R)}" y="{f2(cy - R)}" width="{f2(2 * R)}" height="{f2(2 * R)}" '
           f'rx="{f2(0.25 * R)}" style="fill:{DOM_FILL};stroke:{DOM_STROKE};stroke-width:0.25"/>',
           tag(f"{pre}-on", cx, yon, "on", w, h, PURPLE, PURPLE_TINT, INK),
           tag(f"{pre}-off", cx, yoff, "off", w, h, LIGHT, "#ffffff", MID)]
    lc = cx + w / 2 + 1.2
    out.append(arc(f"{pre}-rot", lc, yon, 1.0, 215, 145, L=0.9, Wd=0.8))
    out.append(math_text(cx, yon - h / 2 - 1.1,
                         [("𝑒,", "n"), (TH + "𝑟,", "n"), (TH + "𝑟", "n"), ("2", "sup"), (",", "n"), (TH + "𝑟", "n"),
                          ("3", "sup")], FS_ANN, gid=f"{pre}-label"))
    out.append("</g>")
    return "".join(out)


OUT = {1: ("orientation", out_orientation,
           [("𝒴", "cal"), (TH + "=" + TH + "[0," + TH + "2𝜋)", "n")],
           [("𝜌", "n"), ("𝑌", "sub"), ("(𝐺)" + TH + "≅" + TH + "𝐶", "n"), ("4", "sub")]),
       2: ("axis", out_axis,
           [("𝒴", "cal"), (TH + "=" + TH + "[0," + TH + "𝜋)", "n")],
           [("𝜌", "n"), ("𝑌", "sub"), ("(𝐺)" + TH + "≅" + TH + "𝐶", "n"), ("2", "sub")]),
       3: ("class", out_class,
           [("𝒴", "cal"), (TH + "=" + TH + "{", "n"), ("on," + TH + "off", "rm"), ("}", "n")],
           [("𝜌", "n"), ("𝑌", "sub"), ("(𝐺)" + TH + "=" + TH + "{", "n"), ("id", "rm"), ("}", "n")])}

X_SPACE = [("𝒳", "cal"), (TH + "=" + TH + "ℝ", "n"), ("2", "sup")]
RHO_X = [("𝜌", "n"), ("𝑋", "sub"), ("(𝑟)" + TH + "=" + TH + "𝑅", "n"), ("𝜋/2", "sub")]


def output_panel(i, x, y, cw, R, dial_dy, cap_dy, two_lines=True, cap_gap=3.4):
    """Output i in a cell of width cw with top-left (x, y): header, dial centred dial_dy below the top,
    captions from cap_dy below the top."""
    name, fn, ysp, img = OUT[i]
    cx = x + cw / 2
    out = [header(x + 0.6, y + 3.0, str(i), name, f"out{i}-header"),
           fn(f"out{i}", cx, y + dial_dy, R),
           math_text(cx, y + cap_dy, ysp, FS_ANN, gid=f"out{i}-space")]
    if two_lines:
        out.append(math_text(cx, y + cap_dy + cap_gap, img, FS_ANN, color=GREY, gid=f"out{i}-image"))
    return "".join(out)


# ------------------------------------------------------------------ variants
def svg_doc(title, layers):
    body = "".join(f'<g id="layer-{lid}" inkscape:groupmode="layer" inkscape:label="{lab}">{c}</g>'
                   for lid, lab, c in layers)
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
            f'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" width="{W}mm" height="{H}mm" '
            f'viewBox="0 0 {W} {H}" version="1.1">\n<title>{title}</title>\n'
            f'<sodipodi:namedview id="namedview" pagecolor="#ffffff" inkscape:document-units="mm" units="mm"/>\n'
            f'{body}\n</svg>\n')


def input_texts(x, y, anchor="start", gap=3.6):
    """Input header and captions: space X (black) and the form of r on it (grey), as for the outputs."""
    return (text(x, y, "input", FS_TXT, anchor, style="italic", gid="input-name")
            + math_text(x, y + gap + 0.4, X_SPACE, FS_ANN, anchor, gid="input-space")
            + math_text(x, y + 2 * gap + 0.4, RHO_X, FS_ANN, anchor, color=GREY, gid="input-rho"))


def variant_A():
    """Input on top, outputs in a row."""
    s = 30.0
    inp = canvas("input", W / 2, 4.2 + s / 2, s, sc=1.0) + input_texts(0.6, 6.0)
    cw = W / 3
    outs = "".join(output_panel(i, (i - 1) * cw, 38.0, cw, 7.0, 12.5, 24.0, cap_gap=3.5) for i in (1, 2, 3))
    return svg_doc("One rotation, several forms: input above, outputs below",
                   [("input", "Input", inp), ("outputs", "Outputs", outs)])


def variant_B():
    """2 x 2 grid, input top-left."""
    c = W / 2
    s = 18.0  # = the diameter of the output disks
    inp = (text(0.6, 3.0, "input", FS_TXT, "start", style="italic", gid="input-name")
           + canvas("input", c / 2, 16.4, s, sc=0.72)
           + math_text(c / 2, c - 5.0, X_SPACE, FS_ANN, gid="input-space")
           + math_text(c / 2, c - 1.7, RHO_X, FS_ANN, color=GREY, gid="input-rho"))
    kw = dict(R=9.0, dial_dy=16.4, cap_dy=c - 5.0, cap_gap=3.3)
    outs = (output_panel(1, c, 0.0, c, **kw) + output_panel(2, 0.0, c, c, **kw) + output_panel(3, c, c, c, **kw))
    return svg_doc("One rotation, several forms: 2 x 2 grid",
                   [("input", "Input", inp), ("outputs", "Outputs", outs)])


def variant_C():
    """Input on the left, outputs stacked on the right."""
    s = 40.0
    cx, top = 3.0 + s / 2, 13.0
    inp = (text(0.6, top - 5.0, "input", FS_TXT, "start", style="italic", gid="input-name")
           + canvas("input", cx, top + s / 2, s, sc=1.05)
           + math_text(cx, top + s + 4.6, X_SPACE, FS_ANN, gid="input-space")
           + math_text(cx, top + s + 8.2, RHO_X, FS_ANN, color=GREY, gid="input-rho"))
    x0, ch = 48.0, H / 3
    outs = "".join(output_panel(i, x0, (i - 1) * ch, W - x0, 5.4, 11.2, ch - 1.4, two_lines=False)
                   for i in (1, 2, 3))
    return svg_doc("One rotation, several forms: input left, outputs right",
                   [("input", "Input", inp), ("outputs", "Outputs", outs)])


def variant_D():
    """The input canvas alone, e in the upper-right corner; corner tags are the only text."""
    fs = FS_LAB
    s = W - 2 * (0.58 * fs + 1.6)  # room for the corner tags outside the canvas
    inp = canvas("input", W / 2, H / 2, s, sc=1.6, th0=45, fs=fs, arc_sc=1.4)
    return svg_doc("One rotation, several forms: the C4 orbit of the input",
                   [("input", "Input", inp)])


VARIANTS = {"A": variant_A, "B": variant_B, "C": variant_C, "D": variant_D}

# ------------------------------------------------------------------ export + checks
INKSCAPE_ENV = {k: v for k, v in os.environ.items()
                if k not in ("GSETTINGS_SCHEMA_DIR", "GTK_PATH", "GTK_EXE_PREFIX", "GIO_MODULE_DIR",
                             "GDK_PIXBUF_MODULE_FILE", "GDK_PIXBUF_MODULEDIR", "LOCPATH")}
INKSCAPE_ENV["XDG_DATA_DIRS"] = "/usr/local/share:/usr/share"


def inkscape(*args):
    return subprocess.run(["inkscape", *args], env=INKSCAPE_ENV, capture_output=True, text=True, check=True).stdout


def validate(path, svg):
    """Text boxes: inside the page (0.4 mm margin) and pairwise disjoint."""
    import re
    px = 96 / 25.4
    bb = {}
    for ln in inkscape(path, "--query-all").splitlines():
        p = ln.split(",")
        if len(p) == 5:
            bb[p[0]] = tuple(float(v) / px for v in p[1:])
    tids = [t for t in re.findall(r'<text id="([^"]+)"', svg) if t in bb]
    issues = []
    for t in tids:
        x, y, w, h = bb[t]
        if x < 0.4 or y < 0.4 or x + w > W - 0.4 or y + h > H - 0.4:
            issues.append(f"{t} outside the page margin ({x:.1f},{y:.1f},{x + w:.1f},{y + h:.1f})")
    for i, a in enumerate(tids):
        for b in tids[i + 1:]:
            A, B = bb[a], bb[b]
            if A[0] < B[0] + B[2] and B[0] < A[0] + A[2] and A[1] < B[1] + B[3] and B[1] < A[1] + A[3]:
                if not (a.endswith("-text") or b.endswith("-text")):
                    issues.append(f"text overlap: {a} / {b}")
    return issues


def final(name):
    img = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    svg_path = os.path.join(img, "one-rotation.svg")
    with open(svg_path, "w", encoding="utf-8") as fh:
        fh.write(VARIANTS[name]())
    inkscape(svg_path, "--export-type=pdf", "-o", svg_path[:-4] + ".pdf")
    print(svg_path[:-4] + ".pdf")


def main(argv):
    if argv and argv[0] == "--final":
        return final(argv[1] if len(argv) > 1 else "D")
    outdir = argv[0] if argv else "."
    os.makedirs(outdir, exist_ok=True)
    for name, fn in VARIANTS.items():
        svg = fn()
        path = os.path.join(outdir, f"one-rotation_variant_{name}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg)
        issues = validate(path, svg)
        inkscape(path, "--export-type=png", "--export-dpi=400", "--export-background=#ffffff",
                 "-o", path[:-4] + ".png")
        print(f"[{name}] {path} -- {len(issues)} layout issue(s)")
        for it in issues:
            print("   ", it)


if __name__ == "__main__":
    main(sys.argv[1:])
