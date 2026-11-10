# Introduction

## Symmetries

In basic (planar) geometry there are three main types of symmetries.
A reflection mirrors the plane around a line, a rotation spins it around a single point and a translation shifts it without any fixed point.
But symmetry can also be abstract and many objects can have symmetries: automorphisms on sets give rise to the permutation.

In fact, group theory, which is the language of symmetry takes root in three different fields: the theory of algebraic equations, number theory, and geometry [wussing1984].
Ideas underpinning the notion of group can be traced back to Euler and Lagrange in the $18$-th century.
Legendre is credited [hon2008fststmoarsc] for seing symmetry as transformations.
Galois coined the term ``group'' around $1830$.
Felix Klein published his Erlangen program in $1872$ in which group theory becomes an organizing principle: different geometries are understood through the symmetries that preserve their structures.
Arthur Cayley ($1854$) then Heinrich Weber ($1882$) proposed an axiomatic definition of group but the universally accepted modern definition is due to Walther von Dyck, Klein's assistant.
The group axioms reflect in a natural way the idea of "a transformation that doesn't change".
Namely, chaining two transformations that don't change produces can be seen as a transformation that doesn't change itself (closure), any transformation can be undone (inverse), in particular transformation are lossless since they do not change the object.
Finally doing nothing can be seen as a trivial transformation (identity).
The settled definition was then a starting point for other structures and the development of abstract algebra.
One notable achievement is the classification of finite simple groups, a $50$ year collective endeavor.

Opposite notions exist such as asymmetry (the absence or violation of symmetry) or antisymmetric relations ($x\sim y \implies y\nsim x$).

Symmetries are transformations that leave something unchanged (or changed in a way we understand).
As such, "Symmetry is a complexity-reducing concept; seek it everywhere." (quote from Alan Perlis, originally in a programming context)
symmetry is a way to make precise the notion of ``understanding'': with invariance we understand what does not play a role; with equivariance we understand how it plays a role

The concept of symmetry has a variety of applications and extend beyond mathematics to physics, chemistry, biology and even architecture and art [weyl1952,makse2025]

## Deep learning

Deep learning is very powerful

Deep learning and high dimensional is not interpretable

While we are interested by deep learning, we also include inherently related data aspects.

## Symmetries and deep learning

Deep learning is full of symmetries
Symmetry touch on many aspects of deep learning
Deep learning is not very interpretablen symmetry has a role of organizing principle as in GDL.

## Objective

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

## Narrative

The story of the paper is a conceptual progression from symmetry known → symmetry used → symmetry observed in parameters whose consequence are too be understood → symmetry unknown → not completely a symmetry (broken/incomplete) Lastly, current active research and possible gaps are identified. 

The exposition is a choice among several possibilities; some segments could be transferred to other places (e.g. equivariant optimizer is in the section about the parameter space but it could be in the symmetry by design section)
