# Final pass: mathematical notions in `main.tex` (2026-11-11)

Scope: every definition, theorem, formula and named mathematical notion in [main.tex](main.tex), checked for
(1) technical correctness and ambiguity, (2) consistency with [notation.md](notation.md), (3) whether it is introduced before or where it is used.

- 282 minimal edits applied (276 lines changed). The file compiles cleanly: 2 `pdflatex` runs, 0 errors, 0 undefined references.
- Backup of the previous version: [old-files/main_2026-11-11_before-final-math-pass.tex](old-files/main_2026-11-11_before-final-math-pass.tex). Full diff: [old-files/main_2026-11-11_final-math-pass.diff](old-files/main_2026-11-11_final-math-pass.diff).
- Line numbers below refer to the **current** `main.tex`.
- Doubtful claims were checked against `summaries/` and, where needed, `raw/` (Frankle 2020, Lyle 2020, Brea 2019, Grigsby 2023, Grillo 2026, Elsayed 2020, Ziyin 2024/2024a/2025a, Arjevani 2023, Neyshabur 2015, Tran 2025, Ali 2026, Wang 2023a, Urbano 2026, Otto 2025).

Structure: **A** needs your decision · **B** fixes already applied · **C** full inventory. All three are in reading order.

---

## A. Needs your decision (reading order)

✔**A1. "Extent restricted" is defined as a subset of $G$, but includes semigroups and groupoids.**
[Table 1, L190](main.tex#L190), [§6.2, L2282](main.tex#L2282), [Table 5 caption, L2302](main.tex#L2302).
"$g\in S\subsetneq G$ (a subgroup, a non-closed set or a semigroup)": non-invertible maps (crop, blur, downsampling) and the overparametrization groupoid are not subsets of any group $G$.
Suggested wording: *"it holds only on a restricted set of transformations: a subset $S\subsetneq G$ (a subgroup or a non-closed subset), a weaker structure such as a semigroup or a groupoid, or only on part of the domain (local, instance-level)."*
Also in Table 5, the row "Non-closed subset: identity ✓, inverses ✓" is true for $[-90^\circ,90^\circ]$ but not by definition (Romero's $S$ need not contain inverses).

✔**A2. The "tilt" example in "One rotation, several forms"** ([L333](main.tex#L333)).
$\rho_Y(r)=-I$ is a valid homomorphism ($(-I)^4=I$), but $r$ is a $90^\circ$ rotation. If $f$ predicts a vector of $\mathbb{R}^2$ (a direction, a force), that vector rotates by $90^\circ$, i.e. $\rho_Y(r)=J=\left(\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\right)$ (the $J$ of §2.5).
$-I$ is correct for an *unoriented axis* encoded as $(\cos2\alpha,\sin2\alpha)$, since $\alpha\mapsto\alpha+\pi/2$ gives $2\alpha\mapsto2\alpha+\pi$.
Choose: (a) "a $2\times2$ rotation matrix $\rho_Y(r)=J$ if $f$ predicts a vector in $\mathbb{R}^2$", or (b) keep $-I$ and write "if $f$ predicts an axis (undirected line) encoded as $(\cos2\alpha,\sin2\alpha)\in\mathbb{R}^2$". Option (b) keeps the example's point that the forms really differ.

✔**A3. Number of classes written $L$** ([L270](main.tex#L270), L273, L277). This clashes with the criterion $L(\hat y,y)$. Low priority; any other letter works.

✔**A4. Domain symbol in §3.1.** GDL uses $\Omega$ ([L554](main.tex#L554)), but the $G$-CNN paragraph says "a function on the domain $\mathcal{X}$ … projected back to $\mathcal{X}$" ([L576–578](main.tex#L576)), and §2.3 uses $\mathcal{X}=\mathbb{R}^d$ as the base space of feature fields. Suggest using $\Omega$ for the domain throughout §3.1.
*Applied 2026-11-12:* $\Omega$ is the domain with points $u$, and $\mathcal{X}=\mathcal{X}(\Omega,\mathbb{R}^C)$ is the space of signals with the induced action $(g\cdot x)(u)=x(g^{-1}\cdot u)$ (L554–555). Edits also at L480, L483–484, L487, L577, L579 and L2359. The groupoid is now $\mathcal{G}(S,V)$ and the sublevel sets $\Theta_{\le\lambda}$. A row was added to notation.md.

✔**A5. Named but never introduced: spherical harmonics, tensor products, 1-WL** ([L599](main.tex#L599), L612, [L725](main.tex#L725)). Suggested one-liners:
- *spherical harmonics $Y^\ell_m$: functions on $S^2$ that span the irreducible representations of $SO(3)$ (degree $\ell$, dimension $2\ell+1$);*
- *tensor products of irreps, decomposed back into irreps by Clebsch–Gordan coefficients;*
- *1-WL (colour refinement) repeatedly relabels each node by hashing its label with the multiset of its neighbours' labels; two graphs are distinguished when their label histograms differ.*

✔**A6. The Deep Sets theorem is stated twice** ([L620](main.tex#L620): $\psi(\sum_i\phi(x_i))$ with $X$ a matrix; [L712](main.tex#L712): $\psi(\sum_{x\in X}\phi(x))$ with $X$ a set). Keep one and cross-reference it. It also uses $\phi$, which notation.md reserves for $\phi$-equivalence (but $\rho$ is taken too).

✔**A7. What is random in the exchangeability display?** ([L904–907](main.tex#L904))
$\operatorname{Law}(\mathcal{A}(\sigma\cdot\mathcal{D},\theta_0))=\operatorname{Law}(\mathcal{A}(\mathcal{D},\theta_0))$.
If $\mathcal{D}$ is exchangeable, this holds for *any* measurable $\mathcal{A}$ (a pushforward), so it does not need Bloem-Reddy & Teh.
Their functional representation fits **random reshuffling** better: with a uniform permutation $\sigma'$ drawn by the algorithm, $\theta_T=\mathcal{A}(\sigma'\cdot\mathcal{D},\theta_0)=f(\eta,\mathbb{M}_{\mathcal{D}})$ with $\eta=\sigma'$ independent noise. So *conditionally on $\mathcal{D}$*, the law of $\theta_T$ is $S_n$-invariant.
Suggested rewrite: *"Restricting to a single epoch and letting $\mathcal{A}$ draw its ordering uniformly at random, $\theta_T$ depends on $\mathcal{D}$ only through $\mathbb{M}_{\mathcal{D}}$ and independent noise, so that $\operatorname{Law}(\mathcal{A}(\sigma\cdot\mathcal{D},\theta_0)\mid\mathcal{D})=\operatorname{Law}(\mathcal{A}(\mathcal{D},\theta_0)\mid\mathcal{D})$ for all $\sigma\in S_n$."*

✔**A8. "Branch symmetry" has no formal definition** ([L935](main.tex#L935)), and "weight entangling" is unclear.
Suggested: *"A branch symmetry: the objective is invariant under swapping the two branches, $(\theta_1,t)\leftrightarrow(\theta_2,t')$; with shared weights $\theta_1=\theta_2$ and a symmetric $L$ this is an exact $C_2$ symmetry."*

✔**A9. Joint-embedding symbols.** The projection head is $g$ ([L946](main.tex#L946), BYOL, DINO), which clashes with group elements $g$ in the same formulas as $t\cdot x$. The loci figure writes $\tau_i\cdot x$, while the text uses $t,t'$ (and $\tau$ is the temperature). Suggest renaming the head (e.g. $\operatorname{proj}$) and aligning the figure with $t,t'$.

✔**A10. Shallow networks written $U\sigma(Vx)$** ([L1203](main.tex#L1203), [L1254](main.tex#L1254)). $U$ is the optimizer update map (Table 1, Eq. equivariant-optimizer) and $V$ a representation space. The sign-flip and orthogonal paragraphs already use $W_2\sigma(W_1x)$. Suggest $W_2,W_1$ everywhere.

✔**A11. Data-dependent subset: $S$ in the text, $X'$ in Fig. 4** ([L1133](main.tex#L1133), L1201). In §6, $S$ also denotes a subset of $G$. Suggest $\mathcal{X}'$ in both the text and the figure.

▢**A12. False-class remark and churn** ([L1183](main.tex#L1183)). Churn compares predicted labels. The link to false classes only holds on misclassified points, where the prediction is a false class set by unconstrained logits. Either say so or drop the churn mention.

▢**A13. Table 4, lightning self-attention row** ([L1361](main.tex#L1361)). The text ([L1303](main.tex#L1303)) classifies $(A,V)\mapsto(\lambda A,\lambda^{-1}V)$ as *Rescale*, but the table puts it under *Scale*. Also, the $GL(d_k)$ symmetry acts *within* a layer on $K^\top Q$ (with an extra between-layer $GL$ in deep networks), while the table says "between-layer" only.

▢**A14. Multi-head attention group (changed, please confirm)** ([L1935](main.tex#L1935)). Tran et al. write $S_h\times GL^h\times GL^h$. Permuting heads reindexes the per-head factors, so the two parts do not commute. I wrote $\big(GL(d_k)^h\times GL(d_v)^h\big)\rtimes S_h$, consistent with your $(\mathbb{R}_{>0})^d\rtimes S_d$ in Example "Groups in this survey", and noted the authors' notation. Revert if you prefer to quote them verbatim.

✔**A15. The exactness criterion and "holds exactly"** ([L2126](main.tex#L2126) vs [L2282](main.tex#L2282)).
The text says "extent-restricted if $\operatorname{Stab}_\epsilon(f)=S\subsetneq G$", but §6.2 says an extent-restricted symmetry "holds exactly" on $S$, i.e. $S\subseteq\operatorname{Stab}_0(f)$.
With $\operatorname{Stab}_\epsilon$, the classification depends on $\epsilon$, and "extent-restricted" also covers "approximate on $S$".
Options: (a) extent-restricted if $\operatorname{Stab}_0(f)=S\subsetneq G$; (b) keep $\epsilon$ and soften §6.2 to "holds (up to $\epsilon$) only on $S$".
Fig. 5(b), with $\operatorname{ee}\approx0$ on $S$, matches (a). I already fixed the downstream statement at [L2335](main.tex#L2335), which was wrong under both readings.

▢**A16. Fig. 5 uses $\theta$ for the rotation angle** ($\operatorname{ee}(f,\theta)$). $\theta$ denotes parameters in notation.md. Suggest $\alpha$ in the SVG.

▢**A17. Lawrence et al.'s "task-useful" metric** ([L2238–2240](main.tex#L2238)).
- $L$ and $L_G$ are accuracies (expected indicator of a correct prediction), yet named like the criterion $L$.
- $L_G$ needs an expectation over $g$.
- $c:\mathcal{X}\to G$ is a *pose map*, while notation.md uses $c$ for the canonicalization $\mathcal{X}\to\mathcal{X}$.

Suggest $A$ and $A_G=\mathbb{E}_{x,g}[\dots]$, and e.g. $\gamma:\mathcal{X}\to G$ with canonical form $\gamma(x)^{-1}x$.

▢**A18. Lawrence 2024 identity** ([L2210–2212](main.tex#L2210)). The pose is $\tilde g$ in the text, then $Z$ in $\mathbb{P}(X,Z)$. Unify the two.

▢**A19. Results stated twice.**
- Arjevani: [L2274](main.tex#L2274) and [L2327](main.tex#L2327).
- Kunin's weight-decay law: [L1535](main.tex#L1535) and [L2261](main.tex#L2261).
- Quessard: [L2010](main.tex#L2010) and [L2323](main.tex#L2323).

Keep one of each and cross-reference.

▢**A20. Goldstone modes** ([L1838](main.tex#L1838)). The regularizer breaks the symmetry explicitly but weakly, which gives *pseudo*-Goldstone modes. Suggest "(pseudo-)Goldstone modes".

▢**A21. "Lie algebra generated by the flow field"** ([L1528](main.tex#L1528)) uses the Lie bracket of vector fields, $[X,Y]=DY\,X-DX\,Y$, not the matrix bracket of §2.5. One gloss would avoid confusion.

▢**A22. Kunin's autoencoder on the Grassmannian** ([L1667](main.tex#L1667)). "The $GL(k)$ symmetry has disappeared": with $L_2$ regularization the residual symmetry is $O(k)$, and the Grassmannian quotients exactly that. Suggest "the residual symmetry has been quotiented out".

▢**A23. Hecht-Nielsen cone** ([L1671](main.tex#L1671)). In $\{x\in\mathbb{R}^q:|x_i|\le|x_k|,\ i\neq k\}$, the quantifier is unclear (for all $i\neq k$, with $k$ fixed?), and $x$ is a parameter vector (better $\theta$).

▢**A24. Undefined term.** "Partial equivariance contributes its own term $E_\epsilon$" ([L2340](main.tex#L2340)): $E_\epsilon$ is never defined.

▢**A25. Equation numbering.** The `align` block in Functional SB ([L2181–2183](main.tex#L2181)) numbers both lines. Add `\notag` to the second line.

▢**A26. Abbreviations list** ([L2548](main.tex#L2548)) is missing EDL, FA, MC/LMC, SS/PS/LS, SLT, RLCT/LLC, TDL, NFN, NTK and GNN/CNN.

▢**A27. Low-priority local symbol reuse** (each is defined locally; listed in case you want a global clean-up):
- $\mathcal{B}$: path height (L1731) and the bias subspace (L1916).
- $\Gamma$: graph, transport plan (L1095), BN scaling (L884), Goodfellow range (L2083), Marcotte's inverse map (L1567).
- $\Omega$: GDL domain, the groupoid $\Omega(S,V)$ (L1206), sublevel sets (L1741).
- $\pi$: quotient map, path vector $\pi(w)$ (L1859), Saul's $\pi_{ji}$ (L1689).
- $\rho_i$: neuron input norm (Saul, L1687).
- $\phi$: feature extractor (Lenc, Petzka, Krippendorf).
- $\overline{W}_t$: direction (L1608) vs the closure overline.
- $I(\theta)$: Fisher information vs the identity.
- $\eta$: noise, parameters, learning rate.
- $\mathcal{A}$: learning algorithm vs parameter subset.
- $B(\theta^\star)$: ball (L1949) vs barrier $B$.
- `\text{or}`, `\text{for all}` in display math: connective words, not operator names, so this seems within the intent of notation.md.

---

## B. Fixes applied (reading order)

### B1. Mathematical errors corrected

| Line | Before | After / why |
|---|---|---|
| [499](main.tex#L499) | matrix Lie groups "include those of Ex. groups" | "up to isomorphism", since $E(n)\hookrightarrow GL(n+1)$ via $(v,R)\mapsto\left(\begin{smallmatrix}R&v\\0&1\end{smallmatrix}\right)$ |
| [524](main.tex#L524) | "one additional constraint per connected component" | at most one per *non-identity* component (generators of $G/G^\circ$ suffice) |
| [683](main.tex#L683) | "…and $K_{\mathrm{self}}$." (truncated) | $K_{\mathrm{self}}=\rho_{\mathrm{out}}(-h)K_{\mathrm{self}}\rho_{\mathrm{in}}(h)$ |
| [724](main.tex#L724) | universality ⇒ orbits "can be take different values (up to continuity)" | $\mathcal{H}$ separates the orbit pairs that continuous invariant functions separate (all pairs for compact $G$) |
| [836](main.tex#L836) | "symmetry group of the domain is a subgroup of the target" | the transferred group must be a subgroup of the *target domain's* symmetry group |
| [845](main.tex#L845) | FA has "strictly lower generalization error" than DA | risk no larger (Jensen) plus tighter PAC-Bayes bounds, as in Lyle et al. (FA ≤ DA) |
| [948](main.tex#L948) | SimCLR: index $i$ undefined, $x_k$ mixed with $t'\cdot x$ | standard $\ell_{i,j}$ over $2N$ views $z_k=g(f(\tilde x_k))$ |
| [972](main.tex#L972) | "Branch-swap symmetry (1)" | it is item 2 of the list |
| [1008](main.tex#L1008) | diagonal invariance called a "subcase" of Eq. invariant-loss; the justification assumed its conclusion | it is *weaker* (implied by $G\times G$ invariance); the justification is now the requirement $L(f(gx),gy)=L(f(x),y)$ |
| [1014](main.tex#L1014) | $[gy]_i=y_{i+n \bmod n}$ (the identity map); "two spatial positions for $n=3$" | $g\cdot(u,v)=(v,u)$ with $S_2$; one position in $\mathbb{R}^3$ |
| [1213](main.tex#L1213) | "actions $G\times\mathbb{R}^n\to\mathbb{R}^m$" | function-preserving maps; not group actions (pointer to groupoids) |
| [1214](main.tex#L1214) | splitting "sharing its outgoing weights" | splitting the outgoing weights between the two copies |
| [1218](main.tex#L1218) | negative rescaling: activation becomes $\tau_v\min(0,x/\tau_v)$, which **equals** $\max(0,x)$ for $\tau_v<0$ | $\tau_v\max(0,x/\tau_v)=\min(0,x)$ (Armenta's change of basis $f'_v(z)=\tau_vf_v(z/\tau_v)$) |
| [1302](main.tex#L1302) | monomial: $\alpha_{\mathcal{A}_1}^{r}\odot\alpha_{\mathcal{A}_2}^{-1}$, wrong if $\mathcal{A}_1$ is incoming, since $(\alpha^r)^r\alpha^{-1}\ne1$ | $(\lambda w_{\mathrm{in}},\lambda^{-r}w_{\mathrm{out}})$, with $\mathcal{A}_1$/$\mathcal{A}_2$ named |
| [1336](main.tex#L1336) | "unit $v$ with negative input parameter $\theta^+_v$" ($\theta^+_v$ undefined) | defined as incoming weights and bias, all negative; from the 2nd hidden layer on |
| [1341](main.tex#L1341) | Grillo: "the function of an $L$-layer ReLU net cannot be realized by any $(L-1)$-layer net" | an *open set* of parameters has this property (Prop. 5.24) |
| [1416](main.tex#L1416) | mirror symmetries: "rotation, permutation, sign flip" | rescaling added, consistent with L2269 and Ziyin 2024 |
| [1450](main.tex#L1450) | never co-active weight "can be perturbed freely" | generically, locally (Grigsby et al.) |
| [1476](main.tex#L1476) | FI: $\{\eta:f_\eta=f_\theta,\ \eta\nsim\theta\}$ finite (infinite as soon as another class exists, since rescaling orbits are continuous) | the fiber consists of finitely many $\sim$-classes |
| [1521](main.tex#L1521) | $(A,B)\mapsto\lVert AB^\top-M^*\rVert^2$ "is not smooth" (it is polynomial) | has no globally Lipschitz gradient |
| [1589](main.tex#L1589) | plateau "contains all $d_k!$ reparametrizations" | all reachable along equal-loss paths (Brea et al.'s statement) |
| [1591](main.tex#L1591), [1667](main.tex#L1667) | Kunin: "minima forced to be symmetric states", $W_1=W_2^\top$ | $W_1=W_2^\top$ is the fixed set of the swap $\tau:(W_1,W_2)\mapsto(W_2^\top,W_1^\top)$; $\tau$ transposes $W_2W_1$ (never PS) and is a loss symmetry only if $XX^\top\propto I$, where it is an O-mirror symmetry. Kunin's theorem holds for any $X$. (Revised 2026-11-12 after review: the first fix wrongly said "not a symmetric state".) |
| [1651](main.tex#L1651) | section picks "one point in each fiber" | in each *orbit* ("fiber" is used for $\varphi$) |
| [1658](main.tex#L1658) | PSI manifold $(\mathbb{R}^{d_1}\times\dots)/\!\sim$ | zero vectors removed (otherwise not a manifold) |
| [1681](main.tex#L1681) | Equi-normalization $D_{k-1}^{-1}W_kD_k$: shapes do not match your convention $W_k\in\mathbb{R}^{d_k\times d_{k-1}}$ (L1441, L1916) | $D_kW_kD_{k-1}^{-1}$, $D_0=D_q=I$ |
| [1731](main.tex#L1731) | path height $\min_\gamma$ | $\inf_\gamma$ |
| [1734](main.tex#L1734) | $G_e$ (reads as the stabilizer of $e$); $B$ used for the path height | $G^\circ$ (identity component); $\mathcal{B}$ |
| [1768](main.tex#L1768) | Frankle: barrier "only for $k>0$" (**reversed**) | barrier for small $k$, incl. $k=0$; short shared training suffices (paper: unstable at init, stable early) |
| [1864](main.tex#L1864) | Path-SGD $\gamma_p$: "norm of the path vector restricted to paths through $e$" | with $w_e$ removed from each product (otherwise not rescaling-invariant) |
| [1902](main.tex#L1902) | SynFlow per-edge score $\langle\partial L/\partial\theta,\theta\rangle$ (a scalar) | $\partial\mathcal{L}/\partial\theta\odot\theta$ |
| [1935](main.tex#L1935) | multi-head group $S_h\times GL^h\times GL^h$ | $\rtimes$ (see A14) |
| [2086](main.tex#L2086) | Lenc ratio subtracts a matrix $e_{ii}$ from a row | $e_i^\top$ |
| [2185](main.tex#L2185) | Nyquist $f_s>f_{\max}$ | $f_s>2f_{\max}$ |
| [2187](main.tex#L2187) | "$k(Gx)$ representing the best choice on $Gx$" | total dissent: mass of the orbit off its majority label; fundamental domain defined |
| [2197](main.tex#L2197) | obstruction iff $\operatorname{Stab}(f^*(x))\subsetneq\operatorname{Stab}(x)$ | iff $\operatorname{Stab}(x)\not\subseteq\operatorname{Stab}(f^*(x))$ (⊊ is one case) |
| [2212](main.tex#L2212) | "proving the bound: $R(f)-R(\bar f)=\dots$" | an identity |
| [2214](main.tex#L2214) | "exactly $H$-equivariant provided $h_\theta$ injective" | $H$-equivariant always; injectivity rules out larger groups |
| [2266](main.tex#L2266) | entropic term $S=-\tfrac14\mathbb{E}\lVert\cdot\rVert^2$ | $+\tfrac14$ (Ziyin et al. 2025a, Eq. 3, checked in `raw/`) |
| [2270](main.tex#L2270) | "$G$-symmetric state is the fixed set of $P_G$" (vs. §4 def. $G_\theta\neq\{e\}$) | for a finite subgroup $G$ (e.g. a transposition), the states with $G_\theta\supseteq G$; $P_G$ = Reynolds operator |
| [2272](main.tex#L2272) | $\Delta^G$ for the pair $(i,j)$ $=\lVert\theta_i-\theta_j\rVert^2$ | $\tfrac12\lVert\theta_i-\theta_j\rVert^2$, since $\theta-P_G\theta$ splits the difference in halves |
| [2274](main.tex#L2274), [2327](main.tex#L2327) | $S_p\times S_q$ maximal in $S_d$ | only for $p\neq q$ ($S_p\times S_p<S_p\wr S_2$) |
| [2317](main.tex#L2317) | Otto: sentence without a verb | nuclear norm of $A\mapsto\mathcal{L}_Af$ as a convex surrogate of its rank |
| [2335](main.tex#L2335) | partial equivariance (exact on $S$) "corresponds to $\operatorname{Stab}_\epsilon(f)$ with $\epsilon>0$" | $S\subseteq\operatorname{Stab}_0(f)$; approximate version $\operatorname{Stab}_\epsilon$ |
| [2369](main.tex#L2369) | duplication: outgoing columns sum to $\boldsymbol 1$ | sum to the original column |
| [2389](main.tex#L2389) | $\lVert f\rVert_{\mathrm{EE}}$ "recovered by the formulation … used in the introduction" | equals $\sup_g\operatorname{ee}(f,g)$ (start of §6) when $\rho_Y$ acts by isometries |
| [2408](main.tex#L2408) | Ali: "$\dim E_\theta(O_x)=|O_x|$"; unspecified $\tilde\rho$ | embedded orbit spans a $|G\cdot x|$-dim subspace; restriction $\cong\rho_{\mathrm{reg}}$ |
| [2410](main.tex#L2410), [2418](main.tex#L2418) | wrong cross-refs (self-reference to §6.3; FA is not in auto-DA) | §6 intro; §3.2.3 |
| [2429](main.tex#L2429) | RPP: $f=f_e+\theta Wx$ then "$W=A+B$" (two decompositions mixed; $\theta$ = parameters) | $\gamma Wx$; RPP layers $A+B$, $A=Q\beta$ with $Q$ a basis of solutions of Eq. linear-equivariance |
| [2437](main.tex#L2437) | "LLLC" | LRLC (paper's name) |

### B2. Notation aligned with notation.md

- `\ref`, `\cref`, `\labelcref` replaced by `\Cref` (13 places; e.g. L234, L538, L542, L547, L852, L1007, L1045, L1118, L1187, L1213, L1578).
- $\theta$ used as an angle replaced by $\alpha$: L332, L507, Mesh CNN L680–683, Augerino L2346.
- $\phi$-equivalence uses $x,x'\in\mathcal{X}$, not $y$ (L263).
- Observational-equivalence example: $\mathcal{Y}=\mathcal{F}$ (was "hypothesis space"), $\phi=\varphi:\theta\mapsto f_\theta$, with a reference to Eq. implementation-map (L285).
- Starred symbols: ground truth uses $^*$ ($Q^*,\sigma^*,M^*,V^*$); $w^\star$ became $\theta_1,\theta_2$ (L874); $L^\star$ became $L_{\mathrm{PIT}}$ (L1056).
- Indicators: `\mathbb{1}` and `\mathbb{I}` became `\boldsymbol{1}` (L1535, L2261). `\mathbb{1}` does not render properly with amssymb.
- $\mathcal{W}_1$ became $W_1$, as in §3.1 (L2225–2226).
- $\mathcal{D}$ is kept for datasets only. SimSiam distance became $d$ (L969); MoE output became $f$ (L1264); plain $D$ datasets became $\mathcal{D}$ (L2065, L2094, L2101, L2325).
- $\mathcal{H}$ is kept for the hypothesis class. Nurisso's invariant sets became $\Theta(c)$, $\Theta_\Gamma(c)$, and the DAG $G$ became $\Gamma$ (L1544–1550, L1903–1904).
- $G$ is kept for groups:
  - Kristiadi metric matrix → $M$ (L1813, L1867);
  - Simsek's counts $G(r,m),T(r^*,m)$ → $N_{\mathrm{sym}},N_{\min}$ (L1630);
  - Goodfellow's firing rate $G(i)$ → $r_{\mathrm{glob}}$ (L2080);
  - Worrall's blur kernel $G_A$ → $k_A$ (L2359);
  - the chain $G_0\ge G_1$ → $G^{(0)}\ge G^{(1)}$ (L2313), which otherwise reads like stabilizers.
- $g$ is kept for group elements:
  - Riemannian metric $g_w$ → $\langle\cdot,\cdot\rangle_w$ (L1661);
  - minimality's $g_\eta$ → $\tilde f$ (L1326);
  - hypernetwork $g$ → $\Psi$ (L1941);
  - Jacot's inner map $g$ → $q$, now linked to the quotient map $\pi$ (L2051);
  - spherical filter $h$ → $\kappa$, since $h\in SO(2)$ appears in the same paragraph (L662).
- $\rho$ is kept for representations: $Q_\rho$ → $Q_s$ (L1417–1418); SAM radius $\rho$ → $r$, perturbation $\epsilon$ → $\delta$ ($\epsilon$ = tolerance); ASAM $T_w$ → $T_\theta$ (L1821–1827).
- Losses:
  - per-example $\mathcal{L}_\theta(x_1,x_2)$ → $\ell(x_1,x_2,\theta)$ (L944);
  - gradients of the training loss use $\mathcal{L}$, not $L$ (Armenta L1886, SynFlow L1902, Smidt L2200);
  - $\nabla^2 f$ → $\nabla^2\mathcal{L}$ (L1606);
  - Fan et al.: $\mathcal{L}(\theta)$, $f_\theta$ instead of $NN_\theta$ (L1080).
- MoCo/DINO teacher $\theta_t$ (clashed with $\theta_t$ = step $t$) → $\xi$, as in BYOL (L952, L959, L964, L966).
- Lie algebra bases → $A_i$: LieGAN $L_i$ (L2005), Krippendorf $T^a$ (L2060), LieGG $\mathfrak{h}$ (L2064). Lie derivative $\mathcal{L}_X$ → $\mathcal{L}_A$, linked to §2.5 (L2098). LieSD criterion written with $\partial f$ and $\mathcal{L}_{A_i}f=0$, "for connected $G$" (L2067).
- Indices: batches $m$ → $k$, as in L865 (L884, L887); widths $n_{k\pm1}$ → $d_{l\pm1}$ (L1334–1335); Brea's layer index $k$ → $l$ (L1588–1589).
- Spaces calligraphic, labels plain: Higgins $f:\mathcal{X}\to\mathcal{Z}$, $\mathcal{Z}=\bigoplus\mathcal{Z}_i$ (L2321); Shakerinava $f:\mathcal{X}\to\mathcal{Z}$, $\operatorname{Inv}:\mathcal{Z}^2\to\mathbb{R}$ (L2444); $d_Y$ a distance on $\mathcal{Y}$ (L2387); $\mathcal{X}=\cup_{x\in F}Gx$ (L2187).
- Augmentation sets $\mathcal{A}$ → $\mathcal{T}$ (Gupta L2360–2361, van der Wilk L2440).
- $\mathcal{F}$ is kept for the function space: Zhang's $\widetilde{\mathcal{F}}$ → $\phi$ (L2089); Urbano's Fréchet mean $\mathcal{F}(\mu)$ → $\bar g$ (L2246); NFN's undefined $F_W$ → "any functional $\mathcal{F}\to\mathbb{R}$ of $f_\theta$" (L1923).
- Measurement $\mathcal{M}$ → $m$ ($\mathcal{M}$ is the neuromanifold) (L1712).
- Matrices: LoRA $Z$ → $\Delta W$, as in L1314 (L1868); attention $PW_V$ → $W_OW_V$ (L1313); factorization $(U,V)$ → $(A,B)$, since $U$ is the update map in the same subsection (L1521, L1834–1835).
- Reynolds operator unified as $\mathcal{R}$: defined at L594; $\rho_{\mathrm{avg}}$ → $\mathcal{R}$ (L2189–2190); $P_G$ labelled as the Reynolds operator on $\Theta$ (L2270).
- Smaller renames:
  - $h_\Theta$ → $h_\theta$ (L625);
  - EMD bijection $\phi$ → $\sigma$ with $|S_1|=|S_2|$ (L1084);
  - $O\in O(d)$ → $R\in O(d)$ (L1019);
  - $P$ with $P_c=e_c^\top$ → $P_\sigma$ with $\sigma(c)=c$, the stabilizer of the true class (L1034);
  - $\mathcal{A}\subset\Theta$ → a subset of parameter coordinates (L1414);
  - map on the quotient $\varphi$ → $\tilde\varphi$ (L1668);
  - $\varphi^{-1}(\{\varphi(\theta)\})$ with braces (L2503);
  - $D_k,D,D_A$ → $d_k,d,d_A$ (L1935–1938);
  - `\mathrm` subscripts for $W_{\mathrm{fixed}}$ and $*_{\mathrm{partial}}$;
  - `\operatorname{GL}` → `GL`;
  - Arora: bold $\mathbf{x}$, $N$ → $x$, $L$ (L1875).

### B3. Notions now introduced where they are first used

- Def. Invariance: forward references to Def. Group and Def. Group action (L289).
- $\bar f:\mathcal{X}/G\to\mathcal{Y}$ in the factorization through $\pi$ (L413).
- $\mathfrak{so}(n)$ named as the Lie algebra of $SO(n)$ (L506).
- p4 and p4m (L574).
- Reynolds operator formula (L594).
- $\exp_p$ is the Riemannian exponential map, not the matrix exponential; the gauge constraint is equivalent to Eq. steerable-constraint (L654–655).
- Orbit relation $\sim_G$ (L705).
- Dihedral group $D_n$ (L775).
- $g\cdot\mathcal{D}=\{(g\cdot x_i,y_i)\}$ in the augmented risk (L814).
- Update map $U:\Theta\to\Theta$, $\theta_{t+1}=U(\theta_t)$, at first use (L1117).
- Quiver (L1217).
- $M^\dagger$ as a left inverse (L1329).
- Double rotation (L1420).
- Neuromanifold at first use (L1474).
- 1-form $\xi^\flat=\sum_i\xi_i\,d\theta_i$; Poincaré lemma on $\Theta=\mathbb{R}^n$ (L1504–1505).
- Learning rate $\eta$ and $\lambda_{\max}$ (L1606).
- SLT spelled out at first use (L1595).
- Rescaled weights $v_{ij}^{(l)}$ in Armenta's gradient formula (L1888).
- $\theta^+_v$ incoming weights (L1336, L1707).
- Holonomy group (L2324).
- Passive permutation symmetry (L2393).
- Infinitesimal representation reference (L2434).
- Mutual information (L2460).
- Cramér's V formula, which uses the $r,k$ that were previously defined but unused (L2623).
- BN's $\epsilon$ caveat for $\operatorname{BN}(\lambda Wx)=\operatorname{BN}(Wx)$ (L1291).

### B4. Typos and grammar fixed along the way

- Introduction and §3: there→their (L99); missing period (L140); "both work seek" (L542); generalizes→generalize (L678); comma (L667); "can be take" (L724); missing period (L785); "by theoretical addressing" (L787); "by in" (L837).
- §3.3: sharpening→sharpens (L966); "describing [it]" (L992); calls→call (L1003); "is [to] treat" (L1042).
- §4:
  - obstruction→obstructions (L1196); induces→induce (L1333); ReLu (L1411); "complete ?" (L1422); non-degeneracies (L1440); direction→directions (L1486); seing (L1551); generate→generates (L1604); stabilizes→stabilize (L1607); split→splits (L1638); form→from (L1668);
  - than/networks (L1696); transformers models (L1703); "the the" (L1734); "prevents asymptotically" (L1742); architecture→architectures (L1750); accounts→account (L1778); ViT/language-model (L1784); "measures close" (L1803); implicit→implicitly (L1813); conditionning (L1850); present→presents (L1855); implicitlt (L1867);
  - "as resource … findings" (L1872); "an formalizing" (L1877); teleportating (L1889); "and … :" (L1911); receives→receive (L1928); middleground (L1962).
- §5: "early work extract" (L1993); stray comma (L1998); intepretation (L2044); semicolon (L2049); excites (L2061); misalignement (L2100).
- §6: "an hypothesis" (L2125); duplicated "breaks" (L2157); "can [be] measured" (L2184); overperform and a missing period (L2229); "the another" (L2247); prevent→prevents (L2362); missing period (L2392).
- Discussion and appendices: "explicited" (L2533); "a close calls" (L2602); "choic views" (L2644).
- Missing spaces before `\citep`.

---

## C. Inventory of mathematical notions (reading order)

Status: **OK** = correct, consistent and introduced · **Fixed** = see B · **Decide** = see A.

### §1–2 Introduction, methods, taxonomy
| Notion | Where | Status |
|---|---|---|
| Invariance $f(g\cdot x)=f(x)$, equivariance $f(g\cdot x)=g\cdot f(x)$ (informal) | L105 | OK (formalized in §2) |
| Taxonomy axes and values; $\epsilon$ tolerance; $S\subsetneq G$ | Table 1 | Decide (A1) |
| Loci: $f^*$, $p$, $\mathcal{H}$, $\varphi$, $\mathcal{L}$, $U$, $f_\theta$, $g\cdot\theta=\theta$, $x$, framework | Fig. 1, L175–178 | OK (figure: A9 for $\tau_i$) |
| 17-dim coding vector ($3+2+6+2+2+2$) | L170 | OK (checked) |

### §2 Background
| Notion | Where | Status |
|---|---|---|
| Symmetry / invariance / invariant (informal) | L256–259 | OK |
| $\phi$-equivalence; equivalence classes | Def., L261 | Fixed ($y\to x'$) |
| Examples: segmentation, classification, level sets, observational equivalence | L272–286 | Fixed (labels, $\mathcal{F}$, $\varphi$); A3 for $L$ |
| Invariance | Def., L288 | Fixed (forward refs) |
| Equivariance; $\rho_X,\rho_Y$; $\operatorname{Sym}(\mathcal{S})$; homomorphism condition | Def., L299–325 | OK |
| Symmetry group $\operatorname{Sym}(f)$ is a subgroup | L326 | OK (closure and inverses checked) |
| "One rotation, several forms" ($C_4$) | Ex., L328 | Fixed ($\alpha$); Decide (A2) |
| Invariance as trivial $\rho_Y$ | L339 | Fixed (wording) |
| Group; subgroup; trivial subgroup; homomorphism; isomorphism; automorphism; $\operatorname{Aut}(G)$ | Def., L347–360 | OK |
| Direct and semidirect product | Def., L362 | OK |
| Lie group, dimension, "continuous", compact | L373–375 | OK |
| $C_n$, $GL(n)$, $S_n$ and $P_\sigma$, $O(n)$, $SO(n)$, $E(n)$, $SE(n)$, $(\mathbb{R}_{>0})^d\rtimes S_d$ | Ex., L377 | OK (dimensions $n^2$, $n(n-1)/2$, $n(n+1)/2$ and $\sigma\mapsto P_\sigma$ checked) |
| Group action; $g\cdot x$; actions of $E(n)$ and $S_n$ (points, graphs) | Def., L393–398 | OK |
| Orbit, stabilizer $G_x=\operatorname{Stab}(x)$ | Def., L400 | OK |
| Quotient, quotient map, section, canonicalization; centering example | Def., L408–415 | Fixed ($\bar f$ domain) |
| Orbit–stabilizer theorem; $|G\cdot x|=|G|/|G_x|$; $\dim$ formula; $SO(3)$ on $\mathbb{R}^3$ | Thm., L417–428 | OK (coset space $G/G_x$ is used before $G/H$ is spelled out at L442, minor) |
| Free, faithful, transitive; homogeneous space; $S^2\cong SO(3)/SO(2)$, $\mathbb{R}^n\cong E(n)/O(n)$ | Def., L430–443 | Fixed (quantifier on $x_0$) |
| Linear representation; equivariant linear maps form a subspace | Def., L451–459 | OK |
| Trivial, permutation, regular representations; weight tying $\Lambda_{\sigma(i)\sigma(j)}=\Lambda_{ij}$ | Ex., L461 | OK (checked) |
| Invariant subspace; irreducibility; complete reducibility (compact groups); $S_n$ example | Def., L470–477 | OK |
| Steerable networks, feature field of type $\rho$ | L479–485 | OK |
| Convolution; kernel constraint; isotropic kernels; basis $K=\sum_kw_kK_k$ | Eq. steerable-constraint, L487–494 | OK |
| Matrix Lie groups | L499 | Fixed |
| Lie algebra, Lie bracket, $\exp$, one-parameter subgroup; $\mathfrak{so}(n)$; local $\log$; surjectivity | Def., L501–508 | Fixed (naming, $\alpha$) |
| Infinitesimal representation $d\rho$; infinitesimal generators | Def., L510 | OK |
| Constraint over generators (connected $G$); disconnected groups | Eq. lie-algebra-equivariance, L519–524 | Fixed (count) |
| Lie derivative $\mathcal{L}_Af$; formula for linear actions; $\mathcal{L}_{A_i}f=0$ criterion | L526–531 | OK (formula and criterion checked) |

### §3 Symmetry as a design principle
| Notion | Where | Status |
|---|---|---|
| Domain $\Omega$, signal $x:\Omega\to\mathbb{R}^C$; $\operatorname{Diff}(\Omega)$ | L554–561 | Decide (A4) |
| $G$-CNN: lifting, $G$-convolution $(f\star\kappa)(g)=\sum_hf(h)\kappa(g^{-1}h)$, p4/p4m | L574–581 | OK (equivariance under $\rho_{\mathrm{reg}}$ checked); Fixed (p4) |
| Steerable CNNs; SVD-based EMLP; parameter sharing; Clifford algebras (named) | L583–590 | OK |
| Invariant features; soft penalties; symmetrization; Reynolds operator | L592–594 | Fixed (operator defined) |
| Euclidean groups; irreps, Fourier analysis, tensor products, spherical harmonics | L597–614 | Decide (A5) |
| $S_n$ on sets $X\in\mathbb{R}^{n\times d}$; invariant vs. equivariant | L619 | OK |
| Deep Sets decomposition | L620, L712 | Decide (A6) |
| DGCNN layer; message passing; $S_n$ on $(A,X)$; geometric graphs; TDL complexes (named) | L625–637 | Fixed ($h_\theta$) |
| Frame, gauge, gauge transformation, structure group $H\le GL(d)$, feature type, parallel transport | L642–650 | OK |
| Gauge-equivariant convolution; $\exp_p$; kernel constraint | L652–655 | Fixed (gloss; link to Eq. steerable-constraint, equivalence checked) |
| Spherical convolution (Esteves); zonal filters; $SO(3)$ lift (Cohen) | L661–673 | Fixed (filter $\kappa$) |
| Icosahedral CNN ($H=C_6$); GCN; Mesh-CNN kernel constraints | L675–683 | Fixed ($\alpha_{pq}$, $K_{\mathrm{self}}$) |
| Naturality; $\operatorname{Aut}(\Gamma)\le S_n$ | L686–687 | OK |
| Local canonicalization; $R_i\mapsto R_i\hat R^{-1}$; invariance of $f_i=\rho(R_i)F_i$ | L688–697 | OK (checked); $\mathbb{E}^d$ undefined, minor |
| $C_G(\mathcal{X},\mathcal{Y})$, $\overline{\mathcal{H}}$; representation thms; universality; separation; $\sim_G$ | L703–724 | Fixed (orbits, $\sim_G$, implication) |
| WL hierarchy, $k$-WL, completeness | L725–729 | Decide (A5) |
| Sample-complexity bound in $W_1$; $\operatorname{vol}(\mathcal{X}/G)=\operatorname{vol}(\mathcal{X})/|G|$ | L750–755 | OK (valid for faithful isometric actions on connected $\mathcal{X}$) |
| PAC bound with weight-tying orbits; strict gain (linear); base-space complexity | L759–761 | Fixed (wording) |
| Optimization ease, efficiency gap | L770–771 | OK |
| $D_n$ vs. $C_n$ | L775 | Fixed |
| Augmented risk $\hat R_{\mathrm{aug}}$ | L812–816 | Fixed ($g\cdot\mathcal{D}$) |
| Group-theoretic DA, variance reduction, symmetrization equivalence, PAC-Bayes | L822–828 | OK |
| Feature averaging; DA vs. FA results | L842–846 | Fixed (Lyle) |
| Learning algorithm $\mathcal{A}$; $S_{n_e}$ action; GD $S_n$-invariant; mini-batch $\prod S_B$ | L858–866 | OK |
| Index ratio $n!/(B!)^k\sim(2\pi n)^{(1-k)/2}k^{n+k/2}$ | L867–871 | OK (Stirling checked) |
| Churn; weight distance; subgroup std | L874 | Fixed ($\theta_1,\theta_2$) |
| SS / RR / with-replacement; BN objectives $\mathcal{L}_{\mathrm{GD}},\mathcal{L}_\sigma,\mathcal{L}_{\mathrm{RR}}$ | L879–892 | Fixed ($k$ batches) |
| Floating-point non-associativity remark | L894–897 | OK |
| Exchangeability; empirical measure; Bloem-Reddy representation | L901–903 | OK |
| Invariance in law display | L904–907 | Decide (A7) |
| Curriculum (non-exchangeable) | L910–915 | OK |
| Views, augmentation family $\mathcal{T}$, double symmetry; branch symmetry | L923–938 | Decide (A8) |
| Representational collapse; contrastive / non-contrastive | L940–954 | OK |
| SimCLR loss | L948–950 | Fixed |
| EMA (MoCo, BYOL, DINO); temperatures; stop-gradient; SimSiam loss | L952–972 | Fixed ($\xi$, $d$, item ref); A9 |
| Barlow Twins loss $\lVert I-\mathcal{C}\odot I\rVert_F^2+\lambda\lVert\mathcal{C}\odot(\boldsymbol1\boldsymbol1^\top-I)\rVert_F^2$ | L977–981 | OK (matches $\sum_i(1-\mathcal{C}_{ii})^2+\lambda\sum_{i\ne j}\mathcal{C}_{ij}^2$) |
| VICReg penalty; CLIP symmetric cross-entropy | L982–990 | Fixed ($z^{\mathrm{txt}}$); OK |
| Criterion $L$ vs. loss $\mathcal{L}$; realizable $g$ inducing loss symmetries | L996–997 | OK (implication checked) |
| Invariant criterion; Kaba's invariant loss function | Eq. invariant-loss, L998–1006 | OK |
| Diagonal invariance | Remark, L1008 | Fixed |
| Object-swap example | L1012–1014 | Fixed |
| Prediction-dependent orthogonal action (MSE) | Ex., L1017 | Fixed ($R$) |
| False-class symmetry of CE | Ex., L1027 | Fixed (stabilizer form, checked) |
| Orbit loss $L_{\mathrm{orbit}}=\inf_gL(\hat y,g\cdot y)$; quotient loss | L1042–1049 | OK |
| PIT; deep clustering; prototypes | L1053–1062 | Fixed ($x_k$, $L_{\mathrm{PIT}}$) |
| Slot Attention equivariance; Hungarian matching, $L_{\mathrm{match}}$ | L1065–1076 | OK (the assignment $\hat\sigma=\arg\min_\sigma\sum_iL_{\mathrm{match}}(y_i,\hat y_{\sigma(i)})$ could be written; minor) |
| Chamfer, EMD | L1082–1087 | Fixed (EMD bijection $\sigma$, equal sizes) |
| Gromov–Wasserstein; planted alignment; Ping-Pong | L1093–1100 | Fixed ($Q^*,\sigma^*$) |
| InfoNCE negatives symmetry | Remark, L1102 | OK |

### §4 Parameter space
| Notion | Where | Status |
|---|---|---|
| Implementation map $\varphi$; non-identifiability | Eq. implementation-map, L1111 | OK |
| Three loci; update map $U$ | L1117 | Fixed ($U$ defined) |
| Six classes (1)–(6); $\mathcal{L}_F,\mathcal{L}_R$; $S\subsetneq\mathcal{X}$; $\Theta_0$ | L1133 | Decide (A11) |
| Symmetric state; $G_{g\theta}=gG_\theta g^{-1}$; permutation example | L1139–1143 | OK |
| PS; fiber; observational equivalence; completeness | L1146–1153 | OK |
| LS; Q-symmetries (pointer) | L1155–1160 | OK |
| Hierarchy SS ⇒ PS ⇒⋆ LS | Eq. param-symmetry-hierarchy | OK |
| Loss-level symmetry via regularization | Ex., L1171 | Fixed (ref to Fig. 4 item (2)) |
| False-class loss-level symmetry | Remark, L1179 | Decide (A12) |
| General / instance-level / data-dependent PS ($\Omega(S,V)$, groupoid) | L1190–1210 | OK (data-dependent action checked); A10 for $U,V$ |
| Architectural PS; neuron splitting | L1213–1214 | Fixed |
| Quiver formalism; negative rescaling; argmax error level | L1217–1221 | Fixed |
| Permutation $U\sigma(Vx)=UP^\top\sigma(PVx)$; order $\prod d_l!$ | L1252–1260 | OK; A10 |
| MoE completeness, $G(n)=\mathbb{R}^{d+1}\times S_n$ | L1263–1265 | Fixed (output $f$); direct product correct here (common shift commutes with permutations) |
| Sign flip; order $\prod_l2^{d_l}d_l!$ | L1267–1273 | OK |
| Translation symmetry; softmax shift | L1275–1283 | OK |
| Scale symmetry; BN, IN, LN, GN, WN | L1285–1293 | Fixed (BN $\epsilon$) |
| Rescale symmetry; $(\mathbb{R}_{>0})^{d_l}$; monomial case; lightning attention | L1295–1305 | Fixed (monomial) |
| $GL$ factorization; deep linear; attention; LoRA | L1307–1314 | Fixed ($W_OW_V$); LoRA invariance checked |
| $O(k)$ residue of $GL(k)$ under $L_2$; dynamic word embeddings; radial activations | L1316–1322 | OK (checked) |
| Minimality; Fisher information criterion; width-changing maps, $M^\dagger$; duplication; 0-type neurons; groupoid; instance symmetries | L1325–1337 | Fixed ($\tilde f$, $M^\dagger$, $d_l$, $\theta^+_v$) |
| Depth remark | Remark, L1339 | Fixed |
| Double-entry table | Table 4 | Decide (A13) |
| Intertwiner group $G_{\sigma_n}$ | L1406–1411 | Fixed (wording) |
| Kunin's $\psi(\theta,\alpha)$; O-mirror symmetry; Q-symmetry; exponential symmetries | L1413–1420 | Fixed ($\mathcal{A}$, $Q_s$, list, double rotation) |
| Identifiability up to $G$: $\varphi^{-1}(\{\varphi(\theta)\})=G\cdot\theta$ | L1423–1426 | OK |
| Sigmoidal results; Fukumizu local criterion | L1432–1434 | OK |
| Bent hyperplanes; Rolnick; Phuong formula $W^\eta_l=D_lP_lW^\theta_lP_{l-1}^{-1}D_{l-1}^{-1}$ | L1437–1444 | OK (formula checked) |
| Hidden symmetries, never co-active pairs; Grigsby; Gegenfurtner | L1448–1458 | Fixed (local perturbation) |
| Functional dimension $\dim_{\mathrm{fun}}=\sup_Z\operatorname{rank}\partial E_Z$; expected functional dimension | L1462–1469 | OK |
| Lightning attention fibers; neuromanifold; FI; local-to-global; polynomial activations; subnetworks | L1472–1481 | Fixed (neuromanifold, FI) |
| Conserved function; generator $\xi$; orthogonality to the flow | L1491–1502 | OK (checked) |
| Gradient generator; $\xi^\flat$; Poincaré lemma; symmetric Jacobian; Kunin's examples | L1503–1510 | Fixed (gloss, $\Theta=\mathbb{R}^n$); examples checked (scale law up to a factor $\tfrac12$) |
| Saxe hyperbola; Tarmoun rate; Du balancedness; ReLU balance law | L1516–1523 | Fixed (Du) |
| Flow field $W(\theta)$; Lie algebra of the flow field; ResNets / Transformers | L1527–1530 | Decide (A21) |
| Weight-decay decay law $e^{-\lambda t}c$; drift $O(\eta^2k)$; weight-balancing flow; noise equilibria | L1535–1540 | Fixed ($\boldsymbol1$, $\eta$); law checked |
| Invariant set $\Theta(c)$, hyperquadrics, $2^{l_-}$ components; DAG version; CQ as coordinates | L1544–1552 | Fixed ($\Theta(c)$); component count checked |
| Data-induced CL; flow-field shrinkage; tensorizable networks | L1556–1562 | OK |
| Lifted dynamics; intrinsic recoverability $\ker\partial\phi\cap\ker\partial h=\{0\}$ | L1566–1572 | OK ("equivalent" holds locally) |
| Li et al.: fixed points are critical; $T_x(G\cdot x)\subseteq\operatorname{Null}\nabla^2f$ | L1581–1586 | Fixed ($g\cdot x$); checked for linear actions |
| Permutation points; plateau of dimension $d_{l+1}$ | L1587–1589 | Fixed |
| Linear autoencoder critical points | L1590–1591 | Fixed |
| Invariant set of SGD; approximately $Q$-symmetric; sign and permutation invariant sets; mirror attractivity; SB distance | L1596–1601 | OK |
| Scale invariance with weight decay; $\nabla^2\mathcal{L}(\alpha\theta)=\alpha^{-2}\nabla^2\mathcal{L}(\theta)$; effective learning rate; spherical sharpness | L1604–1611 | Fixed ($\mathcal{L}$, $\eta$) |
| Kobayashi bound; $A^\top A-B^\top B$ conserved and decaying under weight decay; pseudo rank | L1612–1619 | OK (conservation and exponential decay checked) |
| Modified flow $\tfrac\eta2\ddot\theta+\dot\theta=-\nabla\mathcal{L}$ | L1622 | OK |
| Simsek counts; pseudo-determinant | L1629–1632 | Fixed ($N_{\mathrm{sym}},N_{\min}$) |
| Orbit relation; quotient / representative / alignment | L1647–1652 | Fixed (orbit) |
| Basis paths ($m-H$); PSI manifold and metric; Grassmannian; quotient realization map | L1655–1668 | Fixed; A22 |
| Hecht-Nielsen cone; minimal search set | L1671–1672 | Decide (A23) |
| Oblique manifold; projection; Equi-normalization; Saul's balancing factor | L1675–1692 | Fixed (Equi-normalization) |
| Stitching; $G_{\mathrm{ReLU}}$-Procrustes $\mu(X,Y)\in[0,1]$ | L1696–1701 | OK (range checked) |
| Double rotation alignment; product-of-spheres alignment | L1703–1708 | Fixed (gloss, $\theta^+_v$) |
| Measurements factoring through $\Theta/\!\sim$ or $\mathcal{F}$ | L1711–1713 | Fixed ($m$) |
| Fisher–Rao norm; minima-manifold curvature | Remark, L1716 | OK ($I(\theta)$: A27) |
| Path height $\mathcal{B}$; $G^\circ$-invariance | Eq. barrier-height, L1729–1738 | Fixed ($\inf$, $G^\circ$, $\mathcal{B}$); argument checked |
| Sublevel sets; Freeman–Bruna bound; Tatro; Brea paths | L1741–1757 | OK |
| Linear networks: $\mathcal{L}^{-1}(0)\cong GL(h)^{L-1}$, $2^{L-1}$ components | L1758–1759 | OK (checked) |
| Linear barrier $B$ | Eq. linear-barrier | OK |
| Frankle; asymmetric networks; Entezari; Ainsworth; Zhao counterexample; MoE translation invariance of $B$ | L1767–1784 | Fixed (Frankle); translation invariance checked |
| Variance collapse, REPAIR | Remark | OK |
| Flatness; Dinh bound $\lVert\nabla^2\mathcal{L}(T_\alpha\theta)\rVert_F\ge\alpha^{-2}\gamma$ | Eq. dinh-hessian-bound | OK (holds for $\gamma$ taken in the first-layer block) |
| Normalized sharpness; spherical sharpness; invariant Hessian $E=M^{-1}H$; Petzka | L1803–1817 | Fixed ($M$); scale invariance of normalized sharpness checked |
| SAM; ASAM | L1819–1827 | Fixed (renames) |
| Matrix-factorization obstacle; Goldstone GD | L1834–1839 | Fixed ($A,B$); A20 |
| Equivariant update; invariances of GD, Newton, NGD, Adam; scale-freeness; AdamW | Eq. equivariant-optimizer, L1841–1850 | OK |
| Equivariant optimizers ⇒ $\theta_0\sim\tilde\theta_0\Rightarrow\theta_t\sim\tilde\theta_t$ | L1853–1855 | OK (checked) |
| Path vector $\pi(w)$; Path-SGD; reparametrizations vs. weight-space symmetries; explicit metric | L1858–1867 | Fixed ($\gamma_p$, $M(\theta)$) |
| LoRA optimizer equivariance; right preconditioner | L1868–1869 | Fixed ($\Delta W$) |
| Depth as preconditioner; saddle-to-saddle | L1875–1879 | Fixed (notation) |
| Teleportation; gradient transformation $J^{-\top}\nabla\mathcal{L}$; Newton link | L1882–1897 | Fixed ($\mathcal{L}$, $v_{ij}$); criterion checked ($\nabla\mathcal{L}(gw)=J^{-\top}\nabla\mathcal{L}(w)$) |
| SynFlow; singular pruning, $J_\Gamma$ | L1901–1904 | Fixed |
| Metanetworks; $\Theta=\mathcal{W}\oplus\mathcal{B}$; DWS block structure; expressivity | L1910–1925 | Fixed (functional) |
| Rescaling-equivariant message | L1931 | OK |
| Multi-head symmetry group; Transformer-NFN | L1935–1938 | Fixed; A14 |
| Hypernetworks | L1941–1942 | Fixed ($\Psi$) |
| SLT, RLCT, LLC, $V(\epsilon)\propto\epsilon^{\lambda}$; neuroalgebraic geometry | L1945–1961 | OK (general form has a $\log$ factor; "in simple cases" covers it) |

### §5 Symmetry discovery
| Notion | Where | Status |
|---|---|---|
| Discovery triple $(G,\rho_X,\rho_Y)$; joint action on $(x,y)$; $p\circ g^{-1}=p$ vs. equivariance of $f^*$ | L1967–1988 | OK |
| Combinatorial search; Cayley tables; Lie-algebra parametrization | L1998–2001 | Fixed (comma); Cayley table named only |
| LieGAN basis | L2005 | Fixed ($A_i$) |
| Irreps learning; toroidal subgroups; LieDetect ($T^d$, $SU(2)$ named) | L2008–2011 | Fixed (toroidal) |
| Parameter-sharing reparametrization $\mathrm{vec}(W)=Uv$ | L2015 | OK |
| Krippendorf; invariant GP kernel; L-conv; Noether-based discovery | L2020–2024 | OK |
| Circuits; decodability; NTK vs. feature learning; $\epsilon_s$ | L2043–2049 | OK ($\epsilon_s$ and the regimes are named, not defined; minor) |
| Compositions $h\circ q$, $q\approx\pi$ | L2051 | Fixed |
| Orbit clustering probe; generators by regression | L2058–2060 | Fixed (orbits, $A_a$) |
| LieGG criterion; polarization matrix; nullspace | L2064–2066 | Fixed ($A$, $\mathcal{D}$, link to the Lie derivative) |
| LieSD criterion | L2067 | Fixed (connected $G$, $\partial f$, $d\rho_Y=0$) |
| Goodfellow score; Lenc map $M_g$ and ratio | L2080–2087 | Fixed ($r_{\mathrm{loc}},r_{\mathrm{glob}}$, $e_i^\top$) |
| Internal feature distance; prediction gap; invariance error; $DI_f$; Cohen's equivariance error; Shen's share | L2089–2096 | Fixed ($\phi$, $\mathcal{D}$) |
| Lie derivative (Gruver); invariance energy; symmetry variance; space and orthogonality errors | L2098–2104 | Fixed ($\mathcal{L}_A$, $\mathcal{D}$, $V^*$, $k$) |

### §6 Incomplete symmetries
| Notion | Where | Status |
|---|---|---|
| Per-element error $\operatorname{ee}(f,g)$; $\operatorname{Stab}_\epsilon(f)$, $\operatorname{Stab}_\epsilon(\mathcal{H})$ | L2117–2125 | OK (consistent with notation.md) |
| Exactness as an algebraic criterion | L2126 | Decide (A15) |
| Exactness figure | Fig. 5 | Decide (A16) |
| SB types (functional, distributional, dynamical) | L2146–2151, Table 6 | OK |
| Correct / incorrect / extrinsic equivariance | L2154–2155 | OK |
| Functional SB definition | L2181–2183 | OK; A25 |
| Aliasing (Nyquist) | L2185 | Fixed |
| Error lower bound; total dissent; fundamental domain | L2187 | Fixed |
| Reynolds readout | L2189–2190 | Fixed ($\mathcal{R}$) |
| Curie's principle $\operatorname{Stab}(x)\subseteq\operatorname{Stab}(f(x))$; obstruction | L2195–2197 | OK (proof checked); Fixed (obstruction) |
| Order parameters; relaxed $G$-conv diagnostic; equivariant conditional distributions | L2199–2204 | Fixed ($\mathcal{L}$) |
| Input injection, $\operatorname{Stab}(v)$ | L2207 | OK |
| Joint equivariance; risk identity | L2210–2213 | Fixed (identity); A18 |
| Subgroup selection (Goel) | L2214 | Fixed |
| Distributional SB; canonicalized-input example | L2218–2223 | OK |
| Ridge-regression result; approximate distributional invariance $X\approx_dgX$ with $W_1$ | L2225–2226 | Fixed ($W_1$) |
| Pose entropy | L2227 | Fixed |
| Symmetry-bias metric $m(p_X)$; symmetrization $\bar p_X$ | L2234–2236 | OK |
| Task-useful metric | L2238–2240 | Decide (A17) |
| Canonicalization as a Dirac limit; Fréchet mean | L2245–2247 | Fixed ($\bar g$) |
| Spontaneous SB; modified flow; Lagrangian kinetic SB | L2259–2265 | OK (Lagrangian $\mathfrak{L}$ in fraktur, minor) |
| Entropic loss | L2266–2267 | Fixed (sign) |
| Mirror attractivity; $P_G$; $\Delta^G$ | L2269–2273 | Fixed |
| Least symmetry breaking | L2274 | Fixed ($p\neq q$); A19 |
| syre | L2277 | OK |
| Extent restriction; structures table; $\pm90^\circ$ example | L2282–2303 | Decide (A1) |
| Subgroup injection; depthwise chain; restriction of steerable bases; symmetry promotion | L2312–2318 | Fixed ($G^{(l)}$, Otto) |
| Disentanglement (Higgins) | L2321 | Fixed (spaces) |
| Quessard; GEOMANCER, holonomy; Shakerinava objective | L2323–2325 | Fixed (holonomy, $\mathcal{D}_i$) |
| Partial equivariance; non-iterability; Petrache link | L2332–2338 | Fixed (Petrache) |
| Partial group convolution | L2342 | Fixed (subscript); $E_\epsilon$: A24 |
| Augerino; GP range; class-pose range | L2346–2349 | Fixed ($\alpha$) |
| Semigroups; semigroup correlation; scale-space action | L2353–2359 | Fixed ($k_A$, "semigroup element") |
| CARE on semigroups; orbits in semigroups | L2360–2362 | Fixed ($\mathcal{T}$) |
| Groupoid definition; overparametrization groupoid; duplication example | L2364–2369 | Fixed (example) |
| $\epsilon$-approximate equivariance $\lVert f\rVert_{\mathrm{EE}}\le\epsilon$ | Eq. equiv-error-approximate | Fixed ($\mathcal{Y}$, link to $\operatorname{ee}$) |
| Insensitivity; approximate graph symmetry group | L2390–2393 | Fixed ($\delta$, passive gloss) |
| Relaxed architectures vs. soft penalties | L2399–2402 | OK |
| Wang's error bound; Ali's regular representation | L2407–2408 | Fixed (Ali) |
| Train/test tolerance; projection | L2418–2420 | Fixed (ref) |
| Relaxed group/steerable convolutions | L2423–2427 | OK |
| RPP; Lie-derivative penalty $\mathcal{L}_{A_i}(W)$ | L2429–2435 | Fixed; formula consistent with §2.5 |
| LRLC | L2437–2438 | Fixed |
| Invariant GP kernel | L2440 | Fixed ($\mathcal{T}(x)$) |
| Symmetry regularization via invariants; CARE loss; equivariance loss; presentation penalty | L2444–2450 | Fixed (spaces, $\operatorname{Inv}$) |

### §7 Discussion and appendices
| Notion | Where | Status |
|---|---|---|
| Label-dependent extent; class–pose split, $I(Z_\perp;Y)=0$ | L2458–2461 | Fixed (MI) |
| FedAvg relabeling invariance; $\phi$-equivalence reuse in NLP | L2467–2472 | OK |
| Identifiability gap $\varphi^{-1}(\{\varphi(\theta)\})\subseteq G\cdot\theta$ | L2503 | Fixed (braces) |
| Discretization gap | L2517 | Fixed ($\lVert f\rVert_{\mathrm{EE}}$) |
| Parameter-space equivariance $f_{\alpha\theta}=\alpha^Lf_\theta$ | L2520 | OK (bias-free, $L$ weight layers) |
| $B\subseteq B'\Rightarrow S_{B'}(\theta)\subseteq S_B(\theta)$ | L2523 | OK |
| Coding: NA rate $165/2448=6.7\%$; agreement $58/62=93.5\%$; $303/372=81.5\%$; $\binom62=15$ pairs | App. B | OK (all checked) |
| Cramér's V | L2623 | Fixed (defined) |
| Segment and choice views $\bar q_{s,c}(v)$ | App. B.3 | OK |
| Lift $L_{ab}=n_{ab}/E_{ab}$ | App. C | OK ($L$ reuse is local) |
