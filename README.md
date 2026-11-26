# Disproving and Correcting the Distance Laplacian and Distance Signless Laplacian Brouwer-Type Conjectures

> **Phase II audit: not release-ready.** See [independent audit](verification/phase2-independent-audit-2026-11-26.md) for confirmed prior work, independent checks, and formalization limitations. The signless inequality studied here was already rejected as Question 1 in the original paper; the final conjecture is different. The distance Laplacian inequality also has previously published counterexamples. End-to-end real-spectral formalization is not established.

[![Build papers](https://github.com/Pasukalu/distance-brouwer-refutation/actions/workflows/build-papers.yml/badge.svg)](https://github.com/Pasukalu/distance-brouwer-refutation/actions/workflows/build-papers.yml)
[![Verify Lean proofs](https://github.com/Pasukalu/distance-brouwer-refutation/actions/workflows/verify-lean.yml/badge.svg)](https://github.com/Pasukalu/distance-brouwer-refutation/actions/workflows/verify-lean.yml)
[![Lean 4](https://img.shields.io/badge/Lean-4.36.0-blue.svg)](https://lean-lang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This repository contains the arithmetic certificates and analysis, exhaustive $n \le 7$ census ($994$ non-isomorphic connected graphs), publication-quality figures, and structural correction of two published spectral graph theory conjectures:

1. **Alhevaz, Baghipur, Ganie, and Pirzada (2021)** (*Linear and Multilinear Algebra* **69**, 2423–2440; still studied as open in *J. Comb. Optim.* **52**(5), Nov 2026): for every connected non-path graph $G$ and $1 \le k \le n$,
   $$M_k^Q(G) = \sum_{i=1}^k \rho_i^Q(G) \le W(G) + \binom{k+2}{3}.$$
2. **Zhou, Wang, and Chai (2025)** (*Computational and Applied Mathematics* **44**, article 138; still studied as open in *AIMS Mathematics* **11**(10), Oct 2026): for every connected graph $G$ and $1 \le r \le n$,
   $$U_r(G) = \sum_{i=1}^r \partial_i^L(G) \le W(G) + \binom{r+2}{3}.$$

## Main Results

- **Exhaustive $n \le 7$ Census ($994$ non-isomorphic connected graphs: $2, 6, 21, 112, 853$):**
  - $D^L(G)$ violations: $0$ ($n=3$), $2$ ($n=4$), $6$ ($n=5$), $19$ ($n=6$), $61$ ($n=7$).
  - $D^Q(G)$ non-path violations: $0$ ($n \le 5$), $6$ ($n=6$, led by unicyclic $L(3,3)$ and broom tree $B(4,2)$), $16$ ($n=7$, including **100% (9/9)** of all diameter-5 non-path graphs).
  - Corrected universal bound violations: **0 / 994**.
- **Catastrophic $\Theta(n^3)$ Simultaneous Refutation:**
  Pure Schur diagonal majorization proves simultaneous $\Theta(n^3)$ failure on paths $P_n$ ($n \ge 9$), non-path broom trees $B(n-2,2)$ ($n \ge 10$), and unicyclic lollipops $L(3, n-3)$ ($n \ge 12$), with asymptotic excess at least $(\frac{\sqrt{3}}{2} - \frac{5}{6}) n^3 \approx 0.032692\,n^3$.
- **Corrected Universal Theorem:**
  For every connected graph $G$ of order $n \ge 2$ and diameter $D = \operatorname{diam}(G)$, and every $1 \le r \le n$,
  $$U_r(G) \le W(G) + D\binom{r+1}{2}, \qquad M_r^Q(G) \le W(G) + D\binom{r+1}{2}.$$
- **Lean 4 arithmetic artifacts (full real-spectral bridge not verified):**
  Includes formal proofs of Bessel's inequality, an integer spectral-weight inequality under supplied hypotheses, the structural transmission-subset identity, distance-threshold decomposition, all 6 minimal orthogonal rational certificates, all 3 infinite $\Theta(n^3)$ families, and both corrected-bound core lemmas.

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
│   └── analyze_n7_and_plot.py          # Full n<=7 census (994 graphs) + publication figure generator
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
cd lean && lake build

# 2. Exact C++ n=7 enumeration (853 non-isomorphic connected graphs)
g++ -O3 cpp/enum_n7.cpp -o enum_n7 && ./enum_n7 > n7_masks.txt

# 3. Python full verification and figure generation
python3 python/verify_all.py
python3 python/analyze_n7_and_plot.py

# 4. Compile English & Chinese papers
cd paper && lualatex paper_en.tex && lualatex paper_en.tex
lualatex paper_zh.tex && lualatex paper_zh.tex
```
