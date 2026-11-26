# Disproving and Correcting the Distance Laplacian and Distance Signless Laplacian Brouwer-Type Conjectures

[![Build papers](https://github.com/Pasukalu/distance-brouwer-refutation/actions/workflows/build-papers.yml/badge.svg)](https://github.com/Pasukalu/distance-brouwer-refutation/actions/workflows/build-papers.yml)
[![Verify Lean proofs](https://github.com/Pasukalu/distance-brouwer-refutation/actions/workflows/verify-lean.yml/badge.svg)](https://github.com/Pasukalu/distance-brouwer-refutation/actions/workflows/verify-lean.yml)
[![Lean 4](https://img.shields.io/badge/Lean-4.36.0-blue.svg)](https://lean-lang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This repository contains arithmetic certificates, numerical $n \le 7$ census ($994$ non-isomorphic connected graphs), publication-quality figures, and structural correction of two published spectral graph theory conjectures:

1. **Alhevaz, Baghipur, Ganie, and Pirzada (2021)** (*Linear and Multilinear Algebra* **69**(13), 2423–2440, [doi:10.1080/03081087.2019.1679074](https://doi.org/10.1080/03081087.2019.1679074); studied for diameters 3 and 4 in *J. Comb. Optim.* **52**(5), Art. 53, 2026): for every connected non-path graph $G$ and $1 \le k \le n$,
   $$M_k^Q(G) = \sum_{i=1}^k \rho_i^Q(G) \le W(G) + \binom{k+2}{3}.$$
2. **Zhou, Wang, and Chai (2025)** (*Computational and Applied Mathematics* **44**(3), Art. 138, [doi:10.1007/s40314-025-03095-0](https://doi.org/10.1007/s40314-025-03095-0); explicit exceptions $K_{1,3}$ at $r=2$ and $K_{1,4}$ at $r=3$ already reported by [Huang (2026)](https://doi.org/10.3934/math.20261314), arXiv:2606.06945): for every connected graph $G$ and $1 \le r \le n$,
   $$U_r(G) = \sum_{i=1}^r \partial_i^L(G) \le W(G) + \binom{r+2}{3}.$$

## Main Results

- **Exhaustive $n \le 7$ Census (the $994$ connected graphs of orders $3\le n\le 7$: $2, 6, 21, 112, 853$; $995$ if the $2$-vertex graph is included):**
  - $D^L(G)$ violations: $0$ ($n=3$), $2$ ($n=4$), $6$ ($n=5$), $19$ ($n=6$), $61$ ($n=7$).
  - $D^Q(G)$ non-path violations: $0$ ($n \le 5$), $6$ ($n=6$, led by unicyclic $L(3,3)$ and broom tree $B(4,2)$), $16$ ($n=7$, including **100% (9/9)** of all diameter-5 non-path graphs).
  - Corrected universal bound violations: **0 / 994**.
- **Catastrophic $\Theta(n^3)$ Simultaneous Refutation:**
  Pure Schur diagonal majorization proves simultaneous $\Theta(n^3)$ failure on paths $P_n$ ($n \ge 9$), non-path broom trees $B(n-2,2)$ ($n \ge 10$), and unicyclic lollipops $L(3, n-3)$ ($n \ge 12$), with asymptotic excess at least $(\frac{\sqrt{3}}{2} - \frac{5}{6}) n^3 \approx 0.032692\,n^3$.
- **Corrected Universal Theorem:**
  For every connected graph $G$ of order $n \ge 2$ and diameter $D = \operatorname{diam}(G)$, and every $1 \le r \le n$,
  $$U_r(G) \le W(G) + D\binom{r+1}{2}, \qquad M_r^Q(G) \le W(G) + D\binom{r+1}{2}.$$
- **Lean 4 arithmetic verification (18 audited theorems):**
  Integer certificates, the scaled majorization/Bessel core lemma, the path/broom/lollipop family inequalities and the corrected-bound core lemmas are kernel-checked with zero `sorry`; every audited theorem depends only on `propext`, `Classical.choice` and `Quot.sound` (the `#print axioms` output is in the public CI log). Real spectral theory, the graph-to-matrix bridge, the full census and the universal graph-level statements are **not** formalized. The numerical census is not an exact spectral proof; priority for the signless counterexamples remains unverified. Paths are excluded from the signless inequality.

## Repository Structure

```text
.
├── lean/
│   ├── lean-toolchain                  # Lean 4.36.0
│   ├── lakefile.toml                   # Zero-dependency Lake build config
│   ├── DistanceBrouwerRefutation.lean  # 15 core theorems + #print axioms audit
│   └── KyFanSpectral.lean              # Bessel's inequality, Ky Fan Maximum Principle, distance decomp
├── cpp/
│   └── enum_n7.cpp                     # Exact isomorphism-free enumerator of all 853 connected 7-vertex graphs
├── python/
│   ├── verify_all.py                   # Minimal certificates, n<=6 exhaustive check, scaling up to n=100
│   ├── analyze_n7_and_plot.py          # Full n<=7 census (994 graphs) + publication figure generator
│   └── phase2_exact_atlas.py           # Phase-II exact-root-interval census (SymPy intervals)
├── verification/
│   ├── phase3_independent.py           # Independent generator + census + certificates + stress tests
│   ├── check_lean_hygiene.py           # CI guard: no sorry/axiom, exactly 18 axiom audits
│   ├── peer-review-report.md           # Independent referee report
│   ├── originality-audit.md            # Priority / novelty audit with verified metadata
│   ├── formalization-coverage.md       # Theorem-by-theorem Lean coverage and gaps
│   └── submission-readiness.md         # Venues, AI policies, submission checklist
├── paper/
│   ├── paper_en.tex                    # English LaTeX paper (with 3 figures)
│   ├── paper_zh.tex                    # Chinese LaTeX paper (with 3 figures, LuaLaTeX)
│   └── figures/                        # Vector PDF and 300-DPI PNG figures
├── LICENSE                             # MIT License
└── README.md
```

## Quick Reproduction

```bash
# 1. Lean 4 formal verification (zero sorry, ~6s)
(cd lean && lake build)

# 2. Exact C++ n=7 enumeration (853 non-isomorphic connected graphs)
g++ -O3 cpp/enum_n7.cpp -o enum_n7 && ./enum_n7 > n7_masks.txt

# 3. Python full verification and figure generation
python3 -m pip install -r requirements.txt
python3 python/verify_all.py
python3 python/analyze_n7_and_plot.py

# 4. Compile English & Chinese papers
(cd paper && lualatex paper_en.tex && lualatex paper_en.tex && lualatex paper_zh.tex && lualatex paper_zh.tex)
```


## Independent verification (phase 3)

A second implementation (`verification/phase3_independent.py`, no shared code with `python/verify_all.py`) regenerates the graph set from scratch, recomputes every spectrum and re-verifies every certificate. It is run in CI on each push. Results on 2026-11-26:

| Check | Result |
|---|---|
| Connected graphs, orders 2–7 | 1, 2, 6, 21, 112, 853 (A001349) |
| $D^L$ violations, $n=3\ldots7$ | 0, 2, 6, 19, 61 |
| $D^Q$ non-path violations | 0, 0, 0, 6, 16 |
| Corrected-bound violations | 0 / 994 |
| Diameter-5 non-path graphs at $n=7$ | 9, all 9 violate both inequalities |
| Six rational certificates | all orthogonal, all strict (exact arithmetic) |
| Corrected bound, random graphs $8\le n\le13$ | 0 / 3,600 violations, minimum slack 9.71 |
| $\Theta(n^3)$ families, $n\le150$ | violation for every tested $n$; excess/$n^3\to0.0309$ |

Reports: [peer review](verification/peer-review-report.md), [originality audit](verification/originality-audit.md), [formalization coverage](verification/formalization-coverage.md), [submission readiness](verification/submission-readiness.md).

## Audit status

The checked-in PDFs predate the audit revisions until rebuilt. Consult the LaTeX sources and CI artifacts. No claim of priority is made for the known distance Laplacian counterexamples. See `AUDIT.md` for remaining proof obligations.
