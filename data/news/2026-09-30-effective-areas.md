---
date: 2026-09-30
type: paper
title: Where do neutrino telescope effective areas come from?
paper: Meighen-Berger:2026yls
software: softpaws
version: 1.0.0
image: img/news/effective-areas.png
image_alt: Line plot of effective area versus neutrino energy for TRIDENT, KM3NeT/ARCA, P-ONE and IceCube. Solid published curves and dashed first-principles curves lie on top of each other.
caption: Published effective areas (solid) and the first-principles calculation (dashed) for four telescopes.
---
Neutrino telescopes see neutrinos through the muons they produce. Most of those muons are born kilometers outside the detector, and how far they travel decides how many neutrinos a telescope can catch. Experiments usually get this number, the effective area, from large detector simulations. These tell us what a detector sees, but not why.

In this paper I compute the muon's range analytically, including the random way it loses energy. The result reproduces full Monte Carlo propagation to within 3%. With just two numbers per detector, it matches the published effective areas of IceCube, KM3NeT/ARCA and P-ONE to about 1%. Because muon physics and detector response are now separate, a new detector or a new energy-loss model can be benchmarked quickly.

The calculation is released as softpaws 1.0, an open Python package with documentation. Anyone can reproduce these effective areas or predict them for a detector that has not been simulated yet.
