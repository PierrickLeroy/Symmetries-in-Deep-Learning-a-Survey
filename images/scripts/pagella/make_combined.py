"""Merge the two panels of fig:param-space-symmetries side by side, then export the PDF used by main.tex.

Reads the panel SVGs as they are on disk (so Inkscape edits made to either panel are kept), prefixes every id
with "a-" / "b-" to avoid collisions, and wraps each panel in an Inkscape layer "Panel a" / "Panel b".
Usage: python3 make_combined.py   (paths are relative to survey/images)
Re-running overwrites param-space-symmetries.svg / .pdf, including Inkscape edits made to the merged file.
"""
import os
import re
import subprocess
import xml.etree.ElementTree as ET

from make_left_variants import INKSCAPE_ENV

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.normpath(os.path.join(HERE, "..", ".."))
PANELS = [("a", "param-space-symmetries_left.svg"), ("b", "param-space-symmetries_right.svg")]
OUT_SVG = os.path.join(IMG, "param-space-symmetries.svg")
OUT_PDF = os.path.join(IMG, "param-space-symmetries.pdf")

NS = {"svg": "http://www.w3.org/2000/svg", "inkscape": "http://www.inkscape.org/namespaces/inkscape",
      "sodipodi": "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd", "xlink": "http://www.w3.org/1999/xlink"}
for p, u in NS.items():
    ET.register_namespace("" if p == "svg" else p, u)
SVG = "{%s}" % NS["svg"]
INK = "{%s}" % NS["inkscape"]
SKIP = {SVG + "title", SVG + "metadata", "{%s}namedview" % NS["sodipodi"]}


def to_mm(v):
    m = re.fullmatch(r"\s*([\d.]+)\s*(mm|cm|in|pt|px)?\s*", v)
    val, unit = float(m.group(1)), m.group(2) or "px"
    return val * {"mm": 1.0, "cm": 10.0, "in": 25.4, "pt": 25.4 / 72, "px": 25.4 / 96}[unit]


def load(path, prefix):
    root = ET.parse(path).getroot()
    w, h = to_mm(root.get("width")), to_mm(root.get("height"))
    vb = [float(x) for x in root.get("viewBox").replace(",", " ").split()]
    ids = {e.get("id") for e in root.iter() if e.get("id")}

    def ref(m):
        return f"url(#{prefix}{m.group(1)})" if m.group(1) in ids else m.group(0)

    for e in root.iter():
        for k, v in list(e.attrib.items()):
            if k == "id":
                e.set(k, prefix + v)
            elif "url(#" in v:
                e.set(k, re.sub(r"url\(#([^)]+)\)", ref, v))
            elif k.endswith("href") and v.startswith("#") and v[1:] in ids:
                e.set(k, "#" + prefix + v[1:])
    defs = [c for c in root if c.tag == SVG + "defs"]
    body = [c for c in root if c.tag != SVG + "defs" and c.tag not in SKIP]
    return w, h, vb, defs, body


def main():
    panels = [(lab, *load(os.path.join(IMG, f), f"{lab}-")) for lab, f in PANELS]
    W = sum(p[1] for p in panels)
    H = max(p[2] for p in panels)
    root = ET.Element(SVG + "svg", {"width": f"{W:.1f}mm", "height": f"{H:.1f}mm", "viewBox": f"0 0 {W:.1f} {H:.1f}",
                                    "version": "1.1"})
    ET.SubElement(root, SVG + "title").text = "Parameter-space symmetries"
    ET.SubElement(root, "{%s}namedview" % NS["sodipodi"], {"id": "namedview", "pagecolor": "#ffffff",
                                                          INK + "document-units": "mm", "units": "mm"})
    defs = ET.SubElement(root, SVG + "defs", {"id": "defs"})
    x = 0.0
    for lab, w, h, vb, pdefs, body in panels:
        for d in pdefs:
            defs.extend(list(d))
        sx, sy = w / vb[2], h / vb[3]
        tf = f"translate({x:.1f},0)"
        if abs(sx - 1) > 1e-6 or abs(sy - 1) > 1e-6:
            tf += f" scale({sx:.6f},{sy:.6f})"
        if vb[0] or vb[1]:
            tf += f" translate({-vb[0]:.3f},{-vb[1]:.3f})"
        g = ET.SubElement(root, SVG + "g", {"id": f"panel-{lab}", INK + "groupmode": "layer",
                                            INK + "label": f"Panel {lab}", "transform": tf})
        g.extend(body)
        x += w
    ET.ElementTree(root).write(OUT_SVG, encoding="UTF-8", xml_declaration=True)
    subprocess.run(["inkscape", OUT_SVG, "--export-type=pdf", "-o", OUT_PDF], env=INKSCAPE_ENV,
                   capture_output=True, text=True, check=True)
    print(f"{OUT_SVG}: {W:.1f} x {H:.1f} mm\n{OUT_PDF}")


if __name__ == "__main__":
    main()
