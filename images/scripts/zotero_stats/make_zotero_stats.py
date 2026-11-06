"""Corpus statistics figure (fig:corpus-stats): publications per year (left) and sourcing progress (right).

Left:  number of works per publication year; works published in 2010 or earlier share the first bar.
Right: cumulative number of works against the date they were added to the Zotero library, annotated with
       the three phases of the project (initial bulk, passive monitoring, active writing).

Text is typeset by LaTeX with mathpazo, so the fonts match the survey body (Type 1, embedded).
Usage: python3 make_zotero_stats.py                 writes survey/images/zotero_stats.pdf (variant A)
       python3 make_zotero_stats.py --variant B     numbered badges on the curve + key, instead of labels
       python3 make_zotero_stats.py --out X.pdf --csv Y.csv --export-date 2026-11-06
The export date (end of the curve) defaults to the modification time of the CSV.
"""
import argparse
import datetime as dt
import os

import matplotlib

matplotlib.use("pdf")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, *[".."] * 5))  # symmetry-survey/
CSV = os.path.join(ROOT, "zotero.csv")
OUT = os.path.join(ROOT, "claude-code", "survey", "images", "zotero_stats.pdf")

# Project timeline. Works added before PROJECT_START were already in the library: they form the initial bulk.
PROJECT_START = pd.Timestamp("2024-07-01")
PHASE3_START = pd.Timestamp("2026-05-01")  # start of active writing and gap filling
OLD_YEAR = 2010  # works published in or before this year are aggregated in the first bar

MM = 1 / 25.4
W, H = 138 * MM, 52 * MM  # MDPI \textwidth = 138 mm; include with width=\textwidth
INK, GREY, RULE = "#222222", "#555555", "#e4e4e4"
BASE = "#3b9fc9"  # survey blue (Paul Tol), as in param-space-symmetries and exactness-rotation
BAND = "#f1f1ef"  # phase-3 shading
FS_TICK, FS_LAB, FS_ANN = 7, 8, 7  # pt

plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage[T1]{fontenc}\usepackage{mathpazo}",
    "font.family": "serif",
    "font.size": FS_TICK,
    "axes.labelsize": FS_LAB,
    "axes.labelcolor": INK,
    "axes.edgecolor": GREY,
    "axes.linewidth": 0.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.color": GREY,
    "ytick.color": GREY,
    "xtick.labelcolor": INK,
    "ytick.labelcolor": INK,
    "xtick.labelsize": FS_TICK,
    "ytick.labelsize": FS_TICK,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    "xtick.major.size": 2.0,
    "ytick.major.size": 2.0,
    "xtick.minor.size": 1.2,
    "xtick.minor.width": 0.4,
    "xtick.major.pad": 2.0,
    "ytick.major.pad": 2.0,
    "pdf.fonttype": 42,
})


def load(csv):
    df = pd.read_csv(csv)
    published = pd.to_datetime(df["Date"], format="mixed", errors="coerce").dt.year
    added = pd.to_datetime(df["Date Added"], format="mixed", errors="coerce")
    n_bad = published.isna().sum() + added.isna().sum()
    if n_bad:
        print(f"warning: {n_bad} unparsed dates dropped")
    return published.dropna().astype(int), added.dropna().sort_values().reset_index(drop=True)


def months(t0, t1):
    return (t1 - t0).days / 30.44


def style_grid(ax):
    ax.grid(axis="y", color=RULE, linewidth=0.5)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)


# ------------------------------------------------------------------ left: publications per year
def plot_years(ax, years, export):
    last = max(years.max(), export.year)
    xs = [OLD_YEAR - 1] + list(range(OLD_YEAR + 1, last + 1))  # one empty slot separates the aggregate bar
    ys = [(years <= OLD_YEAR).sum()] + [(years == y).sum() for y in range(OLD_YEAR + 1, last + 1)]
    colors = [BASE] * len(xs)
    partial = export < pd.Timestamp(f"{last}-12-31")
    if partial:
        colors[-1] = matplotlib.colors.to_hex(np.array(matplotlib.colors.to_rgb(BASE)) * 0.45 + 0.55)
    ax.bar(xs, ys, width=0.72, color=colors, linewidth=0, zorder=2)
    if partial:
        ax.text(xs[-1], ys[-1] + 1.5, "partial", ha="center", va="bottom", rotation=90, fontsize=FS_ANN - 1,
                color=GREY)

    ticks = [OLD_YEAR - 1] + list(range(OLD_YEAR + 4, last + 1, 4))
    ax.set_xticks(ticks, [rf"$\leq${OLD_YEAR}"] + [str(t) for t in ticks[1:]])
    ax.set_xlim(OLD_YEAR - 2, last + 1)
    ax.set_ylim(0, 10 * np.ceil(max(ys) / 10) + 2)
    ax.set_yticks(np.arange(0, max(ys) + 10, 10))
    ax.set_xlabel("Publication year")
    ax.set_ylabel("Number of works")
    style_grid(ax)


# ------------------------------------------------------------------ right: sourcing progress
def phases(added, export):
    n1 = int((added <= PROJECT_START).sum())
    n2 = int(((added > PROJECT_START) & (added <= PHASE3_START)).sum())
    n3 = int((added > PHASE3_START).sum())
    r2 = n2 / months(PROJECT_START, PHASE3_START)
    r3 = n3 / months(PHASE3_START, export)
    print(f"phase 1: {n1} works at {PROJECT_START.date()}")
    print(f"phase 2: +{n2} works in {months(PROJECT_START, PHASE3_START):.1f} months ({r2:.1f}/month)")
    print(f"phase 3: +{n3} works in {months(PHASE3_START, export):.1f} months ({r3:.1f}/month), total {len(added)}")
    return n1, n2, n3, r2, r3


def cumulative(added, export):
    t = added.where(added > PROJECT_START, PROJECT_START)
    y = np.arange(1, len(t) + 1)
    keep = np.r_[t.values[1:] != t.values[:-1], True]  # last count at each timestamp
    t, y = pd.DatetimeIndex(t.values[keep]), y[keep]
    return t.append(pd.DatetimeIndex([export])), np.r_[y, y[-1]]


def date_axis(ax, x0, x1):
    ax.set_xlim(x0, x1)
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=(4, 10)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))


def badge(ax, x, y, k, **kw):
    ax.text(x, y, rf"\textbf{{{k}}}", ha="center", va="center", fontsize=FS_ANN - 1, color="white", zorder=6,
            bbox=dict(boxstyle="circle,pad=0.18", fc=INK, ec="none"), **kw)


def phase_label(ax, x, y, k, *lines, ha="left"):
    """Badge k, then lines stacked downward from (x, y): the phase name in ink, the last line (its figure) in grey."""
    sign = 1 if ha == "left" else -1
    badge(ax, x, y, k)
    for i, line in enumerate(lines):
        ax.annotate(line, (x, y), xytext=(sign * 6.5, 2.2 - i * (FS_ANN + 1.2)), textcoords="offset points",
                    ha=ha, va="center", fontsize=FS_ANN, color=GREY if i == len(lines) - 1 else INK, zorder=6)


def plot_progress(ax, added, export, variant):
    n1, n2, n3, r2, r3 = phases(added, export)
    t, y = cumulative(added, export)
    x0, x1 = PROJECT_START - pd.Timedelta(days=45), export + pd.Timedelta(days=25)
    ymax = 50 * np.ceil((len(added) + 25) / 50)

    ax.axvspan(PHASE3_START, x1, color=BAND, linewidth=0, zorder=0)
    ax.step(t, y, where="post", color=BASE, linewidth=1.2, solid_joinstyle="round", zorder=3)
    ax.plot([PROJECT_START], [n1], "o", ms=3.6, color=BASE, mec="white", mew=0.8, zorder=4)
    ax.plot([export], [len(added)], "o", ms=3.6, color=BASE, mec="white", mew=0.8, zorder=4)
    ax.text(export - pd.Timedelta(days=12), len(added) + 10, rf"{len(added)}", ha="right", va="bottom",
            fontsize=FS_ANN, color=INK)

    d = pd.Timedelta(days=1)
    if variant == "A":
        # Each label sits in the empty space next to the part of the curve it describes.
        phase_label(ax, PROJECT_START + 30 * d, n1 - 32, 1, "Initial bulk", rf"{n1} works, Jul 2024")
        phase_label(ax, PROJECT_START + 120 * d, 262, 2, "Passive monitoring", rf"$\approx${r2:.0f} works/month")
        phase_label(ax, PHASE3_START - 40 * d, 420, 3, "Active writing,", "gap filling",
                    rf"$\approx${r3:.0f} works/month", ha="right")
    else:
        # Numbered badges on the curve, explained by a key in the empty upper-left corner.
        def on_curve(x):
            return y[max(t.searchsorted(x, side="right") - 1, 0)]
        badge(ax, PROJECT_START + 30 * d, n1 - 30, 1)
        xm = PROJECT_START + (PHASE3_START - PROJECT_START) * 0.5
        badge(ax, xm, on_curve(xm) + 30, 2)
        x3 = PHASE3_START + (export - PHASE3_START) * 0.4
        badge(ax, x3 - 38 * d, on_curve(x3) + 5, 3)
        key = [rf"Initial bulk: {n1} works (Jul 2024)", rf"Passive monitoring: $\approx${r2:.0f} works/month",
               rf"Writing, gap filling: $\approx${r3:.0f} works/month"]
        for i, line in enumerate(key):
            yk = ymax - 25 - i * 0.075 * ymax
            badge(ax, PROJECT_START, yk, i + 1)
            ax.annotate(line, (PROJECT_START, yk), xytext=(6.5, 0), textcoords="offset points", ha="left",
                        va="center", fontsize=FS_ANN, color=INK)

    date_axis(ax, x0, x1)
    ax.set_ylim(0, ymax)
    ax.set_yticks(np.arange(0, ymax + 1, 100))
    ax.set_xlabel("Date added")
    ax.set_ylabel("Cumulative number of works")
    style_grid(ax)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default=CSV)
    p.add_argument("--out", default=OUT)
    p.add_argument("--variant", default="A", choices="AB")
    p.add_argument("--export-date", default=None, help="end of the curve (default: CSV modification time)")
    a = p.parse_args()
    export = pd.Timestamp(a.export_date or dt.datetime.fromtimestamp(os.path.getmtime(a.csv)).date())

    years, added = load(a.csv)
    export = max(export, added.max().normalize())
    fig = plt.figure(figsize=(W, H))
    gs = fig.add_gridspec(1, 2, width_ratios=(1, 1.12), wspace=0.30, left=0.075, right=0.995, bottom=0.2,
                          top=0.97)
    plot_years(fig.add_subplot(gs[0]), years, export)
    plot_progress(fig.add_subplot(gs[1]), added, export, a.variant)
    fig.savefig(a.out)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
