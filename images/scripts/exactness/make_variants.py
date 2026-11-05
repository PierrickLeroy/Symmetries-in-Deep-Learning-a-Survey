"""Exactness axis on a rotation-symmetric 2D image (sec:incomplete-symmetries) -- 3 design variants.

a exact (constant-hue annulus), b extent-restricted (digit 6 -> 9 under a half-turn),
c approximate (annulus whose hue varies slowly with the polar angle).
Units: 1 user unit = 1 mm. Text stays <text> in TeX Gyre Pagella (matches mathpazo), so it is editable.
Usage: python3 make_variants.py OUTDIR     (writes exactness_variant_{A,B,C}.svg and .png previews)
       python3 make_variants.py --final    (writes variant C as survey/images/exactness-rotation.{svg,pdf})
Re-running --final overwrites exactness-rotation.svg / .pdf, including Inkscape edits made to them.
"""
import math
import os
import subprocess
import sys

MATH = "'TeX Gyre Pagella Math', 'TeX Gyre Pagella', serif"
TEXT = "'TeX Gyre Pagella', serif"
W = 138.0  # MDPI \textwidth (mm)
INK, GREY, LIGHT = "#222222", "#555555", "#bbbbbb"
GREEN = "#117733"  # Paul Tol: "the symmetry holds"
BASE = "#3b9fc9"   # Paul Tol blue, the image ink
FS_LAB, FS_TXT, FS_TICK = 3.2, 2.8, 2.4  # 9 pt, 8 pt, ~7 pt


def f1(v):
    return f"{v:.1f}"


def f2(v):
    return f"{v:.2f}"


# ------------------------------------------------------------------ colour (OKLCH, for a perceptually even hue sweep)
def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _gam(c):
    c = min(max(c, 0.0), 1.0)
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def hex_to_oklch(h):
    r, g, b = (_lin(int(h[i:i + 2], 16) / 255) for i in (1, 3, 5))
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    A = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    B = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return L, math.hypot(A, B), math.degrees(math.atan2(B, A)) % 360


def oklch_to_hex(L, C, h):
    a, b = C * math.cos(math.radians(h)), C * math.sin(math.radians(h))
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    rgb = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
           -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
           -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)
    return "#" + "".join(f"{round(_gam(c) * 255):02x}" for c in rgb)


L0, C0, H0 = hex_to_oklch(BASE)
# Approximate annulus: colour(phi) = (L0, C0, H0) + (dL, dC, dH) cos(phi) in OKLCH, i.e. lightness ("value"),
# chroma ("saturation") and hue all vary together around the colour of the exact annulus.
APPROX = dict(dL=-0.12, dC=0.04, dH=36.0)  # pale teal (phi = pi) <-> deep indigo (phi = 0); stays in sRGB


def approx_colour(phi_deg, dL=None, dC=None, dH=None):
    c = math.cos(math.radians(phi_deg))
    dL = APPROX["dL"] if dL is None else dL
    dC = APPROX["dC"] if dC is None else dC
    dH = APPROX["dH"] if dH is None else dH
    return oklch_to_hex(L0 + dL * c, C0 + dC * c, H0 + dH * c)


# ------------------------------------------------------------------ primitives
def pt(cx, cy, r, a):
    """Point at math angle a (deg, counter-clockwise from +x) on the circle (cx, cy, r); SVG y points down."""
    return cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a))


def annulus(gid, cx, cy, R, r, fill):
    d = (f"M {f2(cx + R)},{f2(cy)} A {R} {R} 0 1 0 {f2(cx - R)},{f2(cy)} A {R} {R} 0 1 0 {f2(cx + R)},{f2(cy)} Z "
         f"M {f2(cx + r)},{f2(cy)} A {r} {r} 0 1 0 {f2(cx - r)},{f2(cy)} A {r} {r} 0 1 0 {f2(cx + r)},{f2(cy)} Z")
    return f'<path id="{gid}" d="{d}" style="fill:{fill};fill-rule:evenodd;stroke:none"/>'


def annulus_varying(gid, cx, cy, R, r, n=120, overlap=0.6, colour=approx_colour):
    """Annulus split into n wedges, wedge k coloured at colour(phi_k); wedges overlap to hide seams."""
    out = [f'<g id="{gid}" inkscape:label="annulus, varying colour ({n} wedges)">']
    for k in range(n):
        a0, a1 = 360 * k / n, 360 * (k + 1) / n + overlap
        col = colour((a0 + a1 - overlap) / 2)
        (x0, y0), (x1, y1) = pt(cx, cy, R, a0), pt(cx, cy, R, a1)
        (u1, v1), (u0, v0) = pt(cx, cy, r, a1), pt(cx, cy, r, a0)
        d = (f"M {f2(x0)},{f2(y0)} A {R} {R} 0 0 0 {f2(x1)},{f2(y1)} L {f2(u1)},{f2(v1)} "
             f"A {r} {r} 0 0 1 {f2(u0)},{f2(v0)} Z")
        out.append(f'<path id="{gid}-w{k:03d}" d="{d}" style="fill:{col};stroke:none"/>')
    out.append("</g>")
    return "".join(out)


def six(gid, cx, cy, h, rot=0.0, color=BASE, opacity=1.0, width=None):
    """Hand-written digit 6 of height h centred at (cx, cy), rotated by rot deg counter-clockwise.
    The glyph is centred, so rot = 180 gives a 9 at the same place."""
    s = h
    pts = dict(top=(0.20, -0.48), c1=(-0.08, -0.47), c2=(-0.27, -0.16), left=(-0.27, 0.21), right=(0.27, 0.21))
    P = {k: (cx + s * x, cy + s * y) for k, (x, y) in pts.items()}
    rl = 0.27 * s
    d = (f"M {f2(P['top'][0])},{f2(P['top'][1])} C {f2(P['c1'][0])},{f2(P['c1'][1])} "
         f"{f2(P['c2'][0])},{f2(P['c2'][1])} {f2(P['left'][0])},{f2(P['left'][1])} "
         f"A {f2(rl)} {f2(rl)} 0 0 0 {f2(P['right'][0])},{f2(P['right'][1])} "
         f"A {f2(rl)} {f2(rl)} 0 0 0 {f2(P['left'][0])},{f2(P['left'][1])}")
    w = width if width is not None else 0.13 * h
    tf = f' transform="rotate({f1(-rot)},{f2(cx)},{f2(cy)})"' if rot else ""
    return (f'<path id="{gid}" d="{d}"{tf} style="fill:none;stroke:{color};stroke-width:{f2(w)};'
            f'stroke-linecap:round;stroke-linejoin:round;opacity:{opacity}"/>')


def head(x, y, tx, ty, color, L=1.7, Wd=1.4):
    """Filled arrow head with tip at (x, y) pointing along the unit vector (tx, ty)."""
    nx, ny = -ty, tx
    bx, by = x - L * tx, y - L * ty
    return (f'<path d="M {f2(x)},{f2(y)} L {f2(bx + Wd / 2 * nx)},{f2(by + Wd / 2 * ny)} '
            f'L {f2(bx - Wd / 2 * nx)},{f2(by - Wd / 2 * ny)} Z" style="fill:{color};stroke:none"/>')


def arc(gid, cx, cy, r, a0, a1, color=GREY, w=0.35, heads=(), dash=None, opacity=1.0):
    """Counter-clockwise arc from a0 to a1 (deg); heads in {'start', 'end'} adds arrow heads.
    The stroke is shortened under each head so the tip sits exactly at a0 / a1."""
    span = (a1 - a0) % 360 or 360
    trim = math.degrees(1.2 / r)  # ~1.2 mm of arc hidden under a head
    s0 = a0 + (trim if "start" in heads else 0)
    s1 = a0 + span - (trim if "end" in heads else 0)
    (x0, y0), (x1, y1) = pt(cx, cy, r, s0), pt(cx, cy, r, s1)
    large = 1 if (s1 - s0) > 180 else 0
    style = f"fill:none;stroke:{color};stroke-width:{w};stroke-linecap:butt;opacity:{opacity}"
    if dash:
        style += f";stroke-dasharray:{dash}"
    out = [f'<g id="{gid}">',
           f'<path d="M {f2(x0)},{f2(y0)} A {r} {r} 0 {large} 0 {f2(x1)},{f2(y1)}" style="{style}"/>']
    for which in heads:
        a = a0 if which == "start" else a0 + span
        sgn = -1 if which == "start" else 1
        x, y = pt(cx, cy, r, a)
        tx, ty = -math.sin(math.radians(a)) * sgn, -math.cos(math.radians(a)) * sgn
        out.append(head(x, y, tx, ty, color))
    out.append("</g>")
    return "".join(out)


def wavy_arc(gid, cx, cy, r, a0, a1, color=GREEN, w=0.4, amp=0.3, wl=3.4):
    """Counter-clockwise arc a0 -> a1 whose radius oscillates (a "≈" drawn along the rotation), with an end head."""
    span = (a1 - a0) % 360 or 360
    trim = math.degrees(1.2 / r)
    n = int(span * 2)
    pts = []
    for i in range(n + 1):
        a = a0 + (span - trim) * i / n
        s_len = math.radians(a - a0) * r
        pts.append(pt(cx, cy, r + amp * math.sin(2 * math.pi * s_len / wl), a))
    d = "M " + " L ".join(f"{f2(x)},{f2(y)}" for x, y in pts)
    a = a0 + span
    x, y = pt(cx, cy, r, a)
    return (f'<g id="{gid}"><path d="{d}" style="fill:none;stroke:{color};stroke-width:{w};stroke-linejoin:round"/>'
            f'{head(x, y, -math.sin(math.radians(a)), -math.cos(math.radians(a)), color)}</g>')


def text(x, y, s, size=FS_TXT, anchor="middle", family=TEXT, style="normal", weight="normal", color=INK, gid=None):
    i = f' id="{gid}"' if gid else ""
    return (f'<text{i} x="{f2(x)}" y="{f2(y)}" style="font-family:{family};font-size:{size}px;font-style:{style};'
            f'font-weight:{weight};fill:{color};text-anchor:{anchor}">{s}</text>')


def math_text(x, y, parts, size=FS_TXT, anchor="middle", color=INK, gid=None):
    """parts: list of (string, 'n' | 'sub'). Subscripts are tspans shifted with dy (portable to Ipe / browsers)."""
    sub, shift = 0.7 * size, 0.22 * size
    spans, down = [], False
    for s, kind in parts:
        if kind == "sub" and not down:
            spans.append(f'<tspan dy="{f2(shift)}" style="font-size:{f2(sub)}px">{s}</tspan>')
            down = True
        elif kind == "n" and down:
            spans.append(f'<tspan dy="{f2(-shift)}">{s}</tspan>')
            down = False
        else:
            spans.append(f"<tspan>{s}</tspan>")
    i = f' id="{gid}"' if gid else ""
    return (f'<text{i} x="{f2(x)}" y="{f2(y)}" style="font-family:{MATH};font-size:{size}px;fill:{color};'
            f'text-anchor:{anchor}">{"".join(spans)}</text>')


TH = " "  # thin space
CRIT = {  # exactness criteria of the excerpt, in terms of the epsilon-stabilizer
    "a": [("Stab", "n"), ("0", "sub"), ("(𝑓)" + TH + "=" + TH + "𝐺", "n")],
    "b": [("Stab", "n"), ("𝜖", "sub"), ("(𝑓)" + TH + "=" + TH + "𝑆" + TH + "⊊" + TH + "𝐺", "n")],
    "c": [("Stab", "n"), ("0", "sub"), ("(𝑓)" + TH + "≠" + TH + "𝐺" + TH + "=" + TH + "Stab", "n"), ("𝜖", "sub"),
          ("(𝑓)", "n")],
}
NAME = {"a": "exact", "b": "extent-restricted", "c": "approximate"}


def image(k, cx, cy, size, ghost=False):
    """The three 2D images; size = outer diameter of the annuli = height of the 6."""
    R, r = size / 2, size / 2 * 0.62
    if k == "a":
        return annulus("img-a", cx, cy, R, r, BASE)
    if k == "c":
        return annulus_varying("img-c", cx, cy, R, r)
    g = six("img-b", cx, cy, size)
    if ghost:  # faint copy rotated by pi/2: the boundary of S, where 6 and 9 can no longer be told apart
        g = six("img-b-ghost", cx, cy, size, rot=90, color=GREY, opacity=0.22) + g
    return g


def svg_doc(w, h, title, layers):
    body = "".join(f'<g id="layer-{lid}" inkscape:groupmode="layer" inkscape:label="{lab}">{c}</g>'
                   for lid, lab, c in layers)
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
            f'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" width="{f1(w)}mm" height="{f1(h)}mm" '
            f'viewBox="0 0 {f1(w)} {f1(h)}" version="1.1">\n<title>{title}</title>\n'
            f'<sodipodi:namedview id="namedview" pagecolor="#ffffff" inkscape:document-units="mm" units="mm"/>\n'
            f'{body}\n</svg>\n')


COLS = {"a": W / 6, "b": W / 2, "c": 5 * W / 6}


# ------------------------------------------------------------------ variant A: images only
def variant_A():
    H, cy, size = 38.0, 18.5, 22.0
    imgs, labs = [], []
    for k, cx in COLS.items():
        imgs.append(f'<g id="panel-{k}-image" inkscape:label="image {k}">{image(k, cx, cy, size)}</g>')
        labs.append(text(cx - 20, 5.0, k, FS_LAB, "start", weight="bold", gid=f"label-{k}"))
        labs.append(text(cx, 35.0, NAME[k], FS_TXT, style="italic", gid=f"name-{k}"))
    return svg_doc(W, H, "Exactness of a rotation symmetry: images only",
                   [("images", "Images", "".join(imgs)), ("labels", "Labels", "".join(labs))])


# ------------------------------------------------------------------ variant B: rotation symbols + criteria
def dial(k, cx, cy, Rd=12.0, Ra=14.5):
    """Image domain (light grey disk) and the rotation symbol around it, as (domain, rotation, ghosts) SVG strings.
    a: full arc (exact on G); b: arc on S = [-pi/2, pi/2] only, dashed on G minus S, with faint 6s turned by
    -pi/2 / +pi/2 at the two ends of S (6 and 9 can no longer be told apart); c: wavy full arc ("≈" on G)."""
    S0 = 90.0
    dom = (f'<circle id="domain-{k}" cx="{f2(cx)}" cy="{f2(cy)}" r="{Rd}" '
           f'style="fill:#f3f3f3;stroke:#d6d6d6;stroke-width:0.25"/>')
    ghosts = ""
    if k == "a":
        rot = arc("rot-a", cx, cy, Ra, 110, 70, GREEN, 0.4, heads=("end",))
    elif k == "c":
        rot = wavy_arc("rot-c", cx, cy, Ra, 110, 70)
    else:
        rot = (arc("rot-b-out", cx, cy, Ra, 90 + S0, 90 - S0, LIGHT, 0.3, dash="0.8,0.8")
               + arc("rot-b-S", cx, cy, Ra, 90 - S0, 90 + S0, GREEN, 0.4, heads=("start", "end"))
               + math_text(cx, cy - Ra - 1.4, [("𝑆", "n")], FS_TXT, color=GREEN, gid="label-S"))
        gr = Ra + 5.0
        ghosts = (f'<g id="ghosts-b" inkscape:label="ghosts: 6 turned by ±pi/2">'
                  f'{six("ghost-minus", cx + gr, cy, 6.0, rot=-90, color=GREY, opacity=0.4)}'
                  f'{six("ghost-plus", cx - gr, cy, 6.0, rot=90, color=GREY, opacity=0.4)}</g>')
    return dom, rot, ghosts


def variant_B():
    H, cy, size = 50.0, 22.0, 19.0
    dom, imgs, rots, labs = [], [], [], []
    for k, cx in COLS.items():
        d, r, g = dial(k, cx, cy)
        dom.append(d)
        rots.append(r)
        imgs.append(f'<g id="panel-{k}-image" inkscape:label="image {k}">{image(k, cx, cy, size)}</g>{g}')
        labs.append(text(cx - 20, 5.0, k, FS_LAB, "start", weight="bold", gid=f"label-{k}"))
        labs.append(text(cx, 42.0, NAME[k], FS_TXT, style="italic", gid=f"name-{k}"))
        labs.append(math_text(cx, 47.5, CRIT[k], FS_TXT, gid=f"crit-{k}"))
    return svg_doc(W, H, "Exactness of a rotation symmetry: rotation symbols",
                   [("domain", "Image domains", "".join(dom)), ("images", "Images", "".join(imgs)),
                    ("rotations", "Rotations", "".join(rots)), ("labels", "Labels", "".join(labs))])


# ------------------------------------------------------------------ variant C: images + equivariance-error profile
def ee_profile(k, th):
    """Schematic theta -> ee(f, theta), in units of the plot height; EPS is the tolerance level."""
    if k == "a":
        return 0.0
    if k == "c":  # colour(phi) = c0 + v cos(phi)  =>  sup_phi |colour(phi - th) - colour(phi)| = 2 |v| |sin(th / 2)|
        return 0.8 * EPS * abs(math.sin(th / 2))
    z = (abs(th) - math.pi / 2) / 0.28  # crosses EPS exactly at |th| = pi/2
    return 0.92 / (1 + math.exp(-(z + math.log(EPS / (0.92 - EPS)))))


EPS = 0.3


def variant_C():
    H, cy, size = 80.0, 25.5, 19.0
    pw, ph, py0 = 34.0, 18.0, 65.0  # plot width, height, y of the theta axis
    dom, imgs, rots, plots, labs = [], [], [], [], []
    for k, cx in COLS.items():
        d, r, g = dial(k, cx, cy)
        dom.append(d)
        rots.append(r)
        imgs.append(f'<g id="panel-{k}-image" inkscape:label="image {k}">{image(k, cx, cy, size)}</g>{g}')
        x0, x1 = cx - pw / 2, cx + pw / 2
        X = lambda th: x0 + (th + math.pi) / (2 * math.pi) * pw  # noqa: E731
        Y = lambda v: py0 - v * ph  # noqa: E731
        p = [f'<g id="plot-{k}" inkscape:label="ee profile {k}">']
        # Stab_eps(f): sublevel set {theta : ee <= eps}, drawn as a rug under the theta axis
        n = 400
        ths = [-math.pi + 2 * math.pi * i / n for i in range(n + 1)]
        inside = [ee_profile(k, t) <= EPS + 1e-9 for t in ths]
        segs, start = [], None
        for t, ok in zip(ths, inside):
            if ok and start is None:
                start = t
            if not ok and start is not None:
                segs.append((start, t))
                start = None
        if start is not None:
            segs.append((start, math.pi))
        for i, (a, b) in enumerate(segs):
            p.append(f'<rect id="stab-{k}-{i}" x="{f2(X(a))}" y="{f2(py0 + 0.9)}" width="{f2(X(b) - X(a))}" '
                     f'height="1.2" style="fill:{GREEN};fill-opacity:0.55;stroke:none"/>')
        # axes, eps level, ticks
        p.append(f'<path d="M {f2(x0)},{f2(py0)} H {f2(x1 + 1.5)} M {f2(x0)},{f2(py0)} V {f2(py0 - ph - 1.5)}" '
                 f'style="fill:none;stroke:{INK};stroke-width:0.3"/>')
        p.append(f'<path d="M {f2(x0)},{f2(Y(EPS))} H {f2(x1)}" '
                 f'style="fill:none;stroke:{GREY};stroke-width:0.3;stroke-dasharray:1,0.8"/>')
        p.append(math_text(x0 - 1.0, Y(EPS) + 0.8, [("𝜖", "n")], FS_TICK, "end"))
        p.append(math_text(x0 - 1.0, py0 + 0.8, [("0", "n")], FS_TICK, "end"))
        for th, lab in ((-math.pi, "−𝜋"), (0.0, ""), (math.pi, "𝜋")):
            p.append(f'<path d="M {f2(X(th))},{f2(py0)} V {f2(py0 + 0.8)}" style="stroke:{INK};stroke-width:0.3"/>')
            if lab:
                p.append(math_text(X(th), py0 + 4.6, [(lab, "n")], FS_TICK))
        # the rug is the set Stab_eps(f), named under its centre
        p.append(math_text(X(0.0), py0 + 4.9, [("𝑆" if k == "b" else "𝐺", "n")], FS_TICK, color=GREEN,
                           gid=f"label-stab-{k}"))
        p.append(math_text(x1 + 2.2, py0 + 0.8, [("𝜃", "n")], FS_TICK, "start"))
        p.append(math_text(x0 + 1.0, py0 - ph - 0.6, [("ee(𝑓," + TH + "𝜃)", "n")], FS_TICK, "start"))
        # curve
        pts = " ".join(f"{f2(X(t))},{f2(Y(ee_profile(k, t)))}" for t in ths[::4])
        p.append(f'<polyline points="{pts}" style="fill:none;stroke:{BASE};stroke-width:0.55;stroke-linejoin:round"/>')
        p.append("</g>")
        plots.append("".join(p))
        labs.append(text(cx - 20, 5.0, k, FS_LAB, "start", weight="bold", gid=f"label-{k}"))
        labs.append(text(cx - 16.5, 5.0, NAME[k], FS_TXT, "start", style="italic", gid=f"name-{k}"))
        labs.append(math_text(cx, 77.0, CRIT[k], FS_TXT, gid=f"crit-{k}"))
    return svg_doc(W, H, "Exactness of a rotation symmetry: error profiles",
                   [("domain", "Image domains", "".join(dom)), ("images", "Images", "".join(imgs)),
                    ("rotations", "Rotations", "".join(rots)), ("plots", "Error profiles", "".join(plots)),
                    ("labels", "Labels", "".join(labs))])


# ------------------------------------------------------------------ export
INKSCAPE_ENV = {k: v for k, v in os.environ.items()
                if k not in ("GSETTINGS_SCHEMA_DIR", "GTK_PATH", "GTK_EXE_PREFIX", "GIO_MODULE_DIR",
                             "GDK_PIXBUF_MODULE_FILE", "GDK_PIXBUF_MODULEDIR", "LOCPATH")}
INKSCAPE_ENV["XDG_DATA_DIRS"] = "/usr/local/share:/usr/share"


def final():
    """Write the chosen variant (C) as survey/images/exactness-rotation.{svg,pdf}, used by main.tex."""
    img = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    svg = os.path.join(img, "exactness-rotation.svg")
    with open(svg, "w", encoding="utf-8") as fh:
        fh.write(variant_C())
    subprocess.run(["inkscape", svg, "--export-type=pdf", "-o", svg[:-4] + ".pdf"], env=INKSCAPE_ENV,
                   capture_output=True, text=True, check=True)
    print(svg[:-4] + ".pdf")


def main(outdir):
    if outdir == "--final":
        return final()
    os.makedirs(outdir, exist_ok=True)
    for name, fn in (("A", variant_A), ("B", variant_B), ("C", variant_C)):
        svg = os.path.join(outdir, f"exactness_variant_{name}.svg")
        with open(svg, "w", encoding="utf-8") as fh:
            fh.write(fn())
        subprocess.run(["inkscape", svg, "--export-type=png", "--export-dpi=300", "--export-background=#ffffff",
                        "-o", svg[:-4] + ".png"], env=INKSCAPE_ENV, capture_output=True, text=True, check=True)
        print(svg)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
