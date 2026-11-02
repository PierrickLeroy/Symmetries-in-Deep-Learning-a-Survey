# `fig:param-space-symmetries` — notes on building the figure

Status (2026-11-02): both panels done and merged; `main.tex` (≈ l. 1415) includes `images/param-space-symmetries.pdf` (Figure 3, p. 33), caption (b) written.

## 1. Files

| File | Role |
|---|---|
| `images/param-space-symmetries.pdf` | **Merged figure used by `main.tex`**, 184 × 127.4 mm, fonts embedded |
| `images/param-space-symmetries.svg` | Merged figure, Inkscape-editable (layers "Panel a", "Panel b"; ids prefixed `a-`, `b-`) |
| `images/scripts/pagella/make_combined.py` | Merges the two panel SVGs side by side and exports the PDF (`python3 make_combined.py`) |
| `images/param-space-symmetries_left.svg` | **Final left panel (a)**, 92 × 127.4 mm, Inkscape-editable |
| `images/draft/param-space-symmetries.png` | Hand-drawn draft of both panels (right half = right panel) |
| `images/scripts/pagella/make_left_final.py` | Generator of the final left panel |
| `images/scripts/pagella/make_left_variants.py` | Shared helpers (math text, widths, frames, badges, validator) |
| `images/param-space-symmetries_right.svg` | **Right panel (b)**, 92 × 127.4 mm, Inkscape-editable |
| `images/scripts/pagella/make_right_final.py` | Generator of the right panel (overwrites Inkscape edits if re-run) |
| `images/scripts/pagella/make_right_variants.py` | Unused right-panel alternatives A and C (`python3 make_right_variants.py OUTDIR`) |
| `images/param-space-symmetries_left_pagella-B.svg` | Unused alternative: 138 mm wide, 3 columns (delete if stacking is ruled out) |
| `images/scripts/param_space_symmetries_left.py` | Unrelated earlier generator (LaTeX glyphs + Helvetica); not used for the final; writes `…_left_A/B.svg` |

Regenerating with `cd images/scripts/pagella && python3 make_left_final.py ../../param-space-symmetries_left.svg` **overwrites any Inkscape edits** made to the SVG.

## 2. Target format and placement

- Right panel: **92 mm wide**, ideally **127.4 mm tall** (same height as the left panel), panel label **b** at the same place as **a** (bold TeX Gyre Pagella 10 pt, baseline at $(x,y)=(2.0, 5.2)$ mm).
- Both panels side by side: $2\times 92 = 184$ mm ≤ full MDPI width $=$ `\textwidth` (138.6 mm) $+$ `\extralength` (46.1 mm) $=184.7$ mm.
- Workflow: edit a panel SVG (by hand in Inkscape, or via its generator), then `cd images/scripts/pagella && python3 make_combined.py`, which rebuilds `param-space-symmetries.svg` from the two panels and exports `param-space-symmetries.pdf` (fonts embedded, checked with `pdffonts`). Edits made directly to the merged SVG are lost on the next merge.
- Included with the MDPI full-width pattern; `[!tbp]` as for the other full-width figure (with `[ht]` the 185 mm float was deferred to the last page):

```latex
\begin{figure}[!tbp]
\begin{adjustwidth}{-\extralength}{0cm}
    \centering
    \includegraphics[width=\linewidth]{images/param-space-symmetries.pdf}
\end{adjustwidth}
    \caption{\textbf{(a)} ... \textbf{(b)} ...}
    \label{fig:param-space-symmetries}
\end{figure}
```

## 3. Content of the right panel (from the draft and §"Classifications")

Objects and maps in the draft:

| Draft element | Meaning | Suggested notation (consistent with `main.tex` / `notation.md`) |
|---|---|---|
| $\Theta\subset\mathbb{R}^m$ with coloured curves | parameter space, orbits / level sets through $\theta$ | $\Theta$ |
| $\Theta'\subset\mathbb{R}^{m'}$ | second architecture (architectural symmetry, e.g. neuron splitting) | open question, see §6 |
| $\varphi:\Theta\to\mathcal F$ | implementation map, $\varphi(\theta)=f_\theta$ | $\varphi$ (text uses `\varphi`) |
| $\varphi_{X'}:\Theta\to\mathcal F_{\vert X'}$ | implementation restricted to data subset | $\varphi_S$ if $S$ is adopted (§6) |
| $i:\mathcal F\to\mathcal F_{\vert X'}$ | restriction $f\mapsto f_{\vert X'}$ | avoid $i$ (reads as an inclusion); use $r_S$ or $(\cdot)_{\vert S}$ |
| red set in $\mathcal F$ | $i^{-1}(\{\varphi_{X'}(\theta)\})$: functions agreeing with $f_\theta$ on $X'$ | $r_S^{-1}(\{\varphi_S(\theta)\})$ |
| $L_F:\mathcal F\to\mathbb{R}$ | loss that factors through $\varphi$ | $\mathcal{L}_F$ |
| $L_R:\Theta\to\mathbb{R}$ | regularizer | $\mathcal{L}_R$ |
| `AGG` box | aggregation $\mathbb{R}\times\mathbb{R}\to\mathbb{R}$; the text uses a sum | $\mathcal{L}(\theta)=\mathcal{L}_F(f_\theta)+\mathcal{L}_R(\theta)$ |

The diagram commutes: $\varphi_S=r_S\circ\varphi$ and $\mathcal L=\operatorname{AGG}\big(\mathcal L_F\circ\varphi,\ \mathcal L_R\big)$.

### Geometric reading of the six classes

For fixed $\theta$, draw the set of points $g\cdot\theta$ that each class allows, using the **left-panel colour** of that class:

| # | Name (left panel) | Colour | Set to draw | Space |
|---|---|---|---|---|
| 1 | symmetric state | `#332288` | $\theta$ itself, $g\cdot\theta=\theta$ with $g\neq e$ (dot + self-loop arrow); $g\in G_\theta$ | $\Theta$ |
| 2 | functional | `#3b9fc9` | fiber $\varphi^{-1}(\{f_\theta\})$ through $\theta$; maps to the single point $f_\theta$ | $\Theta$ → point in $\mathcal F$ |
| 3 | loss (factoring) | `#117733` | level set $\mathcal L_F^{-1}(\{\mathcal L_F(f_\theta)\})\ni f_\theta$; its preimage under $\varphi$ contains the fiber | $\mathcal F$ (and $\Theta$) |
| 4 | loss | `#882255` | level set $\mathcal L^{-1}(\{\mathcal L(\theta)\})\ni\theta$ | $\Theta$ |
| 5 | data-dependent | `#999933` | $\varphi_S^{-1}(\{\varphi_S(\theta)\})\supseteq$ fiber; in $\mathcal F$: $r_S^{-1}(\{\varphi_S(\theta)\})\ni f_\theta$ | $\Theta$, $\mathcal F$, $\mathcal F_{\vert S}$ |
| 6 | instance | `#ee6677` | region $U\subsetneq\Theta$ on which fibers are larger than generic fibers | $\Theta$ |

Constraints so that the right panel does not contradict the left panel's inclusions ($1\subset2$, $1\subset4$, $2\subset3$, $2\subset5$, $2\subset6$):
- $\{\theta\}\subseteq$ fiber $\subseteq\varphi^{-1}\big(\mathcal L_F^{-1}(\mathcal L_F(f_\theta))\big)$ and fiber $\subseteq\varphi_S^{-1}(\varphi_S(\theta))$: draw the blue fiber **inside** the green and olive sets.
- The wine level set (4) passes through $\theta$ but need **not** contain the fiber ($2\not\subset4$): draw it crossing the blue curve, not along it.
- (6) does not enlarge the reachable set at a given $\theta\in U$ (still $f_{g\theta}=f_\theta$); what changes is that $g$ is only valid on $U$. Show $U$ as a region where fibers jump in dimension.
- Concrete shapes from the left-panel network $\mathcal N$ (optional): fiber of (2) is the line $\eta+\mathbb{R}\mathbf 1$; $U=\{\theta_2<0\}$ is a half-space mapped to the single function $\mathbf 1/3$; with $S=\{0\}$, $\varphi_S$ is constant, so its fiber is all of $\Theta$.

The draft's freehand colours (red, orange, green, purple, yellow, blue) should be remapped to this palette (same meaning = same colour across panels).

## 4. Style spec shared with the left panel

- Units: 1 SVG user unit = 1 mm; coordinates rounded to 0.1 mm; all text stays `<text>` (subscripts as `<tspan style="font-size:70%;baseline-shift:sub">`).
- Fonts: math in **TeX Gyre Pagella Math** (matches `mathpazo`), using Unicode math italics: $\theta$ U+1D703, $\eta$ U+1D702, $\sigma$ U+1D70E, `\varphi` → U+1D711 (𝜑, not U+1D719 ϕ), $\mathcal F$ U+2131 (ℱ), $\mathcal L$ U+2112, $\mathcal N$ U+1D4A9, $\mathbf 1$ U+1D7CF, $\mathbb R$ U+211D. Labels, badges, names: **TeX Gyre Pagella Bold**.
- Sizes (pt): panel label 10; setup text 8; large network labels 8.5; small network labels 6.3; notes and legend 6; subplot names 6.5 bold; badge numbers 7.5 bold; ⊂ glyph 12.
- Colours: ink `#222222`; edges and nodes `#555555`; connectors `#888888`. Class colours as in §3: Paul Tol set, min pairwise $\Delta E\ge 22$ in normal, protan, deutan and tritan simulation.
- Strokes (mm): edges 0.28 (highlighted 0.5); large network 0.33 / 0.6; frames 0.35 with fill-opacity 0.07 of the class colour, corner radius 1.6; connectors 0.3.
- Arrowheads: one `<marker>` per colour, `markerUnits="userSpaceOnUse"`, 1.5 mm, `orient="auto-start-reverse"`. Skill rule: map arrows ≥ 10 mm long, ≥ 3 mm clear of text.
- Inkscape layers: `Setup`, `Subplots`, `Inclusions`, `Legend`; each subplot is a group labelled e.g. "(2) functional symmetry".

## 5. Tooling

- Inkscape crashes when launched from the VS Code terminal (snap environment). Use:
  `env -u GSETTINGS_SCHEMA_DIR -u GTK_PATH -u GTK_EXE_PREFIX -u GIO_MODULE_DIR -u GDK_PIXBUF_MODULE_FILE -u GDK_PIXBUF_MODULEDIR -u LOCPATH XDG_DATA_DIRS=/usr/local/share:/usr/share inkscape …`
- Preview: `inkscape X.svg --export-type=png --export-dpi=300 --export-background=white -o X.png`.
- Reusable helpers in `make_left_variants.py`:
  - `Doc.text` takes a mini math markup: `_x` / `_{..}` subscript, `^x` superscript; single Latin letters and Greek become math italic; multi-letter words stay upright; `\word` forces upright; `-` is a spaced minus, `−` a unary one.
    Add `"φ": "\U0001D711"` to `ITALIC_GREEK` before using $\varphi$.
  - `width` measures text with fontTools.
  - `Doc.line` / `rect` / `swap_arc` / `marker` draw shapes; `subset_glyph` draws a centred, rotated ⊂; `number_tag` draws a badge.
  - `validate` reads real bounding boxes via `inkscape --query-all` and flags text closer than 1 mm to its frame, text/text overlaps, and lines crossing text.

## 6. Open issues and caption to-dos

1. **Panel naming:** the caption says **Left./Right.** but the panel is labelled **a**. Switch to (a)/(b), and write the right-panel caption (currently empty).
2. **Data-subset notation:** text uses $S\subsetneq\mathcal X$; caption and left panel (note in subplot 5: "$X'=\{0\}$") use $X'\subsetneq X$. Pick one. $S$ matches the text and `notation.md` (spaces calligraphic). Changing the left panel is one string in `SUBPLOTS[5]["notes"]`.
3. **Caption typos:**
   - (6) reads $f_{g\theta}=f(\theta)$; should be $f_{g\theta}=f_\theta$.
   - "not exhaustive,:" has a stray comma.
4. **Item (4) in the caption:** the left panel uses $\mathcal L=\mathrm{CE}+\lVert\theta\rVert_1$, $\theta_2=x=1$, and $\Delta=\log(5/2)=\log5-\log2$, not $\log5-2\log2$.
   - Step (i) $\eta_2\gets0$ lowers CE by $\log(5/4)$ and $\ell_1$ by $\log2$.
   - Step (ii) $\eta\gets\eta+(\Delta/3)\mathbf 1$ leaves CE unchanged and raises $\ell_1$ by $\Delta$.
   - With weight $\lambda$ on $\ell_1$: $\Delta=\log2+\lambda^{-1}\log(5/4)$.
5. **$\Theta'$:** resolved (2026-11-02): kept in the right panel without its own colour or a map $\Theta\to\Theta'$; $\varphi$ is overloaded on $\Theta'$ (§7).
6. **Left-panel layout:** 2 columns (3/2/1 left, 5/6/4 right), so "larger sets higher" holds only for 1 ⊂ 2 ⊂ 3 and 2 ⊂ 5. The ⊂ glyphs make every relation explicit.

## 7. Right panel (b): what was built (2026-11-02)

Regenerate: `cd images/scripts/pagella && python3 make_right_final.py ../../param-space-symmetries_right.svg` (validator: 0 issues).

**Layout (variant B, "commutative square").** Top row: the modified spaces $\Theta'\subseteq\mathbb R^m$ (larger architecture; $n,m$ as in the "Architectural Symmetry" paragraph) and $\mathcal F_{\vert X'}$. Middle row: $\Theta\subseteq\mathbb R^n\xrightarrow{\varphi}\mathcal F$, with $\varphi:\Theta'\to\mathcal F$ curving in from above and $i:\mathcal F\to\mathcal F_{\vert X'}$ going up.
Bottom: $\mathcal L_R$ under $\Theta$ and $\mathcal L_F$ under $\mathcal F$, both copies of $\mathbb R$ feed `AGG`, which maps down to a third $\mathbb R$. Legend (line sample + class number + set) bottom right.
Frames and blobs use the left-panel frame recipe in grey: `fill:#555555;fill-opacity:0.07;stroke:#555555;stroke-width:0.35`, corner radius 1.6 (`FRAME_STYLE`). Label at $f_\theta$: $f_\theta=\varphi(\theta)$. Curves in $\mathcal F$ are trimmed to stay ≥ 1.6 mm inside the blob (`clip_inside`).

**Visual code.**
- Colour $k$ in $\Theta,\Theta'$ = set reached from $\theta$ by class $k$. Coincident sets are parallel lines of one ribbon (line 0.32 mm, spacing 0.62 mm).
- A dot of colour $k$ is the point whose preimage is the colour-$k$ set: $f_\theta$ (2), $\mathcal L_F(f_\theta)$ (3), $\mathcal L(\theta)$ (4), $i(f_\theta)$ (5). $\theta$, $\tilde\theta$, $\mathcal L_R(\theta)$ are ink.
- (1) The two components of $G\theta$ are mirror images about $G\tilde\theta$: reading $G\supseteq\mathbb Z_2$, $\tilde\theta$ is fixed by the reflection (stabilizer $\mathbb Z_2$), so its orbit has one component. The orbit stripe faces $G\tilde\theta$.
- In $\Theta$: two $G\theta$ ribbons carry (1)(2)(3)(5); extra closed fibre component (2)(3)(5); extra arcs (3) and (5); the (4) level set crosses the ribbon at $\theta$.
- In $\Theta'$: two fibre ribbons (2)(3)(5); extra arcs (3), (5); separate (4) arc. No point is marked in $\Theta'$.
- In $\mathcal F$: level set $\mathcal L_F^{-1}(\mathcal L_F(f_\theta))$ (green) and fibre $i^{-1}(i(f_\theta))$ (olive) cross at $f_\theta$.

**Choices to confirm.**
1. $i$ is a plain arrow, not a hooked $\hookrightarrow$: restriction is surjective and not injective (the olive curve in $\mathcal F$ is a non-trivial fibre of $i$).
2. Level sets are written $\mathcal L_F^{-1}(\mathcal L_F(f_\theta))$ and $\mathcal L^{-1}(\mathcal L(\theta))$ (the request wrote $\mathcal L_F^{-1}(f_\theta)$ and $L^{-1}(\theta)$).
3. Labels follow `main.tex`: $\mathcal L_F$ (not $\mathcal L_{\mathcal F}$), $\Theta\subseteq\mathbb R^n$, $\Theta'\subseteq\mathbb R^m$ (draft: $m$, $m'$).
4. The tilde of $\tilde\theta$ is a spacing `˜` in a shifted `<tspan>` (the combining U+0303 collides with 𝜃 in Inkscape). When retyping it in Inkscape, keep the tspan or redraw it.

**Caption draft (b).**
Spaces and maps: $\varphi$ sends $\Theta$ and the parameter space $\Theta'$ of a larger architecture to $\mathcal F$, $i$ restricts functions to $X'$, and the loss aggregates $\mathcal L_F$ and $\mathcal L_R$.
In $\Theta$ and $\Theta'$, each colour shows the set of parameters reached from $\theta$ by the class of the same colour in (a); coincident sets are drawn as parallel stripes.
A coloured dot is the point whose preimage is the set of that colour.
(1) $G\theta$ has two components, mirror images of each other, while the more symmetric $\tilde\theta$ has a one-component orbit $G\tilde\theta$.
(4) The level set of $\mathcal L$ crosses the fibre of $\varphi$ at $\theta$ without containing it.

**Variants (2026-11-02), B chosen.** A = parameter spaces side by side on top, flow downwards (first version). B = commutative square: $\Theta'$ and $\mathcal F_{\vert X'}$ on top, $\Theta\xrightarrow{\varphi}\mathcal F$ in the middle, losses below; outline-only spaces, thin separated lines, legend with line samples. C = $\Theta$ as a full-width hero with set labels written next to each curve (no legend), $\Theta'$ and $\mathcal F_{\vert X'}$ to the right of the compact diagram; warm fills, stripes with thin gaps. All three: same content, 92 × 127.4 mm, all arrows ≥ 10 mm, validator 0 issues. B is now `make_right_final.py`; A and C were deleted as SVGs and can be regenerated with `make_right_variants.py`.
