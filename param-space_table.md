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