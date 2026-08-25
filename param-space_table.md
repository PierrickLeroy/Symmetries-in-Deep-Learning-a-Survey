Data for double entry table (component x symmetry type):
- [godfrey2022] ReLU: rescale permute, Leaky ReLU: rescale permute, RBF: permute flip sign (diag with $\pm 1$ entries), polynomial: permute rescale, linear: GL, sigmoid: permute, CNN: permute on filters
- [jacot2022] linear networks, rotation, overparametrization by 0 neurons/inclusion map into a bigger architecture with 0 neurons appended
- [hecht-nielsen1990anc] permutation
- [fukumizu1996nn] overparametrization, minimality is a form of non-redundance
- [phuong2019,bona-pellissier2023] for non-increasing dimension ReLU nets rescaling and permutation are the only general symmetries
- [rolnick2020p3icml] ReLU permutation rescale recoverability for connected boundaries that intersect all previous layer boundaries + hidden symmetry when $z'$ is inactive whenever $z$ is active, $\theta_{zz'}$ can move freely
- [elisendagrigsby2025aim] ReLU nets, permutation and rescalings
- [fefferman1993anips] tanh
- [grillo2026] ReLU permutation rescaling
- [gegenfurtner2026] ReLU symmetries on non-negative orthant (discrete + continuous) and symmetries due to layer composition (continuous + discrete in a special case) -> these are new symmetries
- [saxe2014piclr2] linear networks: scaling, orthogonal and $GL(n)$
- [neyshabur2015anips] relu rescale
- [salimans2016anips] the proposed weight normalization introduces a scale symmetry
- [dinh2017] ReLU rescaling
- [freeman2017] ReLU permutation rescaling
- [huang2017] batchnorm scale; ReLU rescale
- [arora2018p3icml] GL sym of linear nets
- [bamler2018p3icml] word embedding; rotation
- [li2018] rotation matrix factorization
- [badrinarayanan2015] batchnorm scale oblique manifold, relu rescale
- [wu2018a] group normalization, scale
- [brea2019] permutation, overparametrization
- [kunin2019p3icml] GL(n) symm linear nets -> O(n) symm regularized linear nets
- [liang2019pticais] relu rescaling
- [meng2019] relu rescaling
- [tsuzuku2019] relu rescaling
- [yi2019] relu rescaling
- [kunin2020] rescaling, scaling, translation
- [tatro2020] neuron permutation
- [armenta2021a] quiver nn multiple symmetries permutation scale rescale, activation symmetry, cross-architectural
- [armenta2021b] ReLU rescaling batchnorm
- [kwon2021p3icml] ReLU rescaling
- [petzka2021anips] ReLU rescaling
- [simsek2021] permutation, overparametrization same input neuron summing to 1 or 0 output neurons
- [tanaka2021] homogeneous rescaling, scaling in batchnorm groupnorm layernorm, translation softmax/CE, rotation in word embedding
- [entezari2022] permutation of units: neuron and cnn filters
- [pittorino2022jsm] CNN and ReLU: scale and permutation, argmax: translation and scaling in last layer (doesn't change the ranking)
- [zhuang2022tmlr] AdamW scale
- [yi2022ptcuai] BN scale
- [ainsworth2023] permutation cnn mlp
- [grigsby2023p4icml] hidden symmetries of ReLU nets; (i) stably unactivated neuron (mostly for neuron beyond second layer): change each parameter but conserve sign (ii) never co-activated neurons: fully arbitrary weight between them (iii) multiple linear region are collapsed: depends (iv) positive codimension layer map: rotation at each next layer neuron (maybe the degree of freedom scale with codimension)
- [jordan2023] permutation cnn mlp, batchnorm scaling
- [lyu2023] scale normalization layers
- [navon2023p4icml] permutation symmetry of MLP (metanetwork context) 
- [saul2023] rescaling relu
- [zhao2023] leaky relu rescaling
- [zhao2023a] data dependent symmetry MLP, radial activation orthogonal
- [chen2024jsm] permutation neuron cnn filters
- [kalogeropoulos2024] rescale ReLU, sign flip tanh sine
- [kobayashi2024anips] low rank, rotation, self-attention 
- [lim2024] relu rescaling, permutation MLP
- [nurisso2024a] relu rescaling, permutation shallow MLP
- [zhao2024] Leaky ReLU rescaling
- [ziyin2024a] exponential symmetries (rescale, scale, double rotation)
- [henry2025] polynomial networks (lightning self attention); GL sym as attention, another between layer GL sym and a within-layer scaling symmetry
- [tran2025anips] permutation MoE, translation softmax
- [zhao2025a] linear networks GL, relu rescale
- [usevich2025] polynomial NN scaling (careful: $\sigma(\alpha x)=\alpha^r\sigma(x)$)
- [zhang2025p4icml] double rotation sym self-attention, permutation feedforward, rescaling self-attention
- [nurisso2025] relu rescale feedforward
- [ziyin2025a] K invariance (cts Lie group symmetry), exponential, scale rescale rotation orthogonal
- [ziyin2025] translation scaling rescaling rotation permutation double rotation sign flip
- [li2020anips] batchnorm scale invariance
- [yen2025iclr] LoRA GL
- [sareen2026] overparametrization cross architectural by inclusion (splitting)
- [tran2025iclr]: multi-head attention permutation GL + transformers permutation 
- [ziyin2024]: rotation permutation sign-flip

| Component \ Symmetry Type | Permutation | Rescaling | Sign Flip | Scale | Translation | Orthogonal | $GL(n)$ | Cross-Architectural | Data-dependent | Instance/Hidden |
|---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Feedforward networks** | [hecht-nielsen1990anc], [brea2019], [tatro2020], [entezari2022], [ainsworth2023], [jordan2023], [navon2023p4icml], [chen2024jsm], [lim2024], [nurisso2024a], [kalogeropoulos2024], [simsek2021], [zhang2025p4icml], [ziyin2025], [godfrey2022], [ziyin2024] | [ziyin2024a], [ziyin2025a], [ziyin2025] | [ziyin2025], [ziyin2024] |  [ziyin2024a], [ziyin2025a], [ziyin2025] |  [ziyin2025], |  [ziyin2024a], [ziyin2025a], [ziyin2025], [ziyin2024] | | [fukumizu1996nn] | [zhao2023a] | |
| **Transformers** | [zhang2025p4icml], [tran2025iclr] | | | |  | [zhang2025p4icml], [kobayashi2024anips] | [henry2025], [kobayashi2024anips] | | | |
| **Multi-heads Attention** | [tran2025iclr] | | | | | [zhang2025p4icml] (per head) | [tran2025iclr] | | | |
| **Self-Attention** | | [zhang2025p4icml] | | | | [zhang2025p4icml], [kobayashi2024anips], [ziyin2024a], [ziyin2025] (double rotation) | [kobayashi2024anips] | | | |
| **Lightning Self-Attention** | | | | [henry2025] (within-layer) | | | [henry2025] (also between-layer) | | | |
| **LoRA** | | | | | | | [yen2025iclr] | | | |
| **BatchNorm** | | | | [badrinarayanan2015], [huang2017], [kunin2020], [li2020anips], [armenta2021b], [tanaka2021], [yi2022ptcuai], [jordan2023], [lyu2023], [ziyin2024a] | | | | | | |
| **BatchNorm variants** | | | | [wu2018a] (GN,LN,IN), [kunin2020] (LN,WN), [lyu2023] (LN), [ziyin2024a] (LN), [li2020anips] (GN,WN), [salimans2016anips] (WN), [tanaka2021] (GN,LN) | | | | | | |
| **Softmax/Cross Entropy** | | | | | [kunin2020], [tanaka2021], [tran2025anips], [ziyin2025] | | | | | |
| **Linear networks** | | | | [saxe2014piclr2] | | [jacot2022], [saxe2014piclr2], [li2018], [kunin2019p3icml], [ziyin2024a] | [godfrey2022], [saxe2014piclr2], [arora2018p3icml], [kunin2019p3icml], [zhao2025a] | [jacot2022] | | |
| **ReLU networks** | [godfrey2022], [phuong2019], [bona-pellissier2023], [freeman2017], [pittorino2022jsm], [lim2024], [nurisso2024a], [elisendagrigsby2025aim], [grillo2026], [gegenfurtner2026], [rolnick2020p3icml] | [rolnick2020p3icml], [godfrey2022], [phuong2019], [bona-pellissier2023], [neyshabur2015anips], [dinh2017], [freeman2017], [huang2017], [badrinarayanan2015], [liang2019pticais], [meng2019], [tsuzuku2019], [yi2019], [kunin2020], [armenta2021b], [kwon2021p3icml], [petzka2021anips], [pittorino2022jsm], [saul2023], [zhao2023], [kalogeropoulos2024], [lim2024], [nurisso2024a], [zhao2024], [elisendagrigsby2025aim], [zhao2025a], [nurisso2025], [ziyin2025], [grillo2026], [gegenfurtner2026] | | | | | | | | [rolnick2020p3icml], [grigsby2023p4icml], [gegenfurtner2026] |
| **Homogeneous activation** | [godfrey2022] (leaky ReLU), [tanaka2021] | [godfrey2022] (leaky ReLU), [kunin2020], [saul2023], [zhao2023], [zhao2024], [kalogeropoulos2024], [nurisso2025], [usevich2025] ($\sigma(\alpha x)=\alpha^{r}\sigma(x)$) | | | | | | | | |
| **Polynomial activation** | [godfrey2022], [usevich2025] | [godfrey2022], [usevich2025] | | [henry2025] | | | [henry2025] | | | |
| **Tanh, odd activation** | [fefferman1993anips] | | [fefferman1993anips], [kalogeropoulos2024] | | | | | | | |
| **Radial activation** | [godfrey2022] | | [godfrey2022] (diagonal with $\pm1$ entries) | | | [zhao2023a] | | | | |
| **Mixture-of-Experts** | [tran2025anips] (experts) | | | | [tran2025anips] (gating params) | | | | | |
| **Quiver NN** | [armenta2021a] | [armenta2021a], [saul2023] (DAG), [nurisso2025] (DAG) | | [armenta2021a] | | | | [armenta2021a] | | |
| **Word embedding** | | | | | | [bamler2018p3icml], [tanaka2021] | | | | |
| **Overparametrization by width** | | | | | [brea2019], [simsek2021] | | | [fukumizu1996nn], [jacot2022], [simsek2021], [sareen2026] | | |
| **CNN filters** | [godfrey2022], [entezari2022], [pittorino2022jsm], [ainsworth2023], [jordan2023], [chen2024jsm] | [pittorino2022jsm] | | | | | | | | |
| **Classification error (argmax)** | | | | [pittorino2022jsm] | [pittorino2022jsm] | | | | | |
| **Optimizers** | [yang2025] | [neyshabur2015anips], [meng2019], [huang2017] | | [zhuang2022tmlr], [badrinarayanan2015], [kingma2015], [yi2022ptcuai] | | [bamler2018p3icml] | [amari1998nc], [zhao2023], [zhao2024], [yen2025iclr], [kristiadi2023anips]| | | |

## Caption
- Batchnorm variants: InstanceNorm(IN), LayerNorm (LN), GroupNorm (GN), WeightNorm (WN).
- Cross architectural: inclusion into a wider architecture
- Optimizers: the cell records symmetries interacting with the *training algorithm*, not symmetries of the network function itself.
- Some components are included in others and similarly for symmetry types. We tried to place works depending on what their content highlights. Works can appear in multiple cells.