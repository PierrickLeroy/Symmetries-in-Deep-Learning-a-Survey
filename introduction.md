# Introduction

## Symmetries

In basic (planar) geometry there are four main types of symmetries.
A reflection mirrors the plane around a line, a rotation spins it around a single point and translations and glide reflections shift it without any fixed point.
But symmetry can also be abstract and many objects can have symmetries: the bijections of a set onto itself are the permutations.

In fact, group theory, which is the language of symmetry takes root in three different fields: the theory of algebraic equations, number theory, and geometry [wussing1984].
Ideas underpinning the notion of group can be traced back to Euler and Lagrange in the $18$-th century.
In his work on solid geometry, Legendre made the conceptual jump of of seing a symmetry as a transformation between object seen as equivalent [legendre1794,hon2008fststmoarsc].
Galois coined the term ``group'' around $1830$.
Felix Klein published his Erlangen program in $1872$ in which group theory becomes an organizing principle: different geometries are understood through the symmetries that preserve their structures.
Arthur Cayley ($1854$) then Heinrich Weber ($1882$) proposed an axiomatic definition of group but the universally accepted modern definition is due to Walther von Dyck, Klein's assistant.
The group axioms naturally capture the idea of a transformation that leaves an object unchanged: composing two such transformations gives another one (closure), doing nothing is one (identity), and each can be undone since nothing is lost (inverse); and associativity holds automatically.
This settled definition was then the starting point for other algebraic structures and for the development of abstract algebra.

The concept of symmetry has a variety of applications and extend beyond mathematics to physics, chemistry, biology and even architecture and art [weyl1952,makse2025]

## Deep learning

Deep learning is now the dominant approach in vision, language, the sciences and many use cases.
A model results from a pipeline (data and their augmentations, architecture, loss, optimizer, training protocol), whose components evolve and are often adopted because they work thus progress has been largely empirical, though not only.
The resulting models are hard to interpret, and the subfields studying them (vision, graph learning, self-supervised learning, learning theory, scientific ML) have developed separate vocabulary and practices.

## Symmetries and deep learning

Symmetry recurs at each stage of the deep learning pipeline.
Some symmetries are imposed on purpose: an equivariant layer, a contrastive loss, an augmentation policy, while others appear without being asked for: hidden neurons can be permuted without changing the function, batch normalization makes the loss scale invariant, and predicting sets is invariant to the order of predictions.
Some symmetries are not known in advance and must be discovered and many hold only approximately or on part of the domain.
Working explicitly with a symmetry can turn a heuristic into a precise statement: invariance says what plays no role, equivariance how it plays a role.
The same notion can also play opposite roles: a prior on data but a confounder on parameters.

These occurrences are studied by separate communities and existing surveys each cover one object or domain (details in Related work).

## Objective

In contrast, we start from the concept of symmetry and go broad: with a mathematical perspective, we list where, why and how it occurs across deep learning, from the problem to the training framework, including the data side (data augmentation, symmetries of the data distribution) and symmetries that are unknown or incomplete.
Symmetry has many faces and we try to tell them apart.
Geometric deep learning [bronstein2021] follows Klein's Erlangen program to classify architectures by the symmetries of their domains.
We extend this perspective from architectures to every place where symmetry occurs (data, parameters, optimization, training pipeline) and classify the occurrences themselves, adhering to the words of Alan Perlis: "Symmetry is a complexity-reducing concept; seek it everywhere.".
Our contributions are threefold:
(i) a faceted taxonomy (\Cref{tab:taxonomy}) whose six axes locate, link and contrast occurrences of symmetry across subfields;
(ii) an inventory of $322$ works organized along this taxonomy, underpinned by a hybrid systematic review and the coding of the corpus (\Cref{sec:materials-methods});
(iii) underexplored areas and possible gaps (\Cref{sec:discussion}).
By mapping these occurrences under a single perspective, we hope to foster the transfer of knowledge and methods between subfields.

The survey is intended for three audiences: researchers in one of the covered fields looking for a bird's-eye view, mathematicians looking for areas where symmetry applies, and deep learning practitioners who want to make the notion of invariance precise.


## Narrative

The first part is a short background on symmetries and group theory, which can be skipped for the accustomed reader.
Then, in first approximation, the story of the paper is a conceptual progression from symmetry imposed by design to symmetry as a by-product, to unknown symmetries that have to be discovered and finally cases that are not exactly symmetries.
Lastly, current active research and possible gaps are identified. 

One caveat, the exposition is a choice among several possibilities; some segments could be transferred to other places (e.g. equivariant optimizer is in the section about the parameter space but it could be in the symmetry by design section)


# Cut

Opposite notions exist such as asymmetry, the absence or violation of symmetry,  or antisymmetry (asymmetric relation: $x\sim y \implies y\nsim x$, antisymmetric relation: $(x\sim y \wedge y\sim x)\implies x=y$).

One notable achievement is the classification of finite simple groups, a $50$ year collective endeavor.

Deep learning is very powerful but learning in high dimension suffers from the curse of dimensionality and therefore needs structure which symmetry can provide.

Networks themselves are overparametrized and their training is non-convex.
It is generally not well understood why training works and what gets learned.
Here symmetries provide a double answer by analysing them it might be possible to eliminate redundancies (make parameter spaces more identifiable), but they can also make training more explicit, uncovering implicit bias or constraints (conservation laws)

Symmetry as the starting point
In contrast, we start from the concept of symmetry and go broad: we list its occurrences across deep learning, from the problem to the training framework including symmetries that are unknown or incomplete, and organize them in a faceted taxonomy across subfields (\Cref{tab:taxonomy}), linking and contrasting them for a high-level, structuralist understanding.

Symmetries appear in different context and with different roles, which this survey tries to disentangle:
- as an inductive prior that must be respected
- as a unifying perspective to classify architecture 
- as a counfounder
- as an unknown
- as a broken object
They can be studied or used.
Symmetries have opposite effect depending on the context: in data they are often insightful and can offer powerful inductive priors; in parameters they are counfounding factors.
They can be obvious or hidden; branches focuses on finding them analytically or extracting them from data i.e. they become a goal of machine learning instead of a mean to an end.

This survey seeks to disentangle these multiple faces.

This work is a survey looking with a mathematical perspective at the notion of symmetry occurring in a deep learning context.
It does not focus on a single branch but is symmetry-centered: starting from this notions and noting where, why and how it appears.
The scope is intended to be broad: multiple area/branches use symmetry in deep learning context but not always with the same tools.
Providing a broad overview could foster inter-branch methodological transfers. 
The goal is to map, organize, and synthesize theses occurrences under a single perspective.
The targeted audience could be either a practioner working in one of the covered fields looking for a bird eye view, a mathematician looking for areas to apply symmetry or a deep learning practicioner curious to make the notion of invariance precise.
The principal contribution of this work is a taxonomy and inventory of symmetry loci conducted at a broad scale, underpinned by a hybrid systematic review permitted by recent advances in language models. 
We hope to help the community transfer knownledge and methods from one subfield to the other, and to structure the field and identify gaps.

Symmetry as a clarifying tool (Erlangen program).