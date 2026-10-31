"""Final left panel (variant B, 92 mm wide, 2 columns, A-style frames).

Reuses the helpers of make_left_variants.py. Usage: python3 make_left_final.py OUT.svg
"""
import math
import sys
from xml.sax.saxutils import escape

from make_left_variants import (BIG, BOLD, COL, GREY, HAIR, INK, LEG_FS, MED, MINI, NOTE_FS, PAD, PT,
                                SETUP_FS, SUBPLOTS, LINKS, TAG, TOP, W, Doc, Geom, draw_net, f1, frame_h,
                                net_points, number_tag, subset_glyph, validate, width)

PAGE_W = 92.0
MARGIN = 2.0
GAP_H, GAP_V = PAGE_W - 2 * W - 2 * 2.6, 10.0
GRID = {3: (0, 0), 5: (1, 0), 2: (0, 1), 6: (1, 1), 1: (0, 2), 4: (1, 2)}
FRAME = "fill:{c};fill-opacity:0.07;stroke:{c};stroke-width:0.35"  # as in variant A
LINK_COL, GLYPH_COL = "#888888", GREY

# Short name shown next to each number badge ('‐' is U+2010, a hyphen the math parser leaves alone).
NAMES = {1: "symmetric state", 2: "functional", 3: "loss (factoring)", 4: "loss",
         5: "data‐dependent", 6: "instance"}
NAME_FS = 6.5 * PT
NAME_EXTRA = 1.2  # extra frame headroom (mm) so names clear the network labels

SETUP_NET = Geom(E=10.0, r=2.2, F=11.0, dy=5.0, fs=8.5 * PT, sfs=7.5 * PT, lw=0.33, lwc=0.6)


def setup_block(doc, top):
    """Network N centred on the page, description lines below it."""
    g = SETUP_NET
    spec = dict(input=("x", None), th1=("θ_1", None), th2=("θ_2", None),
                eta=[("η_1", None), ("η_2", None), ("η_3", None)])
    bw, bh = 4.4, 2 * g.dy + 4.6
    _, n2_rel, xf_rel = net_points(0, g)
    in_w = width("x", g.fs, HAIR) + 0.6
    net_w = in_w + xf_rel + bw + 3.6 + width("ŷ_1", g.fs)
    sx0 = (PAGE_W - net_w) / 2 + in_w
    sy0 = top + bh / 2
    out = []
    body, ends = draw_net(doc, sx0, sy0, g, spec, None, softmax=True)
    out.append(body)
    n1, n2, xf = net_points(sx0, g)
    for k, (lab, _), (ex, ey) in zip((-1, 0, 1), spec["eta"], ends):
        px, py = n2 + 0.7 * (ex - n2), sy0 + 0.7 * (ey - sy0)
        yb = py - (1.7 if k < 0 else 0.9) if k < 1 else py + 1.3 + 0.7 * g.fs
        out.append(doc.text(px, yb, lab, g.fs, INK, "middle", sp=HAIR, idbase=f"setup-eta{k + 2}"))
    out.append(doc.rect("setup-softmax-box", xf, sy0 - bh / 2, bw, bh,
                        f"fill:#ffffff;stroke:{GREY};stroke-width:{g.lw:.2f}", rx=0.6, record=False))
    out.append(doc.text(xf + bw / 2, sy0, "softmax", 7.0 * PT, INK, "middle", vcenter=True, idbase="setup-softmax",
                        extra=f' transform="rotate(-90 {f1(xf + bw / 2)} {f1(sy0)})"'))
    for k in (-1, 0, 1):
        y = sy0 + k * g.dy
        out.append(doc.line(xf + bw, y, xf + bw + 3.0, y, GREY, g.lw))
        out.append(doc.text(xf + bw + 3.6, y, f"ŷ_{k + 2}", g.fs, INK, "start", vcenter=True,
                            idbase=f"setup-yhat{k + 2}"))
    lines = ["𝒩(x)=softmax(η σ(θ_2 σ(θ_1x))),  σ=\\ReLU",
             "ℒ(θ)=CE(𝒩(x), y),  y=[1, 0, 0]^⊤",
             "θ_1=1,  η_1=η_2=log 2,  η_3=0;  θ_2, x generic unless specified"]
    fs = SETUP_FS
    while max(width(s, fs, MED) for s in lines) > PAGE_W - 2 * MARGIN - 2:
        fs -= 0.1 * PT
    lw_ = max(width(s, fs, MED) for s in lines)
    tx = (PAGE_W - lw_) / 2
    lh = 1.45 * fs
    ty = sy0 + bh / 2 + 3.0 + 0.75 * fs
    for i, s in enumerate(lines):
        out.append(doc.text(tx, ty + i * lh, s, fs, INK, "start", sp=MED, idbase="setup-text"))
    return "\n".join(out), ty + (len(lines) - 1) * lh + 0.3 * fs, fs


def legend_row(doc, y):
    """Single centred row: sample + text for each entry."""
    entries = [("line", "changed by g"), ("swap", "swapped by g"), ("text", "arbitrary shifts")]
    sample_w = {"line": 5.0, "swap": 6.4, "text": width("Δ_i∈ℝ", LEG_FS)}
    gap_s, gap_e = 1.4, 4.5
    total = sum(sample_w[k] + gap_s + width(t, LEG_FS) for k, t in entries) + gap_e * (len(entries) - 1)
    x = (PAGE_W - total) / 2
    out = ['<g id="legend" inkscape:label="legend">']
    for kind, txt in entries:
        if kind == "line":
            out.append(doc.line(x, y, x + 5.0, y, GREY, MINI.lwc, guard=False))
        elif kind == "swap":
            out.append(doc.line(x, y, x + 3.6, y - 1.1, GREY, MINI.lwc, guard=False))
            out.append(doc.line(x, y, x + 3.6, y + 1.1, GREY, MINI.lwc, guard=False))
            keep = list(doc.segments)
            out.append(doc.swap_arc(x + 4.4, y - 1.1, y + 1.1, GREY, bulge=1.6, w=0.35))
            doc.segments = keep
        else:
            out.append(doc.text(x, y, "Δ_i∈ℝ", LEG_FS, INK, vcenter=True, idbase="legend"))
        x += sample_w[kind] + gap_s
        out.append(doc.text(x, y, txt, LEG_FS, INK, vcenter=True, idbase="legend"))
        x += width(txt, LEG_FS) + gap_e
    out.append("</g>")
    return "\n".join(out), total


def link(doc, sub, sup, frames):
    (c1, r1), (c2, r2) = GRID[sub], GRID[sup]
    x1, y1, w1, h1 = frames[sub]
    x2, y2, w2, h2 = frames[sup]
    if r1 == r2:  # horizontal, superset to the right/left
        d = 1 if c2 > c1 else -1
        ax, ay = (x1 + w1 + 1.0, y1 + h1 / 2) if d > 0 else (x1 - 1.0, y1 + h1 / 2)
        bx, by = (x2 - 1.0, y2 + h2 / 2) if d > 0 else (x2 + w2 + 1.0, y2 + h2 / 2)
    else:  # superset above: subset top edge -> superset bottom edge
        fa = 0.5 if c1 == c2 else (0.8 if c2 > c1 else 0.2)
        fb = 0.5 if c1 == c2 else (0.2 if c2 > c1 else 0.8)
        ax, ay = x1 + fa * w1, y1 - 1.0
        bx, by = x2 + fb * w2, y2 + h2 + 1.0
    L = math.hypot(bx - ax, by - ay)
    ux, uy = (bx - ax) / L, (by - ay) / L
    mx, my = (ax + bx) / 2, (ay + by) / 2
    gap = 2.1
    ang = math.degrees(math.atan2(by - ay, bx - ax))
    lid = f"incl-{sub}-in-{sup}"
    parts = [f'<g id="{lid}" inkscape:label="({sub}) ⊂ ({sup})">']
    if L / 2 - gap > 0.8:  # draw connector stubs only when there is room
        parts.append(doc.line(ax, ay, mx - gap * ux, my - gap * uy, LINK_COL, 0.3))
        parts.append(doc.line(mx + gap * ux, my + gap * uy, bx, by, LINK_COL, 0.3))
    parts.append(subset_glyph(doc, mx, my, ang, GLYPH_COL, lid))
    parts.append("</g>")
    return "".join(parts)


def build():
    doc = Doc()
    panel_label = doc.text(MARGIN, MARGIN + 3.2, "\\a", 10 * PT, INK, family=BOLD, weight="bold",
                           idbase="panel-label")
    setup_svg, setup_bottom, setup_fs = setup_block(doc, MARGIN + 3.0)

    nrows = 3
    row_h = {r: frame_h(max(len(SUBPLOTS[k]["notes"]) for k, (c, rr) in GRID.items() if rr == r))
             + NAME_EXTRA for r in range(nrows)}
    grid_x0 = (PAGE_W - (2 * W + GAP_H)) / 2
    y = setup_bottom + 6.5
    row_y = {}
    for r in range(nrows):
        row_y[r] = y
        y += row_h[r] + GAP_V
    grid_bottom = y - GAP_V

    frames, subs = {}, []
    for k in sorted(SUBPLOTS):
        s, cl = SUBPLOTS[k], COL[k]
        cc, rr = GRID[k]
        fx, fy, fh = grid_x0 + cc * (W + GAP_H), row_y[rr], row_h[rr]
        frames[k] = (fx, fy, W, fh)
        cont = f"s{k}-frame"
        g = [f'<g id="subplot-{k}" inkscape:label="{escape(s["name"])}">',
             doc.rect(cont, fx, fy, W, fh, FRAME.format(c=cl), rx=1.6, label="frame")]
        ox = fx + PAD + (max(width(t["input"][0], MINI.fs, HAIR) for t in SUBPLOTS.values()) + 0.6)
        oy = fy + TOP + NAME_EXTRA + MINI.dy + 0.55 * MINI.fs
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
        g.append(number_tag(doc, k, fx, fy, "filled"))
        # name: right of the badge (badge spans fx-1.2 .. fx+2.4), inside the frame
        g.append(doc.text(fx + TAG - 1.2 + 1.0, fy + 2.3, NAMES[k], NAME_FS, cl, vcenter=True,
                          family=BOLD, weight="bold", label="name", container=cont, idbase=f"s{k}-name"))
        g.append("</g>")
        subs.append("\n".join(g))

    incl = [link(doc, sub, sup, frames) for sub, sup in LINKS]
    leg_svg, leg_w = legend_row(doc, grid_bottom + 5.0)
    page_h = grid_bottom + 5.0 + 1.5 + MARGIN

    svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
     width="{f1(PAGE_W)}mm" height="{f1(page_h)}mm" viewBox="0 0 {f1(PAGE_W)} {f1(page_h)}" version="1.1">
<title>Parameter-space symmetries, left panel</title>
<sodipodi:namedview id="namedview" pagecolor="#ffffff" inkscape:document-units="mm" units="mm"/>
<defs>
{chr(10).join(doc.markers.values())}
</defs>
<g id="layer-setup" inkscape:groupmode="layer" inkscape:label="Setup">
{panel_label}
<g id="setup-network" inkscape:label="network N">
{setup_svg}
</g>
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
    return svg, doc, page_h, setup_fs, leg_w


if __name__ == "__main__":
    out = sys.argv[1]
    svg, doc, ph, sfs, lw = build()
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(svg)
    issues = validate(out, doc)
    from make_left_variants import inkscape
    for ln in inkscape(out, "--query-all").splitlines():
        p = ln.split(",")
        if len(p) == 5 and p[0] in doc.texts:
            x, y, w, h = (float(v) * 25.4 / 96 for v in p[1:])
            if x < 1.0 or y < 1.0 or x + w > PAGE_W - 1.0 or y + h > ph - 1.0:
                issues.append(f"{p[0]} within 1 mm of the page edge")
    print(f"{out}: {PAGE_W} x {ph:.1f} mm | frame W={W:.1f} gap_h={GAP_H:.1f} | setup text {sfs / PT:.1f} pt "
          f"| legend {lw:.1f} mm | {len(issues)} issue(s)")
    for i in issues:
        print("   ", i)
