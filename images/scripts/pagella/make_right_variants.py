"""Right panel (b), unused alternatives (the chosen layout, former variant B, is make_right_final.py).

A  parameter spaces side by side on top, flow downwards; grey-filled spaces, touching stripes, badge legend.
C  "Θ as hero": large Θ with direct colour labels (no legend), compact diagram below; warm fills.

Usage: python3 make_right_variants.py OUTDIR   -> OUTDIR/param-space-symmetries_right_{A,C}.svg
"""
import math
import os
import sys
from xml.sax.saxutils import escape

from make_right_final import *  # noqa: F401,F403  (primitives, helpers, styles)
from make_right_final import COL, Doc, SPACE_STYLE, TILDE, assemble, check


# ====================================================================== variant A
def build_A():
    doc = Doc()
    C = COL
    spaces, sets, points, maps = [], [], [], []

    # ---------------- vertical layout (everything below the parameter spaces follows from TH)
    TX, TY, TW, TH = 3.0, 7.5, 53.0, 49.0
    TB = TY + TH                      # bottom of Θ and Θ'
    FCX, FRX, FRY = 39.5, 15.5, 11.5  # ℱ blob
    FCY = TB + 13.0 + FRY
    YR = FCY + FRY + 13.0             # the two copies of ℝ feeding AGG
    agg = (19.5, YR + 11.5, 10.0, 5.6)
    YL = agg[1] + agg[3] / 2          # ℝ carrying ℒ(θ)

    def band(x, v, top=TY + 7.5, bot=TB - 3.5):
        return (x, top + v * (bot - top))

    # ---------------- parameter space Θ
    spaces.append(doc.rect("theta-frame", TX, TY, TW, TH, SPACE_STYLE, rx=1.6, label="Θ frame"))
    spaces.append(doc.text(TX + 2.0, TY + 4.3, "Θ ⊆ ℝ^n", SPACE_FS, INK, sp=HAIR, container="theta-frame",
                           idbase="theta-name"))
    ax = 20.0  # θ̃ orbit; the two components of Gθ are mirror images about it
    left = [band(13.0, 0.0), band(11.0, 0.25), band(10.5, 0.5), band(11.3, 0.75), band(13.5, 1.0)]
    right = [(2 * ax - x, y) for x, y in left]
    lcls, rcls = [5, 3, 2, 1], [1, 2, 3, 5]  # orbit stripe on the side facing θ̃'s orbit
    g = ['<g id="theta-sets" inkscape:label="sets in Θ">']
    g.append(ribbon(doc, left, lcls, "theta-orbit-a", "Gθ, component through θ  (1)(2)(3)(5)")[0])
    g.append(ribbon(doc, right, rcls, "theta-orbit-b", "Gθ, second component  (1)(2)(3)(5)")[0])
    g.append(ribbon(doc, [band(ax, 0.0), band(ax, 1.0)], [1], "theta-tilde-orbit", "Gθ̃  (1)")[0])
    lc = band(37.5, 0.40)
    g.append(ribbon(doc, [(lc[0] + 4.2 * math.cos(a), lc[1] + 7.6 * math.sin(a))
                          for a in (2 * math.pi * i / 8 for i in range(8))],
                    [2, 3, 5], "theta-fibre-extra", "extra fibre component  (2)(3)(5)", closed=True)[0])
    g.append(ribbon(doc, [band(32.5, 0.93), band(38.0, 0.80), band(44.5, 0.83), band(48.0, 0.98)], [3],
                    "theta-loss-f-extra", "extra level-set component  (3)")[0])
    g.append(ribbon(doc, [band(51.5, 0.02), band(49.8, 0.27), band(50.5, 0.53), band(52.5, 0.72)], [5],
                    "theta-data-extra", "extra data-dependent component  (5)")[0])
    th = stripe_point(left, lcls, 1, band(0, 0.58)[1])
    g.append(ribbon(doc, [band(4.8, 0.88), band(7.9, 0.72), th, band(16.4, 0.40)], [4], "theta-loss-level",
                    "ℒ level set  (4)")[0])
    g.append("</g>")
    sets.append("\n".join(g))
    tt = band(ax, 0.2)
    points.append('<g id="theta-points" inkscape:label="θ, θ̃">'
                  + dot("theta", *th, INK) + dot("theta-tilde", *tt, INK)
                  + doc.text(th[0] - 2.9, th[1] - 0.9, "θ", POINT_FS, INK, "end", idbase="theta-label",
                             container="theta-frame")
                  + tilde_fix(doc.text(tt[0] + 1.2, tt[1], "θ" + TILDE, POINT_FS, INK, "start", vcenter=True,
                                       idbase="theta-tilde-label", container="theta-frame"), POINT_FS)
                  + "</g>")

    # ---------------- parameter space Θ'
    PX, PW = 60.0, 29.5
    spaces.append(doc.rect("thetap-frame", PX, TY, PW, TH, SPACE_STYLE, rx=1.6, label="Θ′ frame"))
    spaces.append(doc.text(PX + 2.0, TY + 4.3, "Θ' ⊆ ℝ^m", SPACE_FS, INK, sp=HAIR, container="thetap-frame",
                           idbase="thetap-name"))
    g = ['<g id="thetap-sets" inkscape:label="sets in Θ′">']
    g.append(ribbon(doc, [band(65.0, 0.0), band(63.8, 0.26), band(64.4, 0.53), band(66.8, 0.79), band(70.5, 0.98)],
                    [2, 3, 5], "thetap-fibre-a", "fibre component  (2)(3)(5)")[0])
    g.append(ribbon(doc, [band(72.0, 0.0), band(73.6, 0.24), band(72.8, 0.48)], [2, 3, 5], "thetap-fibre-b",
                    "fibre component  (2)(3)(5)")[0])
    g.append(ribbon(doc, [band(79.5, 0.02), band(78.2, 0.29), band(79.8, 0.55)], [3], "thetap-loss-f-extra",
                    "extra level-set component  (3)")[0])
    g.append(ribbon(doc, [band(75.0, 0.98), band(78.5, 0.83), band(83.5, 0.88)], [5], "thetap-data-extra",
                    "extra data-dependent component  (5)")[0])
    g.append(ribbon(doc, [band(86.0, 0.0), band(84.6, 0.29), band(86.0, 0.59)], [4], "thetap-loss-level",
                    "ℒ level set  (4)")[0])
    g.append("</g>")
    sets.append("\n".join(g))

    # ---------------- function space ℱ
    ff = [1.0, 0.94, 1.0, 0.95, 1.0, 1.06, 0.93, 1.02]
    spaces.append(blob(doc, "F-blob", FCX, FCY, FRX, FRY, ff, "ℱ"))
    spaces.append(doc.text(FCX - 0.75 * FRX * ff[5] - 1.0, FCY - 0.75 * FRY * ff[5] - 0.6, "ℱ", SPACE_FS, INK,
                           "end", idbase="F-name"))
    fth = (FCX - 2.0, FCY + 1.0)
    g = ['<g id="F-sets" inkscape:label="sets in ℱ">']
    g.append(ribbon(doc, [(FCX - 13.0, fth[1] + 5.0), (FCX - 8.0, fth[1] + 2.8), fth, (FCX + 5.0, fth[1] - 3.6),
                          (FCX + 11.5, fth[1] - 5.4)], [3], "F-loss-level", "level set of ℒ_F  (3)")[0])
    g.append(ribbon(doc, [(FCX - 6.0, FCY - 8.5), (FCX - 4.2, fth[1] - 4.6), fth, (FCX - 0.5, fth[1] + 4.6),
                          (FCX + 0.1, FCY + 9.4)], [5], "F-restriction-fibre", "fibre of i  (5)")[0])
    g.append("</g>")
    sets.append("\n".join(g))
    points.append('<g id="F-points" inkscape:label="f_θ">' + dot("f-theta", *fth, C[2])
                  + doc.text(fth[0] + 1.6, fth[1] + 3.0, "f_θ", POINT_FS, INK, "start", sp=HAIR,
                             idbase="f-theta-label") + "</g>")

    # ---------------- restricted function space ℱ|X'
    RCX, RCY = 78.5, FCY + 0.5
    spaces.append(blob(doc, "FX-blob", RCX, RCY, 9.5, 6.5, [1.0, 0.95, 1.0, 1.05, 0.97, 1.0, 1.04, 0.96], "ℱ|X′"))
    spaces.append(doc.text(RCX, RCY - 8.5, "ℱ_{|X'}", SPACE_FS, INK, "middle", sp=HAIR, idbase="FX-name"))
    points.append('<g id="FX-points" inkscape:label="i(f_θ)">' + dot("i-f-theta", RCX, RCY - 0.8, C[5])
                  + doc.text(RCX, RCY + 2.6, "i(f_θ)", POINT_FS, INK, "middle", sp=HAIR, idbase="i-f-theta-label")
                  + "</g>")

    # ---------------- copies of ℝ and aggregation
    s, xr = real_line(doc, "R-reg", 4.0, 18.0, YR, "ℒ_R(θ)", INK)
    spaces.append(s)
    s, xf = real_line(doc, "R-fun", 30.0, 49.0, YR, "ℒ_F(f_θ)", C[3])
    spaces.append(s)
    s, _ = real_line(doc, "R-loss", 42.0, 60.0, YL, "ℒ(θ)", C[4])
    spaces.append(s)
    spaces.append('<g id="agg" inkscape:label="AGG">'
                  + doc.rect("agg-box", *agg, f"fill:#ffffff;stroke:{GREY};stroke-width:0.33", rx=0.6, label="box")
                  + doc.text(agg[0] + agg[2] / 2, agg[1] + agg[3] / 2, "AGG", 6.5 * PT, INK, "middle", vcenter=True,
                             idbase="agg-text", container="agg-box")
                  + "</g>")

    # ---------------- maps
    def map_label(lid, x, y, s, anchor):
        return doc.text(x, y, s, MAP_FS, INK, anchor, sp=HAIR, vcenter=True, idbase=lid)

    ftop = FCY - FRY
    maps.append('<g id="map-phi" inkscape:label="φ: Θ → ℱ">'
                + arrow(doc, "phi-arrow", [(FCX + 0.5, TB + 1.5), (FCX + 0.5, ftop - 1.2)], "arrow")
                + map_label("phi-label", FCX - 0.8, (TB + ftop) / 2, "φ", "end") + "</g>")
    maps.append('<g id="map-phi-prime" inkscape:label="φ: Θ′ → ℱ">'
                + arrow(doc, "phip-arrow", [(68.0, TB + 1.5), (65.0, ftop + 1.0), (54.2, ftop + 4.5)], "arrow")
                + map_label("phip-label", 61.0, ftop - 1.6, "φ", "end") + "</g>")
    maps.append('<g id="map-i" inkscape:label="i: ℱ → ℱ|X′">'
                + arrow(doc, "i-arrow", [(FCX + FRX + 1.4, RCY), (RCX - 9.5 * 0.97 - 1.6, RCY)], "arrow")
                + map_label("i-label", (FCX + FRX + RCX - 9.5) / 2, RCY - 2.0, "i", "middle") + "</g>")
    maps.append('<g id="map-LF" inkscape:label="ℒ_F: ℱ → ℝ">'
                + arrow(doc, "LF-arrow", [(xf, FCY + FRY + 1.3), (xf, YR - 1.6)], "arrow")
                + map_label("LF-label", xf + 1.4, (FCY + FRY + YR) / 2, "ℒ_F", "start") + "</g>")
    maps.append('<g id="map-LR" inkscape:label="ℒ_R: Θ → ℝ">'
                + arrow(doc, "LR-arrow", [(xr, TB + 1.5), (xr, YR - 1.6)], "arrow")
                + map_label("LR-label", xr + 1.4, FCY + 4.0, "ℒ_R", "start") + "</g>")
    maps.append('<g id="map-agg-in" inkscape:label="into AGG">'
                + arrow(doc, "agg-in-R", [(18.8, YR + 0.8), (22.2, agg[1] - 0.8)], "from ℒ_R")
                + arrow(doc, "agg-in-F", [(29.2, YR + 0.8), (26.8, agg[1] - 0.8)], "from ℒ_F")
                + "</g>")
    maps.append('<g id="map-agg-out" inkscape:label="AGG → ℝ">'
                + arrow(doc, "agg-out", [(agg[0] + agg[2] + 0.8, YL), (41.0, YL)], "arrow") + "</g>")

    # ---------------- legend (bottom right, one entry per line)
    entries = [(1, "Gθ,  Gθ" + TILDE), (2, "φ^{−1}(f_θ)"), (3, "φ^{−1}(ℒ_F^{−1}(ℒ_F(f_θ)))"),
               (4, "ℒ^{−1}(ℒ(θ))"), (5, "φ^{−1}(i^{−1}(i(f_θ)))")]
    lx, ly0, lh = 64.0, YR - 2.0, 4.4
    leg = ['<g id="legend" inkscape:label="legend">']
    for r, (k, s) in enumerate(entries):
        y = ly0 + r * lh
        leg.append(f'<g id="legend-{k}" inkscape:label="{escape(NAMES[k])}">' + badge(doc, k, lx, y)
                   + tilde_fix(doc.text(lx + 3.8, y, s, LEG_FS, INK, "start", sp=HAIR, vcenter=True,
                                        idbase=f"legend-{k}-text"), LEG_FS)
                   + "</g>")
    leg.append("</g>")

    panel_label = doc.text(2.0, 5.2, "\\b", 10 * PT, INK, family=BOLD, weight="bold", idbase="panel-label")
    layers = [("spaces", "Spaces", [panel_label] + spaces), ("maps", "Maps", maps), ("sets", "Sets", sets),
              ("points", "Points", points), ("legend", "Legend", leg)]
    return assemble(doc, layers, "Parameter-space symmetries, right panel"), doc


# ====================================================================== variant C
def build_C():
    doc = Doc()
    WARM = "fill:#efe9e1;stroke:none"
    st = dict(w=0.45, sp=0.62)  # stripes with thin gaps
    spaces, sets, points, maps, labels = [panel_label(doc)], [], [], [], []

    T = Frame(3.0, 7.5, 86.0, 52.0, top=7.5, bottom=8.5)
    spaces.append(doc.rect("theta-frame", T.x, T.y, T.w, T.h, WARM, rx=1.6, label="Θ ⊆ ℝ^n"))
    spaces.append(doc.text(T.x + 2.0, T.y + 4.3, "Θ ⊆ ℝ^n", SPACE_FS, INK, sp=HAIR, container="theta-frame",
                           idbase="theta-name"))
    ax = 31.5
    loop_c = T.band(54.0, .42)
    extras = dict(loop=ellipse(loop_c[0], loop_c[1], 4.6, 8.4),
                  green=[T.band(47.0, .97), T.band(54.0, .82), T.band(61.0, .85), T.band(65.0, 1.0)],
                  olive=[T.band(80.5, .0), T.band(78.8, .27), T.band(79.6, .53), T.band(81.8, .75)])
    s, th, tt, left = theta_sets(doc, T, ax, 1.0, extras, (T.band(9.0, .97), T.band(13.5, .78), T.band(28.0, .40)), st)
    sets.append(s)
    points.append(theta_points(doc, th, tt, T, "theta-frame"))

    # direct labels in class colours
    yb = T.y1 + 3.6
    lab = [
        (left[-1][0], yb, "Gθ", 1, "middle"), (ax, yb, "Gθ" + TILDE, 1, "middle"), (2 * ax - left[-1][0], yb, "Gθ", 1, "middle"),
        (T.x0 + 0.5, yb, "ℒ^{−1}(ℒ(θ))", 4, "start"),
        (loop_c[0] + 7.0, loop_c[1], "φ^{−1}(f_θ)", 2, "start"),
        (66.5, T.band(0, 1.0)[1], "φ^{−1}(ℒ_F^{−1}(ℒ_F(f_θ)))", 3, "start"),
        (76.6, T.band(0, .12)[1], "φ^{−1}(i^{−1}(i(f_θ)))", 5, "end"),
    ]
    g = ['<g id="direct-labels" inkscape:label="direct labels">']
    for i, (x, y, s_, k, anchor) in enumerate(lab):
        g.append(text(doc, x, y, s_, POINT_FS, COL[k], anchor, vcenter=True, idbase=f"dlabel-{k}",
                      container="theta-frame"))
    g.append("</g>")
    labels.append("\n".join(g))

    # ℱ, Θ' and ℱ|X' below
    TB = T.y + T.h
    FCX, FRX, FRY = 40.0, 10.5, 9.0
    FCY = TB + 12.6 + FRY
    sp_, s, p = f_space(doc, FCX, FCY, FRX, FRY, WARM, st, (FCX - 0.75 * FRX - 1.2, FCY - 0.75 * FRY - 1.4))
    spaces += sp_
    sets.append(s)
    points.append(p)

    P = Frame(64.0, TB + 6.0, 25.5, 32.0, top=7.0, bottom=2.5)
    spaces.append(doc.rect("thetap-frame", P.x, P.y, P.w, P.h, WARM, rx=1.6, label="Θ′ ⊆ ℝ^m"))
    spaces.append(doc.text(P.x + 2.0, P.y + 4.3, "Θ' ⊆ ℝ^m", SPACE_FS, INK, sp=HAIR, container="thetap-frame",
                           idbase="thetap-name"))
    g = ['<g id="thetap-sets" inkscape:label="sets in Θ′">']
    g.append(ribbon(doc, [P.band(67.0, 0.0), P.band(66.2, .35), P.band(67.2, .7), P.band(70.5, 1.0)], [2, 3, 5],
                    "thetap-fibre-a", "fibre component  (2)(3)(5)", **st)[0])
    g.append(ribbon(doc, [P.band(72.5, 0.0), P.band(74.0, .3), P.band(73.2, .58)], [2, 3, 5], "thetap-fibre-b",
                    "fibre component  (2)(3)(5)", **st)[0])
    g.append(ribbon(doc, [P.band(79.0, .02), P.band(77.9, .3), P.band(79.2, .6)], [3], "thetap-loss-f-extra",
                    "extra level-set component  (3)", **st)[0])
    g.append(ribbon(doc, [P.band(75.0, 1.0), P.band(78.5, .82), P.band(83.5, .9)], [5], "thetap-data-extra",
                    "extra data-dependent component  (5)", **st)[0])
    g.append(ribbon(doc, [P.band(85.2, 0.0), P.band(84.0, .3), P.band(85.2, .62)], [4], "thetap-loss-level",
                    "ℒ level set  (4)", **st)[0])
    g.append("</g>")
    sets.append("\n".join(g))

    RCX, RCY = 77.0, P.y + P.h + 16.5
    sp_, p = fx_space(doc, RCX, RCY, 10.0, 6.0, WARM, (RCX + 10.0, RCY - 7.6), "end")
    spaces += sp_
    points.append(p)

    YR = FCY + FRY + 13.1
    agg = (18.5, YR + 11.4, 10.0, 5.6)
    YL = agg[1] + agg[3] / 2
    s, xr = real_line(doc, "R-reg", 3.5, 17.5, YR, "ℒ_R(θ)", INK)
    spaces.append(s)
    s, xf = real_line(doc, "R-fun", FCX - 10.0, FCX + 9.0, YR, "ℒ_F(f_θ)", COL[3])
    spaces.append(s)
    s, xl = real_line(doc, "R-loss", 40.8, 57.5, YL, "ℒ(θ)", COL[4])
    spaces.append(s)
    spaces.append(agg_box(doc, agg))

    ftop, fbot = FCY - FRY, FCY + FRY
    maps.append('<g id="map-phi" inkscape:label="φ: Θ → ℱ">'
                + arrow(doc, "phi-arrow", [(FCX, TB + 1.2), (FCX, ftop - 1.2)], "arrow")
                + mapl(doc, "phi-label", FCX - 1.4, (TB + ftop) / 2, "φ", "end") + "</g>")
    maps.append('<g id="map-phi-prime" inkscape:label="φ: Θ′ → ℱ">'
                + arrow(doc, "phip-arrow", [(P.x - 1.2, FCY), (FCX + FRX + 1.3, FCY)], "arrow")
                + mapl(doc, "phip-label", (P.x + FCX + FRX) / 2, FCY - 2.0, "φ", "middle") + "</g>")
    maps.append('<g id="map-i" inkscape:label="i: ℱ → ℱ|X′">'
                + arrow(doc, "i-arrow", [(FCX + 0.62 * FRX, fbot - 1.2), (FCX + 0.95 * FRX, RCY + 0.5),
                                         (RCX - 10.0 * 0.97 - 1.4, RCY)], "arrow")
                + mapl(doc, "i-label", 56.0, RCY - 8.0, "i", "middle") + "</g>")
    maps.append('<g id="map-LF" inkscape:label="ℒ_F: ℱ → ℝ">'
                + arrow(doc, "LF-arrow", [(xf, fbot + 1.3), (xf, YR - 1.6)], "arrow")
                + mapl(doc, "LF-label", xf - 1.4, (fbot + YR) / 2, "ℒ_F", "end") + "</g>")
    maps.append('<g id="map-LR" inkscape:label="ℒ_R: Θ → ℝ">'
                + arrow(doc, "LR-arrow", [(xr, TB + 1.2), (xr, YR - 1.6)], "arrow")
                + mapl(doc, "LR-label", xr + 1.4, FCY, "ℒ_R", "start") + "</g>")
    maps.append('<g id="map-agg-in" inkscape:label="into AGG">'
                + arrow(doc, "agg-in-R", [(18.2, YR + 0.8), (21.4, agg[1] - 0.8)], "from ℒ_R")
                + arrow(doc, "agg-in-F", [(xf - 10.6, YR + 0.8), (25.6, agg[1] - 0.8)], "from ℒ_F")
                + "</g>")
    maps.append('<g id="map-agg-out" inkscape:label="AGG → ℝ">'
                + arrow(doc, "agg-out", [(agg[0] + agg[2] + 0.8, YL), (39.6, YL)], "arrow") + "</g>")

    layers = [("spaces", "Spaces", spaces), ("maps", "Maps", maps), ("sets", "Sets", sets),
              ("points", "Points", points), ("labels", "Direct labels", labels)]
    return assemble(doc, layers, "Parameter-space symmetries, right panel, variant C (Θ as hero)"), doc


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    for v, fn in (("A", build_A), ("C", build_C)):
        svg, doc = fn()
        path = os.path.join(outdir, f"param-space-symmetries_right_{v}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg)
        issues = check(path, doc)
        print(f"[{v}] {path}: {len(issues)} issue(s)")
        for i in issues:
            print("   ", i)
