"""Practical guide: when and how to reason with a symmetry (sec. Discussion, Conclusions) -- 2 design variants.

The taxonomy (tab:taxonomy) turned into a procedure, one step per axis:
  1 Entry         how the symmetry arrives: given / assumed / suspected     (A priori knowledge)
  2 Locate        decision tree whose leaves are the loci of fig:sym-loci   (Object)
  3 Characterize  can we write (G, rho_A, rho_B)? what is off? properties    (Exactness, State)
  4 Act           discover, explain | neutralize, exploit                   (Purpose)
  5 Diagnose      feedback, outside the progression: cues that something is off, back to step 1
Explicitness is left out. Leaves of the Locate tree keep the Okabe-Ito colours of fig:sym-loci.
Section tags (post-its) are read from ../../../main.aux, so re-running after a recompilation renumbers them.

Variant A: stacked bands with a numbered spine 1 -> 4, Diagnose band at the bottom (dashed, outside the flow),
           return arrow up the right margin into the Entry band.
Variant B: same bands with step titles on top (full-width content), Diagnose drawn as a backward arrow at the top
           of the figure, fed by a return arrow from Act up the right margin, pointing back down into Entry.

Units: 1 user unit = 1 mm, W = 184 mm (full page width: include inside adjustwidth, as fig:selection-flow).
Text and formulas use the LaTeX-subset engine of ../five_routes/make_variants.py (TeX Gyre Pagella, mathpazo).
Usage: python3 make_variants.py OUTDIR        (writes symmetry-guide_variant_{A,B}.svg and .png previews)
       python3 make_variants.py --final A|B   (writes survey/images/symmetry-guide.{svg,pdf})
Re-running --final overwrites symmetry-guide.svg / .pdf, including Inkscape edits made to them.
"""
import importlib.util
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.normpath(os.path.join(HERE, "..", ".."))
AUX = os.path.normpath(os.path.join(IMG, "..", "main.aux"))

_spec = importlib.util.spec_from_file_location("five_routes", os.path.join(HERE, "..", "five_routes", "make_variants.py"))
fr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fr)
fr.SYMS.update({"ast": ("∗", "ord"), "subsetneq": ("⊊", "rel"), "neq": ("≠", "rel"), "colon": (":", "punct")})

W = 184.0
FS_STEP, FS_TXT, FS_ANN, FS_SMALL, FS_TAG = 3.2, 2.8, 2.47, 2.3, 2.1  # 9, 8, 7, 6.5, 6 pt

INK, GREY, MID = "#222222", "#555555", "#777777"
EDGE = "#666666"
NAVY = "#2F4A6D"                        # step colour (the "Object" highlight of fig:sym-loci)
BAND_FILL, BAND_STROKE = "#FAF9F6", "#D6D3CC"  # warm grey, as the axis chips of fig:sym-loci
NODE_STROKE = "#B9B4AA"
BAR_FILL = "#ECE9E2"
TAG_PAD = 2.2
TAG_FILL, TAG_STROKE, TAG_FOLD, TAG_INK = "#FBF1AE", "#DCC659", "#E9D77C", "#4F4500"
LOCUS = {"Problem": "#0072b2", "Model": "#009e73", "Optimization": "#e69f00", "Parameter": "#d55e00",
         "Data": "#cc79a7", "Framework": "#777777"}


# ================================================================== section numbers (post-it tags)
def aux_numbers(path=AUX):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return {m.group(1): m.group(2) for m in re.finditer(r"\\newlabel\{([^}@]+)\}\{\{([^}]*)\}", fh.read())}


NUM = aux_numbers()


def ref(key):
    if ".." in key:  # range of consecutive sections, e.g. sec:groups..sec:lie-algebra -> §3.2–3.5
        a, b = key.split("..")
        return f"§{NUM.get(a, '??')}–{NUM.get(b, '??')}"
    n = NUM.get(key, "??")
    if key.startswith("fig:"):
        return f"Fig. {n}"
    if key.startswith("tab:"):
        return f"Tab. {n}"
    return f"§{n}"


# ================================================================== text helpers
def S(s, font="rm"):
    """'text $math$ text' -> source of the LaTeX-subset engine (text parts in \\text, \\textit or \\textbf)."""
    cmd = {"rm": r"\text", "it": r"\textit", "bf": r"\textbf"}[font]
    out = []
    for i, p in enumerate(s.split("$")):
        if i % 2:
            out.append(p)
        elif p:
            out.append(cmd + "{" + p.replace(" ", "~") + "}")
    return "".join(out)


def bx(s, size=FS_TXT, font="rm"):
    return fr.tex(S(s, font), size)


def tw(s, size=FS_TXT, font="rm"):
    return bx(s, size, font).w


def put(doc, L, gid, s, x, y, size=FS_TXT, font="rm", anchor="start", color=INK, container=None):
    L.append(fr.math_svg(doc, gid, bx(s, size, font), x, y, anchor, color, container))


def wrap(s, width, size, font="rm"):
    """Greedy wrap on spaces outside $...$ (formulas are never broken)."""
    words, cur, inmath = [], "", False
    for ch in s:
        if ch == "$":
            inmath = not inmath
        if ch == " " and not inmath:
            words.append(cur)
            cur = ""
        else:
            cur += ch
    words.append(cur)
    lines, line = [], ""
    for w_ in words:
        cand = (line + " " + w_).strip()
        if line and tw(cand, size, font) > width:
            lines.append(line)
            line = w_
        else:
            line = cand
    return lines + [line]


# ================================================================== drawing primitives
def f2(v):
    return f"{v:.2f}"


def rect(doc, L, gid, x, y, w, h, stroke=NODE_STROKE, fill="#ffffff", sw=0.3, rx=1.2, dash=None, frame=True):
    """gid must already be unique (doc.uid)."""
    if frame:
        doc.frames[gid] = (x, y, w, h)
    d = f";stroke-dasharray:{dash}" if dash else ""
    L.append(f'<rect id="{gid}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}" '
             f'style="fill:{fill};stroke:{stroke};stroke-width:{sw}{d}"/>')
    return gid


def node(doc, L, gid, cx, y, w, h, lines, stroke=NODE_STROKE, fill="#ffffff", sw=0.3, dash=None, rx=1.2):
    """Rounded box centred on cx; lines = [(text, size, font, colour)], centred with an equal pitch."""
    gid = doc.uid(gid)
    rect(doc, L, gid, cx - w / 2, y, w, h, stroke, fill, sw, rx, dash)
    pitch = 1.25 * max(l[1] for l in lines)
    n = len(lines)
    for i, (s, size, font, col) in enumerate(lines):
        by = y + h / 2 + (i - (n - 1) / 2) * pitch + 0.33 * size
        put(doc, L, f"{gid}-l{i}", s, cx, by, size, font, "middle", col, container=gid)
    return gid


def node_w(lines, pad=2.4):
    return max(tw(s, size, font) for s, size, font, _ in lines) + 2 * pad


def line(doc, L, pts, color=EDGE, sw=0.3, dash=None, head=True, r=1.0, register=True):
    """Polyline with rounded corners (quadratic) and an arrowhead at the last point."""
    if register:
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            doc.segments.append((x1, y1, x2, y2))
    pts = [list(p) for p in pts]
    if head:  # shorten the last leg so the stroke stops inside the head
        (xa, ya), (xb, yb) = pts[-2], pts[-1]
        d = ((xb - xa) ** 2 + (yb - ya) ** 2) ** 0.5
        ux, uy = (xb - xa) / d, (yb - ya) / d
        tip = (xb, yb)
        pts[-1] = [xb - 1.0 * ux, yb - 1.0 * uy]
    d = f"M {f2(pts[0][0])},{f2(pts[0][1])}"
    for i in range(1, len(pts) - 1):
        (x0, y0), (x1, y1), (x2, y2) = pts[i - 1], pts[i], pts[i + 1]
        l1 = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
        l2 = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        rr = min(r, l1 / 2, l2 / 2)
        ax, ay = x1 - (x1 - x0) / l1 * rr, y1 - (y1 - y0) / l1 * rr
        bx_, by_ = x1 + (x2 - x1) / l2 * rr, y1 + (y2 - y1) / l2 * rr
        d += f" L {f2(ax)},{f2(ay)} Q {f2(x1)},{f2(y1)} {f2(bx_)},{f2(by_)}"
    d += f" L {f2(pts[-1][0])},{f2(pts[-1][1])}"
    da = f";stroke-dasharray:{dash}" if dash else ""
    out = f'<path d="{d}" style="fill:none;stroke:{color};stroke-width:{sw}{da}"/>'
    if head:
        out += fr.head(tip[0], tip[1], ux, uy, color, L=1.25, Wd=1.0)
    L.append(f'<g id="{doc.uid("edge")}">{out}</g>')


def fan(doc, L, px, py, bus, kids, color=EDGE):
    """Tree edges: parent bottom (px, py) -> bus -> each kid (cx, top, label, side, label_y or None)."""
    for cx, top, lab, side, ly in kids:
        if abs(cx - px) < 0.05:
            line(doc, L, [(px, py), (cx, top)], color)
        else:
            line(doc, L, [(px, py), (px, bus), (cx, bus), (cx, top)], color)
        if lab:
            y = ly if ly is not None else (bus + top) / 2 + 0.8
            x, anc = (cx - 0.9, "end") if side == "L" else (cx + 0.9, "start")
            put(doc, L, "edge-label", lab, x, y, FS_ANN, "it", anc, EDGE)


def tags(doc, L, keys, x_right, y_mid, angle=-2.5):
    """Post-it tags, laid right to left so the last one ends at x_right, centred on y_mid."""
    x = x_right
    for key in reversed(keys):
        s = key if not (":" in key) else ref(key)
        w, h = tw(s, FS_TAG) + TAG_PAD, 3.2
        x0 = x - w
        gid = doc.uid("tag")
        cx, cy = x0 + w / 2, y_mid
        fold = 0.9
        body = (f'<path d="M {f2(x0)},{f2(cy - h / 2)} H {f2(x0 + w - fold)} L {f2(x0 + w)},{f2(cy - h / 2 + fold)} '
                f'V {f2(cy + h / 2)} H {f2(x0)} Z" style="fill:{TAG_FILL};stroke:{TAG_STROKE};stroke-width:0.15"/>'
                f'<path d="M {f2(x0 + w - fold)},{f2(cy - h / 2)} V {f2(cy - h / 2 + fold)} H {f2(x0 + w)} Z" '
                f'style="fill:{TAG_FOLD};stroke:{TAG_STROKE};stroke-width:0.15;stroke-linejoin:round"/>')
        doc.frames[gid] = (x0, cy - h / 2, w, h)
        t = fr.math_svg(doc, f"{gid}-t", bx(s, FS_TAG), cx, cy + 0.33 * FS_TAG + 0.05, "middle", TAG_INK, gid)
        L.append(f'<g id="{gid}" transform="rotate({angle} {f2(cx)} {f2(cy)})">{body}{t}</g>')
        x = x0 - 0.8
    return x


def chip(doc, L, s, x, y, size=FS_SMALL, font="it", color=GREY, fill="#ffffff", stroke=BAND_STROKE):
    """Small rounded label (taxonomy axis), top-left at (x, y); returns its width."""
    w = tw(s, size, font) + 2.0
    gid = doc.uid("axis-chip")
    rect(doc, L, gid, x, y, w, 3.5, stroke, fill, 0.25, 1.0)
    put(doc, L, f"{gid}-t", s, x + 1.0, y + 1.75 + 0.33 * size, size, font, "start", color, gid)
    return w


def badge(doc, L, cx, cy, n, filled=True, r=2.4):
    gid = doc.uid(f"badge-{n}")
    fill, col = (NAVY, "#ffffff") if filled else ("#ffffff", NAVY)
    doc.frames[gid] = (cx - r, cy - r, 2 * r, 2 * r)
    b = bx(str(n), 2.7, "bf")
    t = fr.math_svg(doc, f"{gid}-n", b, cx, cy + 0.34 * 2.7 + 0.05, "middle", col, gid)
    L.append(f'<g id="{gid}"><circle cx="{f2(cx)}" cy="{f2(cy)}" r="{f2(r)}" '
             f'style="fill:{fill};stroke:{NAVY};stroke-width:0.4"/>{t}</g>')


def cycle_icon(L, cx, cy, r=1.25, color=NAVY):
    """Open circular arrow (repeat)."""
    import math
    a0, a1 = math.radians(-60), math.radians(240)
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    ux, uy = -math.sin(a1), math.cos(a1)  # tangent (clockwise in screen coords)
    L.append(f'<g><path d="M {f2(x0)},{f2(y0)} A {f2(r)},{f2(r)} 0 1 1 {f2(x1)},{f2(y1)}" '
             f'style="fill:none;stroke:{color};stroke-width:0.35"/>'
             f'{fr.head(x1 + 0.45 * ux, y1 + 0.45 * uy, ux, uy, color, L=0.9, Wd=0.9)}</g>')


# ================================================================== content
ENTRY = [("Given", "by the problem or a paper", None, None),
         ("Assumed", "candidate, validity unchecked", "1.2,0.6", ["sec:sym-quantification"]),
         ("Suspected", "unknown, at least partially", "0.35,0.6", ["sec:sym-disco"])]

# leaves of the Locate tree: (id, label, locus, text font size)
LEAVES = [("fstar", r"$f^{\ast}$", "Problem"), ("p", "$p$", "Problem"), ("x", r"$g\cdot x=x$", "Data"),
          ("H", r"$\mathcal{H}$", "Model"), ("phi", r"$\varphi$", "Model"),
          ("U", "$U$", "Optimization"), ("L", r"$\mathcal{L}$", "Optimization"),
          ("ftheta", r"$f_\theta$", "Parameter"), ("theta", r"$g\cdot\theta=\theta$", "Parameter"),
          ("fw", "Framework", "Framework")]
LOCUS_TAGS = {"Problem": ["sec:sym-disc-from-data"], "Data": ["par:curie-principle"],
              "Model": ["sec:gdl", "sec:hierarchy-param-space-symmetries"],
              "Optimization": ["sec:symmetry-optimization"],
              "Parameter": ["sec:data-augmentation", "sec:learning-dynamics"],
              "Framework": ["sec:framework-symmetries"]}

OFF = [("domain restriction", r"conditions on $\theta$ or $x$", ["sec:domain-restriction"]),
       ("not a group", "subset of $G$, weaker structure", ["sec:extent-restriction"]),
       ("up to a tolerance", r"approximate, $\epsilon>0$", ["sec:approx-tolerance"])]
PROPS = [("Group", "$G$ finite · discrete infinite · continuous;  compact;  connected"),
         ("Action", r"invariant ($\rho_B$ trivial) · equivariant ($\rho_A=\rho_B$, or $\rho_A\neq\rho_B$) · linear"),
         ("Time", "static · dynamic")]

ACT = [("Discover / describe", ["find $G$ (discovery)", "formalize an observation", "reframe a subfield",
                                "unify previous works"], ["sec:sym-disco", "sec:framework-symmetries"]),
       ("Explain / understand", ["conservation laws", "training dynamics", r"fibers of $\varphi$"],
        ["sec:descr-param-space-symmetries"]),
       ("Neutralize", ["remove", "quotient", "align, canonicalize"], ["sec:quotient-repr-align"]),
       ("Exploit", ["equivariant layers", "data augmentation", "soft penalty", "teleportation, pruning"],
        ["sec:design-principle", "sec:exploit-symmetry-feature"])]

CUES = [("Functional SB", r"equivariant model cannot fit the train set; Curie: "
                          r"$\operatorname{Stab}(f^{\ast}(x))\subsetneq\operatorname{Stab}(x)$", ["sec:functional-sb"], False),
        ("Distributional SB", "a two-sample test tells $p$ from its symmetrized version", ["sec:distributional-sb"], False),
        ("Dynamical SB", "a conserved quantity drifts in practice", ["sec:dynamical-sb"], False),
        ("Equivariance error", "large, or discovery disagrees with the assumed $G$", ["sec:sym-quantification"], False),
        ("Weak signal", "equivariant model loses to an unconstrained one (inconclusive)", ["sec:edl-tradeoffs"], True)]


# ================================================================== bands (content builders, top y, x range)
def entry_content(doc, L, yb, X0, X1, x_free=18.0):
    """Three chips; the right x_free mm stay free for the return arrow. Returns (height, (x, y) of the target)."""
    gap = 5.0
    cw = min(44.0, (X1 - X0 - x_free - 2 * gap) / 3)
    y, h = yb + 3.0, 8.5
    target = None
    for i, (name, desc, dash, keys) in enumerate(ENTRY):
        x = X0 + i * (cw + gap)
        g = node(doc, L, f"entry-{name.lower()}", x + cw / 2, y, cw, h,
                 [(name, FS_TXT, "bf", INK), (desc, FS_ANN, "it", GREY)],
                 stroke=NAVY if dash is None else "#7F8EA3", sw=0.35, dash=dash)
        if keys:
            tags(doc, L, keys, x + cw - 1.0, y)
        target = (x + cw, y + h / 2)
    return h + 6.0, target


def locate_content(doc, L, yb, X0, X1):
    """Decision tree of the Locate step; the leaves are the loci of fig:sym-loci. Returns the height."""
    # leaf centres: fixed pitches (mm) between consecutive leaves, then scaled to fill [X0, X1]
    pitch = [15.5, 17.0, 15.5, 13.0, 13.5, 13.0, 14.0, 14.0, 18.5]
    lw = [tw(lab, FS_TXT, "rm") + 4.2 for _, lab, _ in LEAVES]
    lw = [max(w_, 8.0) for w_ in lw]
    span = sum(pitch)
    s = (X1 - X0 - lw[0] / 2 - lw[-1] / 2 - 1.0) / span
    xs = [X0 + 0.5 + lw[0] / 2]
    for p_ in pitch:
        xs.append(xs[-1] + p_ * s)
    cx = dict(zip([k for k, _, _ in LEAVES], xs))

    h = 5.5
    y0, y1, y2, y3 = yb + 3.0, yb + 14.5, yb + 26.0, yb + 37.5  # rows: root, level 1, level 2, leaves
    b1, b2, b3 = y0 + h + 2.0, y1 + h + 2.0, y2 + h + 2.0          # buses
    hl = 6.0

    def q(gid, x, y, s_):
        lines = [(s_, FS_ANN, "rm", INK)]
        return node(doc, L, gid, x, y, node_w(lines, 2.0), h, lines)

    c_sx = (cx["fstar"] + cx["p"]) / 2
    c_single = (c_sx + cx["x"]) / 2
    c_arch, c_rule, c_par = (cx["H"] + cx["phi"]) / 2, (cx["U"] + cx["L"]) / 2, (cx["ftheta"] + cx["theta"]) / 2
    c_fixed = c_rule
    c_root = c_fixed
    q("q-model", c_root, y0, "Model?")
    q("q-single-x", c_single, y1, "Single $x$?")
    q("q-fixed", c_fixed, y1, "What is fixed?")
    q("q-funct-stat", c_sx, y2, "Functional or statistical?")
    q("q-arch-acts", c_arch, y2, "$g$ acts on?")
    q("q-update", c_rule, y2, "Needs an update?")
    q("q-par-acts", c_par, y2, "$g$ acts on?")

    fan(doc, L, c_root, y0 + h, b1, [(c_single, y1, "no model", "L", None),
                                     (c_fixed, y1, "model", "R", None),
                                     (cx["fw"], y3, "beyond model", "L", (b1 + y1) / 2 + 0.8)])
    fan(doc, L, c_single, y1 + h, b2, [(c_sx, y2, "no", "L", None), (cx["x"], y3, "yes", "L", (b2 + y2) / 2 + 0.8)])
    fan(doc, L, c_fixed, y1 + h, b2, [(c_arch, y2, "architecture", "L", None), (c_rule, y2, "learning rule", "R", None),
                                      (c_par, y2, "parameter", "R", None)])
    fan(doc, L, c_sx, y2 + h, b3, [(cx["fstar"], y3, "functional", "R", None), (cx["p"], y3, "statistical", "R", None)])
    fan(doc, L, c_arch, y2 + h, b3, [(cx["H"], y3, "$x$", "L", None), (cx["phi"], y3, r"$\theta$", "R", None)])
    fan(doc, L, c_rule, y2 + h, b3, [(cx["U"], y3, "yes", "L", None), (cx["L"], y3, "no", "R", None)])
    fan(doc, L, c_par, y2 + h, b3, [(cx["ftheta"], y3, "$x$", "L", None), (cx["theta"], y3, r"$\theta$", "R", None)])

    for (k, lab, loc), w_ in zip(LEAVES, lw):
        node(doc, L, f"leaf-{k}", cx[k], y3, w_, hl, [(lab, FS_TXT, "rm", INK)], stroke=LOCUS[loc], sw=0.5)

    # locus names under the leaves (coloured rule spanning the group) and their post-its
    yr, yn = y3 + hl + 1.6, y3 + hl + 5.0
    groups = {}
    for (k, _, loc), w_ in zip(LEAVES, lw):
        a, b = groups.get(loc, (1e9, -1e9))
        groups[loc] = (min(a, cx[k] - w_ / 2), max(b, cx[k] + w_ / 2))
    for loc, (a, b) in groups.items():
        L.append(f'<path d="M {f2(a + 0.4)},{f2(yr)} H {f2(b - 0.4)}" '
                 f'style="fill:none;stroke:{LOCUS[loc]};stroke-width:0.6;stroke-linecap:round"/>')
        m = (a + b) / 2
        wn = tw(loc, FS_ANN, "bf")
        keys = LOCUS_TAGS[loc]
        wt = sum(tw(ref(k_), FS_TAG) + TAG_PAD for k_ in keys) + 0.8 * (len(keys) - 1)
        put(doc, L, f"locus-{loc.lower()}", loc, m, yn, FS_ANN, "bf", "middle", LOCUS[loc])
        tags(doc, L, keys, m + wt / 2, yn + 3.3, angle=0)
    return yn + 6.0 - yb


def characterize_content(doc, L, yb, X0, X1, back_to_y):
    """Characterization tree. back_to_y: bottom of the Locate band (target of the 'hard case' arrow)."""
    h = 6.0
    root_lines = [(r"Can you write $(G,\rho_A,\rho_B)$?", FS_TXT, "rm", INK)]
    wr = node_w(root_lines, 2.6)
    xr = X0 + 1.0
    c_root = xr + wr / 2
    y0 = yb + 3.0
    node(doc, L, "q-write", c_root, y0, wr, h, root_lines, stroke=NAVY, sw=0.4)

    # "not exactly" branch: three children spread from the 'yes' drop to the right
    yes_x = xr + 4.5
    yw = yb + 15.5
    yk, hk = yb + 27.0, 9.0
    kw = max(node_w([(a, FS_ANN, "rm", INK), (b, FS_ANN, "it", GREY)], 2.0) for a, b, _ in OFF)
    gapk = 4.0
    ks = [yes_x + 10.0 + kw / 2 + i * (kw + gapk) for i in range(3)]
    c_wio = ks[1]
    wio_lines = [("What is off?", FS_ANN, "rm", INK)]
    w_wio = node_w(wio_lines, 2.0)
    node(doc, L, "q-what-off", c_wio, yw, w_wio, 5.5, wio_lines)
    for (a, b, keys), k in zip(OFF, ks):
        node(doc, L, f"off-{a.split()[0]}", k, yk, kw, hk, [(a, FS_ANN, "rm", INK), (b, FS_ANN, "it", GREY)])
        tags(doc, L, keys, k + kw / 2 - 1.0, yk)
    fan(doc, L, c_wio, yw + 5.5, yk - 2.6, [(k, yk, None, "R", None) for k in ks])

    # "no" branch: on the right, Discovery above, hard case below, then back to Locate
    dl = [("Discovery", FS_TXT, "bf", INK), ("$G$ unknown", FS_ANN, "it", GREY)]
    hl = [("Hard case", FS_TXT, "bf", INK), ("complex or latent $G$", FS_ANN, "it", GREY)]
    wdh = max(node_w(dl), node_w(hl))
    hh = 7.5
    xb = X1 - 3.0                 # riser of the dashed 'back to Locate' arrow
    xd = xb - 20.0 - wdh          # left edge of the two boxes
    xs = xd - 8.0                 # split of the 'no' edge
    assert xs > c_wio + w_wio / 2 + 2.5, "no-branch split collides with 'What is off?'"
    yd, yh = y0 + h / 2 - hh / 2, y0 + h / 2 - hh / 2 + hh + 3.0
    node(doc, L, "out-discovery", xd + wdh / 2, yd, wdh, hh, dl)
    tags(doc, L, ["sec:sym-disco"], xd + wdh - 1.0, yd)
    node(doc, L, "out-hard", xd + wdh / 2, yh, wdh, hh, hl, dash="1.2,0.6")
    ymid = y0 + h / 2
    line(doc, L, [(xr + wr, ymid), (xd, ymid)])
    line(doc, L, [(xs, ymid), (xs, yh + hh / 2), (xd, yh + hh / 2)])
    put(doc, L, "edge-label", "no", (xr + wr + xs) / 2, ymid - 1.0, FS_ANN, "it", "middle", EDGE)
    line(doc, L, [(xd + wdh, yh + hh / 2), (xb, yh + hh / 2), (xb, back_to_y)], color=NAVY, dash="1.2,0.7")
    put(doc, L, "back-label", "back to Locate", (xd + wdh + xb) / 2, yh + hh / 2 - 1.1, FS_ANN, "it", "middle",
        NAVY)

    # properties (output of the step)
    yp, hp = yk + hk + 6.0, 16.0
    lead = max(tw(a + ":", FS_ANN, "bf") for a, _ in PROPS)
    xp = xr
    wp = max(lead + 1.6 + max(tw(b, FS_ANN) for _, b in PROPS) + 5.0, ks[2] + kw / 2 - xp)
    gp = doc.uid("properties")
    rect(doc, L, gp, xp, yp, wp, hp, NAVY, "#ffffff", 0.4, 1.2)
    for i, (a, b) in enumerate(PROPS):
        by = yp + 3.9 + i * 3.35
        put(doc, L, f"{gp}-k{i}", a + ":", xp + 2.5, by, FS_ANN, "bf", "start", INK, gp)
        put(doc, L, f"{gp}-v{i}", b, xp + 2.5 + lead + 1.6, by, FS_ANN, "rm", "start", INK, gp)
    tags(doc, L, ["sec:groups..sec:lie-algebra"], xp + wp - 1.0, yp)

    # edges root -> yes / not exactly
    fan(doc, L, c_root, y0 + h, y0 + h + 2.5, [(yes_x, yp, "yes", "R", y0 + h + 5.2),
                                                (c_wio, yw, "not exactly", "L", None)])
    for k in ks:
        line(doc, L, [(k, yk + hk), (k, yp)])

    # the characterization sets the available tools
    by = yp + 3.9 + len(PROPS) * 3.35
    s_tools = "→ determines the available tools"
    put(doc, L, f"{gp}-tools", s_tools, xp + 2.5, by, FS_ANN, "it", "start", GREY, gp)
    wt_ = sum(tw(ref(k_), FS_TAG) + TAG_PAD for k_ in ["sec:edl-achieving-equiv", "sec:lie-algebra"]) + 0.8
    tags(doc, L, ["sec:edl-achieving-equiv", "sec:lie-algebra"], xp + 2.5 + tw(s_tools, FS_ANN, "it") + 1.5 + wt_,
         by - 0.75, angle=0)
    return yp + hp + 3.0 - yb


def act_content(doc, L, yb, X0, X1, bar_x0=None, bar_y=None):
    """Purpose bars (descriptive | prescriptive) over four cards. bar_x0/bar_y: put the bars beside a header."""
    gap = 3.0
    cw = (X1 - X0 - 3 * gap) / 4
    ybar, hb = (yb + 3.0 if bar_y is None else bar_y), 3.6
    for j, lab in enumerate(["descriptive", "prescriptive"]):
        x = X0 + j * 2 * (cw + gap)
        w_ = 2 * cw + gap
        if j == 0 and bar_x0 is not None and bar_x0 > x:
            x, w_ = bar_x0, w_ - (bar_x0 - x)
        gid = doc.uid(f"purpose-{lab}")
        rect(doc, L, gid, x, ybar, w_, hb, "none", BAR_FILL, 0, 1.0)
        put(doc, L, f"{gid}-t", lab, x + w_ / 2, ybar + hb / 2 + 0.33 * FS_ANN, FS_ANN, "it", "middle", GREY, gid)
    yc = max(ybar + hb, yb) + 2.6
    n_max = max(len(items) for _, items, _ in ACT)
    hc = 5.6 + n_max * 3.2 + 1.2
    for i, (title, items, keys) in enumerate(ACT):
        x = X0 + i * (cw + gap)
        gid = doc.uid(f"act-{title.split()[0].lower()}")
        rect(doc, L, gid, x, yc, cw, hc, NODE_STROKE, "#ffffff", 0.3, 1.2)
        put(doc, L, f"{gid}-title", title, x + 2.2, yc + 4.4, FS_TXT, "bf", "start", INK, gid)
        for j, it in enumerate(items):
            put(doc, L, f"{gid}-i{j}", "– " + it, x + 2.2, yc + 8.2 + j * 3.2, FS_ANN, "rm", "start", INK, gid)
        tags(doc, L, keys, x + cw - 1.0, yc)
    return yc + hc + 3.0 - yb


def diagnose_cards(doc, L, yb, X0, X1, cols=5):
    """Cue cards (title, wrapped text, post-it). Returns the height used."""
    gap = 2.5
    cw = (X1 - X0 - (cols - 1) * gap) / cols
    wrapped = [wrap(t, cw - 3.6, FS_SMALL) for _, t, _, _ in CUES]
    rows = (len(CUES) + cols - 1) // cols
    n_max = max(len(w_) for w_ in wrapped)
    hc = 5.2 + n_max * 2.9 + 1.0
    for i, ((title, _, keys, weak), lines) in enumerate(zip(CUES, wrapped)):
        r_, c_ = divmod(i, cols)
        x, y = X0 + c_ * (cw + gap), yb + 3.0 + r_ * (hc + 3.5)
        gid = doc.uid("cue-" + title.split()[0].lower())
        rect(doc, L, gid, x, y, cw, hc, NODE_STROKE, "#ffffff", 0.3, 1.2, "1.0,0.6" if weak else None)
        put(doc, L, f"{gid}-title", title, x + 1.8, y + 4.0, FS_ANN, "bf", "start", INK if not weak else GREY, gid)
        for j, ln in enumerate(lines):
            put(doc, L, f"{gid}-l{j}", ln, x + 1.8, y + 7.4 + j * 2.9, FS_SMALL, "rm", "start", GREY, gid)
        tags(doc, L, keys, x + cw - 1.0, y)
    return 3.0 + rows * hc + (rows - 1) * 3.5 + 3.0


# ================================================================== headers
STEPS = {1: ("Entry", ["A priori knowledge"], None),
         2: ("Locate", ["Object"], r"$f\colon\;A\to B$"),
         3: ("Characterize", ["Exactness", "State"], r"$(G,\rho_A,\rho_B)$"),
         4: ("Act", ["Purpose"], None),
         5: ("Diagnose", [], None)}


def side_header(doc, L, n, yb, x_badge=5.0, x_text=9.0, extra=None):
    """Left header of variant A: badge, step name, taxonomy axis chips, output."""
    name, axes, out = STEPS[n]
    badge(doc, L, x_badge, yb + 5.0, n, filled=(n != 5))
    put(doc, L, f"step-{n}-name", name, x_text, yb + 6.1, FS_STEP, "bf", "start", NAVY)
    y = yb + 8.6
    for a in axes:
        chip(doc, L, a, x_text, y)
        y += 4.3
    if out:
        put(doc, L, f"step-{n}-out-k", "output", x_text, y + 2.6, FS_SMALL, "it", "start", GREY)
        put(doc, L, f"step-{n}-out", out, x_text, y + 6.0, FS_ANN, "rm", "start", INK)
        y += 7.5
    if extra == "repeat":
        cycle_icon(L, x_text + 1.3, y + 1.8)
        put(doc, L, f"step-{n}-repeat", "repeat per locus", x_text + 3.4, y + 2.6, FS_SMALL, "it", "start", NAVY)
        tags(doc, L, ["fig:sym-loci"], x_text + tw(ref("fig:sym-loci"), FS_TAG) + TAG_PAD, y + 6.4, angle=0)
    if n == 5:
        put(doc, L, f"step-{n}-hint", "feedback, outside", x_text, y + 1.6, FS_SMALL, "it", "start", GREY)
        put(doc, L, f"step-{n}-hint2", "the progression", x_text, y + 4.4, FS_SMALL, "it", "start", GREY)


def top_header(doc, L, n, yb, x0):
    """Header of variant B: badge, name and axis chips on one line at the top of the band. Returns its height."""
    name, axes, out = STEPS[n]
    badge(doc, L, x0 + 2.6, yb + 4.2, n, filled=(n != 5))
    x = x0 + 6.4
    put(doc, L, f"step-{n}-name", name, x, yb + 5.3, FS_STEP, "bf", "start", NAVY)
    x += tw(name, FS_STEP, "bf") + 2.5
    for a in axes:
        x += chip(doc, L, a, x, yb + 2.4) + 1.2
    if out:
        x += 1.5
        put(doc, L, f"step-{n}-out", "→ " + out, x, yb + 5.3, FS_ANN, "rm", "start", INK)
        x += tw("→ " + out, FS_ANN) + 2.0
    return x


# ================================================================== variants
BAND_X0, BAND_X1 = 1.0, 176.5   # bands; the return channel runs at x = CH
CH = 180.5
GAP = 4.0


def band(doc, L, gid, yb, h, dash=None):
    rect(doc, L, gid, BAND_X0, yb, BAND_X1 - BAND_X0, h, BAND_STROKE if not dash else NAVY, BAND_FILL,
         0.3 if not dash else 0.35, 2.0, dash, frame=False)


def variant_A():
    doc = fr.Doc()
    Lb = doc.layer("bands", "Bands")
    Lc = doc.layer("content", "Content")
    Lh = doc.layer("headers", "Step headers")
    La = doc.layer("flow", "Flow arrows")
    X0, X1 = 31.0, 174.5
    y = 1.0
    tops = {}
    # 1 Entry
    tops[1] = y
    h1, target = entry_content(doc, Lc, y, X0, X1)
    band(doc, Lb, "band-entry", y, h1)
    side_header(doc, Lh, 1, y)
    y += h1 + GAP
    # 2 Locate
    tops[2] = y
    h2 = locate_content(doc, Lc, y, X0, X1)
    h2 = max(h2, 36.0)
    band(doc, Lb, "band-locate", y, h2)
    side_header(doc, Lh, 2, y, extra="repeat")
    y_loc_bottom = y + h2
    y += h2 + GAP
    # 3 Characterize
    tops[3] = y
    h3 = characterize_content(doc, Lc, y, X0, X1, y_loc_bottom)
    band(doc, Lb, "band-characterize", y, h3)
    side_header(doc, Lh, 3, y)
    y += h3 + GAP
    # 4 Act
    tops[4] = y
    h4 = act_content(doc, Lc, y, X0, X1)
    band(doc, Lb, "band-act", y, h4)
    side_header(doc, Lh, 4, y)
    y += h4 + GAP + 1.0
    # 5 Diagnose
    tops[5] = y
    h5 = diagnose_cards(doc, Lc, y, X0, X1)
    band(doc, Lb, "band-diagnose", y, h5, dash="1.4,0.8")
    side_header(doc, Lh, 5, y)
    H = y + h5 + 1.0
    # spine 1 -> 4 (solid), 4 -> 5 (dashed)
    for n in (1, 2, 3, 4):
        line(doc, La, [(5.0, tops[n] + 7.6), (5.0, tops[n + 1] + 2.4)], color=NAVY, sw=0.45,
             dash=None if n < 4 else "1.2,0.7", register=False)
    # return arrow: Diagnose -> right margin -> Entry (to the 'Suspected' chip)
    yd = y + h5 / 2
    line(doc, La, [(BAND_X1, yd), (CH, yd), (CH, target[1]), (target[0] + 0.4, target[1])], color=NAVY, sw=0.45,
         r=2.0)
    put(doc, La, "revise", "revise", (target[0] + BAND_X1) / 2, target[1] - 1.2, FS_ANN, "it", "middle", NAVY)
    return doc, H, "Reasoning with a symmetry: a practical guide (variant A)"


def variant_B():
    """Step titles on top of each band (content uses the full width); Diagnose is a backward arrow at the top."""
    doc = fr.Doc()
    Lb = doc.layer("bands", "Bands")
    Lc = doc.layer("content", "Content")
    Lh = doc.layer("headers", "Step headers")
    La = doc.layer("flow", "Flow arrows")
    X0, X1 = 5.0, 173.5
    y = 1.0
    # 5 Diagnose as a backward (left-pointing) arrow band at the top
    tip = 7.0
    yD = y
    hD = 7.0 + diagnose_cards(doc, Lc, y + 6.0, X0 + tip, X1 - 1.0)
    gid = doc.uid("band-diagnose")
    Lb.append(f'<path id="{gid}" d="M {f2(BAND_X0 + tip)},{f2(yD)} H {f2(BAND_X1)} V {f2(yD + hD)} '
              f'H {f2(BAND_X0 + tip)} L {f2(BAND_X0)},{f2(yD + hD / 2)} Z" '
              f'style="fill:{BAND_FILL};stroke:{NAVY};stroke-width:0.35;stroke-dasharray:1.4,0.8;stroke-linejoin:round"/>')
    xe = top_header(doc, Lh, 5, yD, X0 + tip - 1.0)
    put(doc, Lh, "step-5-hint", "feedback, outside the progression: when a cue fires, go back to Entry", xe + 0.5,
        yD + 5.3, FS_SMALL, "it", "start", GREY)
    y += hD + GAP + 1.0
    tops = {}
    # 1 Entry: header and chips on one row
    tops[1] = y
    xe = top_header(doc, Lh, 1, y + 3.0, X0)
    h1, target = entry_content(doc, Lc, y, xe + 4.0, X1, x_free=0.0)
    band(doc, Lb, "band-entry", y, h1)
    y += h1 + GAP
    # 2 Locate: the tree root sits beside the header
    tops[2] = y
    xe = top_header(doc, Lh, 2, y, X0)
    cycle_icon(Lh, xe + 1.3, y + 4.4)
    put(doc, Lh, "step-2-repeat", "repeat per locus", xe + 3.4, y + 5.3, FS_SMALL, "it", "start", NAVY)
    tags(doc, Lh, ["fig:sym-loci"], xe + 3.4 + tw("repeat per locus", FS_SMALL, "it") + 1.2
         + tw(ref("fig:sym-loci"), FS_TAG) + TAG_PAD, y + 4.4, angle=0)
    h2 = locate_content(doc, Lc, y + 0.5, X0, X1) + 0.5
    band(doc, Lb, "band-locate", y, h2)
    y_loc_bottom = y + h2
    y += h2 + GAP
    # 3 Characterize
    tops[3] = y
    top_header(doc, Lh, 3, y, X0)
    hh = 6.0
    h3 = characterize_content(doc, Lc, y + hh, X0, X1, y_loc_bottom) + hh
    band(doc, Lb, "band-characterize", y, h3)
    y += h3 + GAP
    # 4 Act: purpose bars beside the header
    tops[4] = y
    xe = top_header(doc, Lh, 4, y, X0)
    h4 = act_content(doc, Lc, y + 6.0, X0, X1, bar_x0=xe + 3.0, bar_y=y + 2.4) + 6.0
    band(doc, Lb, "band-act", y, h4)
    H = y + h4 + 1.0
    # progression arrows between bands (at the badges)
    for n in (1, 2, 3):
        y_from = tops[n + 1] - GAP - 0.4 if n > 1 else tops[2] - GAP - 0.4
        line(doc, La, [(X0 + 2.6, y_from), (X0 + 2.6, tops[n + 1] + 1.6)], color=NAVY, sw=0.45, register=False)
    # return: Act -> right margin -> into the Diagnose arrow band (top)
    ya = tops[4] + h4 / 2
    line(doc, La, [(BAND_X1, ya), (CH, ya), (CH, yD + hD / 2), (BAND_X1 + 0.4, yD + hD / 2)], color=NAVY, sw=0.45,
         r=2.0)
    # Diagnose -> Entry: leaves the arrow band on its slanted lower edge, down to the Entry badge
    xf = X0 + 2.6
    yf = yD + hD / 2 + (xf - BAND_X0) / tip * hD / 2
    line(doc, La, [(xf, yf), (xf, tops[1] + 3.0 + 1.6)], color=NAVY, sw=0.45, dash="1.2,0.7", register=False)
    return doc, H, "Reasoning with a symmetry: a practical guide (variant B)"


VARIANTS = {"A": variant_A, "B": variant_B}


# ================================================================== build
def build(name):
    doc, H, title = VARIANTS[name]()
    return fr.svg_doc(doc, W, H, title, bg="#ffffff"), doc, (W, H)


def final(name):
    svg_path = os.path.join(IMG, "symmetry-guide.svg")
    svg, _, _ = build(name)
    with open(svg_path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    subprocess.run(["inkscape", svg_path, "--export-type=pdf", "-o", svg_path[:-4] + ".pdf"], env=fr.INKSCAPE_ENV,
                   capture_output=True, text=True, check=True)
    print(svg_path[:-4] + ".pdf")


def main(argv):
    if argv and argv[0] == "--final":
        return final(argv[1] if len(argv) > 1 else "A")
    outdir = argv[0] if argv else "."
    os.makedirs(outdir, exist_ok=True)
    for name in (argv[1:] or VARIANTS):
        svg, doc, page = build(name)
        path = os.path.join(outdir, f"symmetry-guide_variant_{name}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg)
        issues = fr.validate(path, doc, page)
        subprocess.run(["inkscape", path, "--export-type=png", "--export-dpi=200", "--export-background=#ffffff",
                        "-o", path[:-4] + ".png"], env=fr.INKSCAPE_ENV, capture_output=True, text=True, check=True)
        print(f"[{name}] {path}: {page[0]:.1f} x {page[1]:.1f} mm -- {len(issues)} layout issue(s)")
        for it in issues[:60]:
            print("   ", it)


if __name__ == "__main__":
    main(sys.argv[1:])
