# Decision tree / pipeline for when and how to reason with a symmetry
A decision tree/sequence of steps to guide the exploration phase when encountering a symmetry.

A progression in steps:
1. Entry point: what triggers the fact of reasoning about symmetry?
2. Locate: find the symmetry locus
3. Characterize: describe the symmetry and its properties
4. Act: what do we want to do; Locate and Characterize steps should orient us
5. Diagnose: if something goes wrong, how do we catch it?

In the figure, steps 2-4 could be represented from left to right.
I am not sure step 1 and 5 should be diagrammatically represented.
Loci should be indicated in 2., and segments (sections, subsections, subsubsections, paragraphs) as tag when they apply.

## Entry points

- A symmetry is mentioned
- A symmetry is hypothesized
- A symmetry is suspected

## Locate
Goal: describes how to pick the box in \Cref{fig:sym-loci}.
It should consists of a (mini) decision tree to identify the locus and answer the question: of which map $f$ is the symmetry a property of?

1. A natural first step is to ask: can it be conceived without any reference to a model/architecture (problem, data)? If not, is it the model per-se (model, optimization, parameter) or is it about how the model is deployed (framework)?
    1. To separate (problem, data): data is about a single point, it is a symmetry in the strong meaning of \Cref{sec:what-is-sym}. Problem involves either a task relating two spaces through a ground-truth/target map $f^*:\mathcal{X}\to \mathcal{Y}$ or multiple point/the data distribution $p$.
    2. To separate (model, optimization, parameter), parameter involves a fixed parameter and is not true in general and symmetric state is the strong sense of \Cref{sec:what-is-sym} again but about the parameter vector; model is about the class of models and its loci (hypothesis space, implementation map) are distinguish by whether it is about a task or the representation of the model; optimization involves an objective, the optimizer involves the update rule and timesteps.
    3. The framework locus is diverse.

Now, it should be possible to attempt writing the domain and codomain of $f$.

There might be multiple symmetries and loci? If this is the case, repeat these steps.

## Characterize
Goal: list all important information about the symmetry

Is it possible to write the triplet $(G, \rho_X, \rho_Y)$?

Loop back to "Locate" if $G$ is found to not be exact
Is there an algebraic form for the action of $g$?
- If not is it because the symmetry is complex but there is an underlying symmetry (3D rotation seen in 2D) or because it is not a true symmetry (incomplete)
- If yes, can $\rho_X$ and $\rho_Y$ be written as matrices

Is $(G, \rho_X, \rho_Y)$ known?

Properties of $G$ as a group
- Continuous or discrete? If discrete, is it finite or infinite?
- Compact?

How does $G$ act:
- Invariantly or equivariantly? If equivariant, is the action the same on input and output space?

Does $G$ formally verifies the axioms of group? If not, describe the actual weaker structure.
If yes, does the symmetry always holds fully? If not does it depend on a notion of time (dynamic) or on space (extent-restricted) or is the symmetry restricted to a subgroup (extent restricted, subgroup case) or up to a tolerance (approximate)?

## Act
This is the purpose axis extended beyond the binary "prescriptive" or "descriptive".

Is it a bug, a feature or an object of study?

What do I want to do?
- Discover/describe
- Explain/understand
- Remove/account for -> symmetry breaking
- Exploit -> GDL, prior

Use the symmetry as a prior:
- Should I hard-code it / Do I have competencies and time to develop an equivariant model? Is it worth it (\Cref{sec:edl-tradeoffs})? If yes, should I try something in-between to still allow it to break?
- augment for it, regularise toward it with an unconstrained model, let it be learned

## Diagnose
How do I diagnose whether the assumed symmetry is actually wrong?
Cues that something is wrong, mechanisms to find that something is not right, guardrails.
- An equivariant model looses against an unconstrained one (or augmented one)
- An equivariance error is large
- 

# Unused
If it was not possible to write $(G, \rho_X, \rho_Y)$, is it because the symmetry is unknown and discovery is the objective?