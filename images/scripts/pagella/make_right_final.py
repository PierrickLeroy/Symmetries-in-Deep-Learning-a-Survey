"""Right panel (b) of fig:param-space-symmetries: spaces, maps, and the set each symmetry class reaches.

Layout "commutative square" (variant B, chosen 2026-11-02): modified spaces (Θ', ℱ|X') on top,
Θ -φ-> ℱ in the middle, ℒ_R and ℒ_F below each, combined by AGG. Alternatives A and C: make_right_variants.py.
Reuses the helpers of make_left_variants.py (fonts, math text, validator).
Usage: python3 make_right_final.py OUT.svg   -- regenerating overwrites Inkscape edits made to OUT.svg.

Visual code
- Each class keeps its left-panel colour. A curve of colour k in a parameter space is (part of) the set
  reachable from theta by class k; coincident sets are drawn as parallel lines of one ribbon.
- A dot of colour k is the image point whose preimage is the set of colour k
  (f_theta for (2), L_F(f_theta) for (3), L(theta) for (4), i(f_theta) for (5)).
"""
import math
import sys
from xml.sax.saxutils import escape

import make_left_variants as mlv
from make_left_variants import BOLD, COL, GREY, HAIR, INK, PT, THIN, Doc, f1, inkscape, validate, width

mlv.ITALIC_GREEK["φ"] = "\U0001D711"  # \varphi

PAGE_W, PAGE_H = 92.0, 127.4
SPACE_FS, MAP_FS, POINT_FS, LEG_FS = 8.0 * PT, 7.0 * PT, 6.5 * PT, 6.0 * PT
STRIPE_W, STRIPE_SP = 0.5, 0.5  # ribbon stripe width / centre spacing (mm)
ARROW_W = 0.35
SPACE_STYLE = f"fill:{GREY};fill-opacity:0.06;stroke:{GREY};stroke-width:0.3"  # variant A
FRAME_STYLE = f"fill:{GREY};fill-opacity:0.07;stroke:{GREY};stroke-width:0.35"  # left-panel frame recipe, in grey
NAMES = {1: "(1) orbit", 2: "(2) functional", 3: "(3) loss (factoring)", 4: "(4) loss", 5: "(5) data-dependent"}


# ------------------------------------------------------------------ smooth curves
def _segments(pts, closed):
    """Catmull-Rom through pts, as cubic Bezier segments (p1, c1, c2, p2)."""
    n, segs = len(pts), []
    for i in range(n if closed else n - 1):
        p1, p2 = pts[i], pts[(i + 1) % n]
        if closed:
            p0, p3 = pts[(i - 1) % n], pts[(i + 2) % n]
        else:
            p0 = pts[i - 1] if i > 0 else (2 * p1[0] - p2[0], 2 * p1[1] - p2[1])
            p3 = pts[i + 2] if i + 2 < n else (2 * p2[0] - p1[0], 2 * p2[1] - p1[1])
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        segs.append((p1, c1, c2, p2))
    return segs


def path_d(pts, closed=False):
    if len(pts) == 2 and not closed:
        return f"M {f1(pts[0][0])},{f1(pts[0][1])} L {f1(pts[1][0])},{f1(pts[1][1])}"
    d = [f"M {f1(pts[0][0])},{f1(pts[0][1])}"]
    for _, c1, c2, p2 in _segments(pts, closed):
        d.append(f"C {f1(c1[0])},{f1(c1[1])} {f1(c2[0])},{f1(c2[1])} {f1(p2[0])},{f1(p2[1])}")
    return " ".join(d) + (" Z" if closed else "")


def sample(pts, closed=False, k=20):
    out = []
    for p1, c1, c2, p2 in _segments(pts, closed):
        for j in range(k):
            t = j / k
            a, b, c, e = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
            out.append((a * p1[0] + b * c1[0] + c * c2[0] + e * p2[0], a * p1[1] + b * c1[1] + c * c2[1] + e * p2[1]))
    if not closed:
        out.append(pts[-1])
    return out


def offset(dense, d, closed):
    n, out = len(dense), []
    for i, (x, y) in enumerate(dense):
        a = dense[(i - 1) % n] if closed or i > 0 else dense[i]
        b = dense[(i + 1) % n] if closed or i < n - 1 else dense[i]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty) or 1.0
        out.append((x - d * ty / L, y + d * tx / L))
    return out


def resample(pts, step, closed):
    """Keep points roughly every `step` mm of arc length (fewer nodes for Inkscape)."""
    keep, acc = [pts[0]], 0.0
    for p, q in zip(pts, pts[1:]):
        acc += math.hypot(q[0] - p[0], q[1] - p[1])
        if acc >= step:
            keep.append(q)
            acc = 0.0
    if closed:
        if math.hypot(keep[-1][0] - keep[0][0], keep[-1][1] - keep[0][1]) < 0.5 * step:
            keep.pop()
    elif keep[-1] != pts[-1]:
        if math.hypot(keep[-1][0] - pts[-1][0], keep[-1][1] - pts[-1][1]) < 0.5 * step:
            keep.pop()
        keep.append(pts[-1])
    return keep


def guard(doc, dense, closed=False):
    pts = dense[::2] + ([dense[0]] if closed else [dense[-1]])
    doc.segments += [(*p, *q) for p, q in zip(pts, pts[1:])]


# ------------------------------------------------------------------ drawing primitives
def ribbon(doc, ctrl, classes, gid, label, closed=False, w=STRIPE_W, sp=STRIPE_SP):
    """Parallel stripes, one per class, following the curve through ctrl.
    classes[0] lies on the right of the direction of travel."""
    dense = sample(ctrl, closed)
    n = len(classes)
    out = [f'<g id="{gid}" inkscape:label="{escape(label)}">']
    cap = "butt" if n > 1 else "round"
    for i, k in enumerate(classes):
        d = -(i - (n - 1) / 2) * sp
        full = offset(dense, d, closed) if n > 1 else dense
        guard(doc, full, closed)
        pts = resample(full, 3.0, closed)
        out.append(f'<path id="{gid}-c{k}" inkscape:label="{escape(NAMES[k])}" d="{path_d(pts, closed)}" '
                   f'style="fill:none;stroke:{COL[k]};stroke-width:{w};stroke-linecap:{cap};'
                   f'stroke-linejoin:round"/>')
    out.append("</g>")
    return "\n".join(out), dense


def stripe_point(ctrl, classes, k, y_target, closed=False, sp=STRIPE_SP):
    """Point of the stripe of class k (inside a ribbon) closest to height y_target."""
    dense = sample(ctrl, closed)
    n, i = len(classes), classes.index(k)
    pts = offset(dense, -(i - (n - 1) / 2) * sp, closed)
    return min(pts, key=lambda p: abs(p[1] - y_target))


def dot(pid, x, y, color, r=0.7):
    return (f'<circle id="{pid}" cx="{f1(x)}" cy="{f1(y)}" r="{r:.2f}" '
            f'style="fill:{color};stroke:#ffffff;stroke-width:0.25"/>')


def blob(doc, bid, cx, cy, rx, ry, factors, label, style=SPACE_STYLE):
    pts = [(cx + rx * f * math.cos(2 * math.pi * i / len(factors)), cy + ry * f * math.sin(2 * math.pi * i / len(factors)))
           for i, f in enumerate(factors)]
    guard(doc, sample(pts, True), True)
    return f'<path id="{bid}" inkscape:label="{escape(label)}" d="{path_d(pts, True)}" style="{style}"/>'


def arrow(doc, aid, pts, label):
    mid = doc.marker(GREY)
    if len(pts) == 2:
        d = f"M {f1(pts[0][0])},{f1(pts[0][1])} L {f1(pts[1][0])},{f1(pts[1][1])}"
        dense = [pts[0], pts[1]]
    else:  # quadratic Bezier
        (x0, y0), (x1, y1), (x2, y2) = pts
        d = f"M {f1(x0)},{f1(y0)} Q {f1(x1)},{f1(y1)} {f1(x2)},{f1(y2)}"
        dense = [((1 - t) ** 2 * x0 + 2 * t * (1 - t) * x1 + t * t * x2,
                  (1 - t) ** 2 * y0 + 2 * t * (1 - t) * y1 + t * t * y2) for t in (i / 12 for i in range(13))]
    doc.segments += [(*p, *q) for p, q in zip(dense, dense[1:])]
    doc.__dict__.setdefault("arrows", []).append((aid, sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(dense, dense[1:]))))
    return (f'<path id="{aid}" inkscape:label="{escape(label)}" d="{d}" style="fill:none;stroke:{GREY};'
            f'stroke-width:{ARROW_W};stroke-linecap:round;marker-end:url(#{mid})"/>')


def real_line(doc, rid, x0, x1, y, pt_label, fill):
    """A copy of R: horizontal line, 'R' above the right end, coloured dot, point label below."""
    xd = (x0 + x1) / 2
    doc.segments.append((x0, y, x1, y))
    return "\n".join([
        f'<g id="{rid}" inkscape:label="R ({escape(pt_label)})">',
        f'<path d="M {f1(x0)},{f1(y)} L {f1(x1)},{f1(y)}" style="fill:none;stroke:{GREY};stroke-width:0.35;stroke-linecap:round"/>',
        doc.text(x1, y - 1.3, "ℝ", SPACE_FS, INK, "end", idbase=f"{rid}-name"),
        dot(f"{rid}-dot", xd, y, fill),
        doc.text(xd, y + 1.2 + 0.75 * POINT_FS, pt_label, POINT_FS, INK, "middle", sp=HAIR, idbase=f"{rid}-pt"),
        "</g>"]), xd


def badge(doc, k, x, y, s=2.8):
    r = doc.rect(f"leg{k}-tag", x, y - s / 2, s, s, f"fill:{COL[k]};stroke:none", rx=0.35)
    t = doc.text(x + s / 2, y, str(k), 6.0 * PT, "#ffffff", "middle", vcenter=True, family=BOLD, weight="bold",
                 idbase=f"leg{k}-number", container=f"leg{k}-tag")
    return r + t


# ------------------------------------------------------------------ figure
TILDE = "¤"  # placeholder for a tilde accent on the preceding glyph (combining U+0303 collides with θ)


def tilde_fix(markup, fs):
    """Replace the placeholder by a spacing tilde shifted over the previous θ (metrics of Pagella Math)."""
    return markup.replace(TILDE, f'<tspan dx="{-0.339 * fs:.2f}" dy="{-0.211 * fs:.2f}">˜</tspan>')


LEGEND_SETS = [(1, "Gθ,  Gθ" + TILDE), (2, "φ^{−1}(f_θ)"), (3, "φ^{−1}(ℒ_F^{−1}(ℒ_F(f_θ)))"),
               (4, "ℒ^{−1}(ℒ(θ))"), (5, "φ^{−1}(i^{−1}(i(f_θ)))")]


def text(doc, x, y, s, fs, fill=INK, anchor="start", vcenter=False, idbase="t", container=None):
    return tilde_fix(doc.text(x, y, s, fs, fill, anchor, sp=HAIR, vcenter=vcenter, idbase=idbase,
                              container=container), fs)


def mapl(doc, lid, x, y, s, anchor):
    return doc.text(x, y, s, MAP_FS, INK, anchor, sp=HAIR, vcenter=True, idbase=lid)


def ellipse(cx, cy, rx, ry, n=8):
    return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]


class Frame:
    """Rectangular parameter space; band(u, v) maps [0,1]^2 to the drawing area below the title."""

    def __init__(self, x, y, w, h, top=7.5, bottom=3.5, side=1.5):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.x0, self.x1, self.y0, self.y1 = x + side, x + w - side, y + top, y + h - bottom

    def band(self, xa, v):  # absolute x, relative v
        return (xa, self.y0 + v * (self.y1 - self.y0))


def theta_sets(doc, F, ax, scale, extras, wine_ends, st, gid="theta"):
    """Orbit lens (two mirrored Gθ ribbons around Gθ̃), extra components, ℒ level set through θ.
    ax: x of Gθ̃; scale: horizontal scale of the lens; extras: dict of ctrl lists; st: stripe style."""
    offs = [-7.0, -9.0, -9.5, -8.7, -6.5]
    left = [F.band(ax + scale * o, v) for o, v in zip(offs, (0, .25, .5, .75, 1))]
    right = [(2 * ax - x, y) for x, y in left]
    lcls, rcls = [5, 3, 2, 1], [1, 2, 3, 5]
    g = [f'<g id="{gid}-sets" inkscape:label="sets in Θ">']
    g.append(ribbon(doc, left, lcls, f"{gid}-orbit-a", "Gθ, component through θ  (1)(2)(3)(5)", **st)[0])
    g.append(ribbon(doc, right, rcls, f"{gid}-orbit-b", "Gθ, second component  (1)(2)(3)(5)", **st)[0])
    g.append(ribbon(doc, [F.band(ax, 0), F.band(ax, 1)], [1], f"{gid}-tilde-orbit", "Gθ̃  (1)", **st)[0])
    g.append(ribbon(doc, extras["loop"], [2, 3, 5], f"{gid}-fibre-extra", "extra fibre component  (2)(3)(5)",
                    closed=True, **st)[0])
    g.append(ribbon(doc, extras["green"], [3], f"{gid}-loss-f-extra", "extra level-set component  (3)", **st)[0])
    g.append(ribbon(doc, extras["olive"], [5], f"{gid}-data-extra", "extra data-dependent component  (5)", **st)[0])
    th = stripe_point(left, lcls, 1, F.band(0, 0.58)[1], sp=st["sp"])
    a, b, c = wine_ends
    g.append(ribbon(doc, [a, b, th, c], [4], f"{gid}-loss-level", "ℒ level set  (4)", **st)[0])
    g.append("</g>")
    return "\n".join(g), th, F.band(ax, 0.2), left


def theta_points(doc, th, tt, F, fid, th_dx=-2.9):
    return ('<g id="theta-points" inkscape:label="θ, θ̃">' + dot("theta", *th, INK) + dot("theta-tilde", *tt, INK)
            + doc.text(th[0] + th_dx, th[1] - 0.9, "θ", POINT_FS, INK, "end", idbase="theta-label", container=fid)
            + text(doc, tt[0] + 1.2, tt[1], "θ" + TILDE, POINT_FS, INK, vcenter=True, idbase="theta-tilde-label",
                   container=fid)
            + "</g>")


BLOB_F = [1.0, 0.94, 1.0, 0.95, 1.0, 1.06, 0.93, 1.02]  # radial factors of the ℱ blob


def blob_polygon(cx, cy, rx, ry, factors):
    n = len(factors)
    return sample([(cx + rx * f * math.cos(2 * math.pi * i / n), cy + ry * f * math.sin(2 * math.pi * i / n))
                   for i, f in enumerate(factors)], True)


def inside_margin(p, poly):
    """Signed distance from p to the polygon boundary: > 0 inside, < 0 outside."""
    x, y = p
    inside, dmin = False, float("inf")
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            inside = not inside
        dx, dy = x2 - x1, y2 - y1
        t = max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy or 1.0)))
        dmin = min(dmin, math.hypot(x - x1 - t * dx, y - y1 - t * dy))
    return dmin if inside else -dmin


def clip_inside(ctrl, poly, anchor, margin):
    """Keep the stretch of the curve through `anchor` that stays >= margin inside poly; return new control points."""
    dense = sample(ctrl)
    i = min(range(len(dense)), key=lambda j: math.hypot(dense[j][0] - anchor[0], dense[j][1] - anchor[1]))
    i0 = i1 = i
    while i0 > 0 and inside_margin(dense[i0 - 1], poly) >= margin:
        i0 -= 1
    while i1 < len(dense) - 1 and inside_margin(dense[i1 + 1], poly) >= margin:
        i1 += 1
    return resample(dense[i0:i1 + 1], 2.5, False)


def f_space(doc, cx, cy, rx, ry, style, st, name_xy, name_anchor="end", fth_label="f_θ", margin=1.6, lab_dx=1.6):
    sp = [blob(doc, "F-blob", cx, cy, rx, ry, BLOB_F, "ℱ", style=style),
          doc.text(*name_xy, "ℱ", SPACE_FS, INK, name_anchor, idbase="F-name")]
    poly = blob_polygon(cx, cy, rx, ry, BLOB_F)
    fth = (cx - 0.13 * rx, cy + 0.09 * ry)
    k = rx / 15.5
    level = [(cx - 13.0 * k, fth[1] + 5.0 * k), (cx - 8.0 * k, fth[1] + 2.8 * k), fth,
             (cx + 5.0 * k, fth[1] - 3.6 * k), (cx + 11.5 * k, fth[1] - 5.4 * k)]
    fibre = [(cx - 6.0 * k, cy - 0.74 * ry), (cx - 4.2 * k, fth[1] - 0.42 * ry), fth,
             (cx - 0.5 * k, fth[1] + 0.42 * ry), (cx + 0.1 * k, cy + 0.82 * ry)]
    g = ['<g id="F-sets" inkscape:label="sets in ℱ">',
         ribbon(doc, clip_inside(level, poly, fth, margin), [3], "F-loss-level", "level set of ℒ_F  (3)", **st)[0],
         ribbon(doc, clip_inside(fibre, poly, fth, margin), [5], "F-restriction-fibre", "fibre of i  (5)", **st)[0],
         "</g>"]
    pts = ('<g id="F-points" inkscape:label="f_θ">' + dot("f-theta", *fth, COL[2])
           + doc.text(fth[0] + lab_dx, fth[1] + 3.0, fth_label, POINT_FS, INK, "start", sp=THIN, idbase="f-theta-label")
           + "</g>")
    return sp, "\n".join(g), pts


def fx_space(doc, cx, cy, rx, ry, style, name_xy, name_anchor="middle"):
    sp = [blob(doc, "FX-blob", cx, cy, rx, ry, [1.0, 0.95, 1.0, 1.05, 0.97, 1.0, 1.04, 0.96], "ℱ|X′", style=style),
          doc.text(*name_xy, "ℱ_{|X'}", SPACE_FS, INK, name_anchor, sp=HAIR, idbase="FX-name")]
    pts = ('<g id="FX-points" inkscape:label="i(f_θ)">' + dot("i-f-theta", cx, cy - 0.8, COL[5])
           + doc.text(cx, cy + 2.6, "i(f_θ)", POINT_FS, INK, "middle", sp=HAIR, idbase="i-f-theta-label") + "</g>")
    return sp, pts


def agg_box(doc, agg, fill="#ffffff"):
    return ('<g id="agg" inkscape:label="AGG">'
            + doc.rect("agg-box", *agg, f"fill:{fill};stroke:{GREY};stroke-width:0.33", rx=0.6, label="box")
            + doc.text(agg[0] + agg[2] / 2, agg[1] + agg[3] / 2, "AGG", 6.5 * PT, INK, "middle", vcenter=True,
                       idbase="agg-text", container="agg-box")
            + "</g>")


def panel_label(doc):
    return doc.text(2.0, 5.2, "\\b", 10 * PT, INK, family=BOLD, weight="bold", idbase="panel-label")


# ------------------------------------------------------------------ figure
def build():
    doc = Doc()
    OUT = FRAME_STYLE  # grey version of the left-panel frames
    st = dict(w=0.32, sp=0.62)  # thin lines with visible gaps
    spaces, sets, points, maps = [panel_label(doc)], [], [], []

    # Θ' (top left) and Θ (middle left)
    P = Frame(3.0, 7.5, 42.0, 24.0, top=7.0, bottom=2.5)
    T = Frame(3.0, 37.5, 42.0, 42.0)
    for fid, Fr, name in (("thetap-frame", P, "Θ' ⊆ ℝ^m"), ("theta-frame", T, "Θ ⊆ ℝ^n")):
        spaces.append(doc.rect(fid, Fr.x, Fr.y, Fr.w, Fr.h, OUT, rx=1.6, label=name))
        spaces.append(doc.text(Fr.x + 2.0, Fr.y + 4.3, name, SPACE_FS, INK, sp=HAIR, container=fid, idbase=fid[:-6]))

    ax = 15.5
    extras = dict(loop=ellipse(30.8, T.band(0, .40)[1], 3.3, 6.6),
                  green=[T.band(25.8, .93), T.band(30.0, .80), T.band(35.3, .83), T.band(38.5, .98)],
                  olive=[T.band(42.0, .02), T.band(40.4, .27), T.band(41.0, .53), T.band(42.3, .72)])
    s, th, tt, _ = theta_sets(doc, T, ax, 0.74, extras, (T.band(4.9, .90), T.band(6.8, .74), T.band(12.6, .40)), st)
    sets.append(s)
    points.append(theta_points(doc, th, tt, T, "theta-frame"))

    g = ['<g id="thetap-sets" inkscape:label="sets in Θ′">']
    g.append(ribbon(doc, [P.band(5.5, 1.0), P.band(10.5, .45), P.band(17.5, .25), P.band(25.0, .45)], [2, 3, 5],
                    "thetap-fibre-a", "fibre component  (2)(3)(5)", **st)[0])
    g.append(ribbon(doc, ellipse(33.0, P.band(0, .45)[1], 3.0, 4.6), [2, 3, 5], "thetap-fibre-b",
                    "fibre component  (2)(3)(5)", closed=True, **st)[0])
    g.append(ribbon(doc, [P.band(13.0, 1.0), P.band(19.0, .80), P.band(26.0, .95)], [3], "thetap-loss-f-extra",
                    "extra level-set component  (3)", **st)[0])
    g.append(ribbon(doc, [P.band(22.0, 0.0), P.band(25.5, .10), P.band(28.0, .02)], [5], "thetap-data-extra",
                    "extra data-dependent component  (5)", **st)[0])
    g.append(ribbon(doc, [P.band(39.5, .05), P.band(41.5, .50), P.band(40.0, 1.0)], [4], "thetap-loss-level",
                    "ℒ level set  (4)", **st)[0])
    g.append("</g>")
    sets.append("\n".join(g))

    # ℱ (middle right, level with Θ) and ℱ|X' (top right, level with Θ')
    FCX, FCY, FRX, FRY = 72.5, T.y + T.h / 2, 15.0, 11.5
    sp_, s, p = f_space(doc, FCX, FCY, FRX, FRY, OUT, st, (FCX + 0.72 * FRX + 0.6, FCY - 0.72 * FRY - 0.9), "start",
                        fth_label="f_θ=φ(θ)", lab_dx=2.9)  # clear of the olive curve (italic f overhangs left)
    spaces += sp_
    sets.append(s)
    points.append(p)
    RCX, RCY = 72.5, P.y + P.h / 2
    sp_, p = fx_space(doc, RCX, RCY, 11.0, 7.0, OUT, (RCX - 11.5, RCY - 7.6), "end")
    spaces += sp_
    points.append(p)

    # losses
    YR = T.y + T.h + 13.0
    agg = (43.5, YR + 9.5, 10.0, 5.6)
    YL = agg[1] + agg[3] + 12.8
    s, xr = real_line(doc, "R-reg", 14.0, 34.0, YR, "ℒ_R(θ)", INK)
    spaces.append(s)
    s, xf = real_line(doc, "R-fun", FCX - 10.0, FCX + 10.0, YR, "ℒ_F(f_θ)", COL[3])
    spaces.append(s)
    s, xl = real_line(doc, "R-loss", 39.5, 57.5, YL, "ℒ(θ)", COL[4])
    spaces.append(s)
    spaces.append(agg_box(doc, agg))

    ftop, fbot = FCY - FRY, FCY + FRY
    maps.append('<g id="map-phi" inkscape:label="φ: Θ → ℱ">'
                + arrow(doc, "phi-arrow", [(T.x + T.w + 1.2, FCY), (FCX - FRX - 1.3, FCY)], "arrow")
                + mapl(doc, "phi-label", (T.x + T.w + FCX - FRX) / 2, FCY - 2.0, "φ", "middle") + "</g>")
    maps.append('<g id="map-phi-prime" inkscape:label="φ: Θ′ → ℱ">'
                + arrow(doc, "phip-arrow", [(P.x + P.w + 1.2, P.y + P.h - 3.0), (59.5, P.y + P.h - 1.0),
                                            (FCX - 0.75 * FRX * 1.06 - 0.6, FCY - 0.75 * FRY * 1.06 - 1.0)], "arrow")
                + mapl(doc, "phip-label", 53.2, P.y + P.h + 6.0, "φ", "end") + "</g>")
    maps.append('<g id="map-i" inkscape:label="i: ℱ → ℱ|X′">'
                + arrow(doc, "i-arrow", [(FCX + 2.5, ftop - 1.2), (FCX + 2.5, RCY + 7.0 + 1.3)], "arrow")
                + mapl(doc, "i-label", FCX + 3.9, (ftop + RCY + 7.0) / 2, "i", "start") + "</g>")
    maps.append('<g id="map-LF" inkscape:label="ℒ_F: ℱ → ℝ">'
                + arrow(doc, "LF-arrow", [(xf, fbot + 1.3), (xf, YR - 1.6)], "arrow")
                + mapl(doc, "LF-label", xf + 1.4, (fbot + YR) / 2, "ℒ_F", "start") + "</g>")
    maps.append('<g id="map-LR" inkscape:label="ℒ_R: Θ → ℝ">'
                + arrow(doc, "LR-arrow", [(xr, T.y + T.h + 1.2), (xr, YR - 1.6)], "arrow")
                + mapl(doc, "LR-label", xr + 1.4, (T.y + T.h + YR) / 2, "ℒ_R", "start") + "</g>")
    maps.append('<g id="map-agg-in" inkscape:label="into AGG">'
                + arrow(doc, "agg-in-R", [(34.8, YR + 0.7), (agg[0] - 0.6, agg[1] + 1.2)], "from ℒ_R")
                + arrow(doc, "agg-in-F", [(xf - 10.8, YR + 0.7), (agg[0] + agg[2] + 0.6, agg[1] + 1.2)], "from ℒ_F")
                + "</g>")
    maps.append('<g id="map-agg-out" inkscape:label="AGG → ℝ">'
                + arrow(doc, "agg-out", [(agg[0] + agg[2] / 2, agg[1] + agg[3] + 0.8), (agg[0] + agg[2] / 2, YL - 1.5)],
                        "arrow") + "</g>")

    # legend: line sample + class number + set, bottom right
    lx, ly0, lh = 62.5, YR + 9.0, 4.3
    leg = ['<g id="legend" inkscape:label="legend">']
    for r, (k, s) in enumerate(LEGEND_SETS):
        y = ly0 + r * lh
        leg.append(f'<g id="legend-{k}" inkscape:label="{escape(NAMES[k])}">'
                   f'<path d="M {lx:.1f},{y:.1f} L {lx + 3.5:.1f},{y:.1f}" style="fill:none;stroke:{COL[k]};'
                   f'stroke-width:0.6;stroke-linecap:round"/>'
                   + doc.text(lx + 4.6, y, str(k), LEG_FS, COL[k], "start", vcenter=True, family=BOLD, weight="bold",
                              idbase=f"legend-{k}-num")
                   + text(doc, lx + 6.6, y, s, LEG_FS, INK, vcenter=True, idbase=f"legend-{k}-text") + "</g>")
    leg.append("</g>")
    layers = [("spaces", "Spaces", spaces), ("maps", "Maps", maps), ("sets", "Sets", sets),
              ("points", "Points", points), ("legend", "Legend", leg)]
    return assemble(doc, layers, "Parameter-space symmetries, right panel"), doc


def assemble(doc, layers, title):
    """layers: [(id, Inkscape label, [svg snippets])] in drawing order."""
    body = "\n".join(f'<g id="layer-{lid}" inkscape:groupmode="layer" inkscape:label="{lab}">\n'
                     + "\n".join(parts) + "\n</g>" for lid, lab, parts in layers)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
     width="{f1(PAGE_W)}mm" height="{f1(PAGE_H)}mm" viewBox="0 0 {f1(PAGE_W)} {f1(PAGE_H)}" version="1.1">
<title>{escape(title)}</title>
<sodipodi:namedview id="namedview" pagecolor="#ffffff" inkscape:document-units="mm" units="mm"/>
<defs>
{chr(10).join(doc.markers.values())}
</defs>
{body}
</svg>
"""


def check(out, doc):
    """Validator of the left panel + page-edge margin + arrow length >= 10 mm."""
    issues = validate(out, doc)
    for ln in inkscape(out, "--query-all").splitlines():
        p = ln.split(",")
        if len(p) == 5 and p[0] in doc.texts:
            x, y, w, h = (float(v) * 25.4 / 96 for v in p[1:])
            if x < 1.0 or y < 1.0 or x + w > PAGE_W - 1.0 or y + h > PAGE_H - 1.0:
                issues.append(f"{p[0]} within 1 mm of the page edge")
    issues += [f"arrow {a} is {L:.1f} mm (< 10)" for a, L in getattr(doc, "arrows", []) if L < 9.95]
    return issues


if __name__ == "__main__":
    out = sys.argv[1]
    svg, doc = build()
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(svg)
    issues = check(out, doc)
    print(f"{out}: {PAGE_W} x {PAGE_H} mm | {len(issues)} issue(s)")
    for i in issues:
        print("   ", i)
