# Notation conventions
---

## 1. Group theory

| Meaning | Notation |
|---|---|
| Group | $G$ |
| Orbit of $x$ | $G\cdot x$ |
| Stabilizer of $x$ (subgroup of $G$ fixing $x$) | $G_x$, or $\operatorname{Stab}(x)$ where the functional form reads better |
| Stabilizer of an injected pose feature $v$ | $\operatorname{Stab}(v) = \{g : \rho(g)v = v\}$ |
| $\epsilon$-stabilizer (Petrache–Trivedi) | $\operatorname{Stab}_\epsilon(f)$ |
| Structure group of a principal bundle / gauge group (allowed changes of frame) | $H$, with $H\le GL(d)$ for frame bundles |
| Automorphism group of a **graph** | $\operatorname{Aut}(\Gamma)$ |
| Automorphism group of a **group** | $\operatorname{Aut}(N)$ |
| Symmetry group of a function | $\operatorname{Sym}(f)$ |
| All bijections of a set | $\operatorname{Sym}(\mathcal{X})$ |

Flags:
- $\operatorname{Sym}$ carries multiple senses.
  They are disambiguated by their argument (a function, a set, a representation-with-superscript)

Write $g\cdot x$ when the action is unambiguous — in particular when $G$ acts
the same way on $\mathcal{X}$ and $\mathcal{Y}$.

Write $\rho_X(g)$ and $\rho_Y(g)$ when the two actions must be distinguished:

$$f(\rho_X(g)\,x) = \rho_Y(g)\,f(x).$$

## 2. Spaces and maps

| Object | Notation | Note |
|---|---|---|
| Space acted on by $G$ (input) | $\mathcal{X}$ | Also the $G$-set, homogeneous space, and bundle base manifold in the Background |
| Output / target space | $\mathcal{Y}$ | |
| Latent / embedding space | $\mathcal{Z}$ | |
| Dataset | $\mathcal{D}$ | |
| Ground truth (target map of the problem) | $f^*$ | Never $f$, $f^\star$ or $f^\ast$; plain $f$ is a generic map, $f_\theta$ the implemented function |
| Hypothesis class | $\mathcal{H}$ | |
| Function space | $\mathcal{F}$ | |
| Continuous $G$-equivariant maps $\mathcal{X}\to\mathcal{Y}$ | $C_G(\mathcal{X},\mathcal{Y})$ | Invariant case: trivial action on $\mathcal{Y}$, e.g. $C_G(\mathcal{X},\mathbb{R})$. Topology of uniform convergence on compact sets unless stated; closure written $\overline{\mathcal{H}}$ (not `\bar`) |
| Linear $G$-equivariant maps (intertwiners) | $\operatorname{Hom}_G(V,W)$ | Linear counterpart of $C_G$; already used in the Background |
| Augmentation family | $\mathcal{T}$ | |
| Vector space carrying a representation | $V$, $W$ | Plain, not calligraphic — these are representation carriers, not data spaces |
| Manifold in a purely geometric statement | $M$ | e.g. GEOMANCER's $M = M_1\times M_2$ |

**Subscripts naming a space use the plain letter**, not the calligraphic one:
$\rho_X$, $\rho_Y$, $\rho_Z$, $d_Y$, $p_X$, $\operatorname{id}_X$.
The rationale is that the subscript is a *label* identifying which space is
meant, while the calligraphic letter denotes the space itself. This avoids
$\rho_{\mathcal{X}}$, which is heavy and non-standard.

## 3. Losses and risks

| Symbol | Meaning |
|---|---|
| $\ell$ | Per-example loss, $\ell(x,\theta)$ |
| $L$ | Loss criterion comparing a prediction to a target, $L(\hat y, y)$ |
| $\mathcal{L}$ | Single argument loss $\Theta \to \mathbb R$ or $\mathcal F \to \mathbb R$ or full training objective (SimCLR, Barlow Twins, DINO, …) |
| $\hat R$ | Empirical risk |
| $R$ | Population risk |

## 4. Errors

| Symbol | Meaning |
|---|---|
| $\lVert f\rVert_{\mathrm{EE}}$ | Global equivariance error, $\sup_{g,x} d_Y(f(\rho_X(g)x), \rho_Y(g)f(x))$ |
| $\operatorname{ee}(f,g)$ | Per-element equivariance error, for a single $g$ |
| $\epsilon$ | Tolerance (never `\varepsilon`) |

## 5. LaTeX style

- Braces always: `\mathbb{R}`, `\mathcal{X}`, `\mathfrak{g}`.
- `\operatorname{}` for function-like operator names; `\mathrm{}` for
  text-like subscripts ($L_{\mathrm{orbit}}$, $\lVert\cdot\rVert_{\mathrm{EE}}$).
  Never `\text{}` inside math for either purpose.
- `\Cref{}` for every cross-reference. Not `\ref`, not `Definition~\ref`,
  not `\S\ref`.
- `\citet{}` when the work is the grammatical subject
  ("\citet{cohen2016} showed…"); `\citep{}` when parenthetical or appositive
  ("Spherical CNNs \citep{cohen2018} use…").
- LaTeX quotes ` ``…'' `, em-dashes `---`, `\emph{}` for emphasis (no
  markdown asterisks).
