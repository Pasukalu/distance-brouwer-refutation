# Peer-review report (independent, AI-assisted)

**Manuscript:** *Disproving and Correcting the Distance Laplacian and Distance Signless Laplacian Brouwer-Type Conjectures*
**Repository:** `Pasukalu/distance-brouwer-refutation`, commit under review: `8778f49` + phase-3 changes
**Reviewer role:** independent mathematical referee / formalization reviewer
**Date:** 2026-11-26
**Recommendation:** **major revision, then accept** — the core mathematical claims survived independent re-derivation, but three classes of defects had to be repaired first (two are now repaired in the repository, one is open).

## 1. Summary of the submission

The manuscript studies two eigenvalue-sum inequalities for the distance Laplacian $D^L(G)$ and the distance signless Laplacian $D^Q(G)$ with the Wiener index $W(G)$ and the binomial penalty $\binom{r+2}{3}$, reports exhaustive counterexamples for $n\le 7$ (994 connected graphs of orders 3–7), proves a $\Theta(n^3)$ asymptotic failure for three infinite families, and proposes the corrected bound $W(G)+D\binom{r+1}{2}$. A Lean 4 development formalizes integer certificates and auxiliary lemmas.

## 2. Findings, with status

| # | Finding | Severity | Status |
|---|---|---|---|
| R1 | **Priority.** The distance-Laplacian inequality was already refuted before this manuscript: the authors' own citation of Huang (2026) lists the exceptions $K_{1,3}$ at $r=2$ and $K_{1,4}$ at $r=3$. Presenting the paper as the refutation of that inequality was an overclaim. | major | **fixed** in v1.0.1 (reframed as "we extend") |
| R2 | **Wrong rational quotients.** For $L(3,3)$ the text printed $196/9+51/5+10$, which sums to $1889/45$, contradicting the printed total $1888/45$. Correct values are $194/9$ and $52/5$ (verified by exact rational arithmetic in `verification/phase3_independent.py`). | major | **fixed** |
| R3 | **Invalid certificate.** The $P_5$ certificate vector $(1,-2,2,-2,1)$ is not orthogonal to the second vector (inner product 4), so Ky Fan does not apply. Replaced by $(1,-1,0,-1,1)$; the three Rayleigh quotients sum to $65/2=32.5$, and the true value is $U_3(P_5)=33>30$. | major | **fixed** |
| R4 | **Wrong Wiener index in the caterpillar remark.** The 12-vertex comb on $P_6$ has $W=206$, not $246$; the correct values are $U_7=300.1091677861$ and threshold $290$ (the printed $376.1092/366$ was shifted). The excess $+10.1092$ is unchanged. | major | **fixed** |
| R5 | **Census counts.** All counts were re-derived from scratch by an independent generator (no code shared with `python/verify_all.py`) and agree exactly: $D^L$ violations $0,2,6,19,61$; $D^Q$ non-path violations $0,0,0,6,16$; corrected-bound violations $0$; diameter-5 non-path graphs $9$, all $9$ violating. | — | **verified** |
| R6 | **Provenance of the signless conjecture.** The original Alhevaz–Baghipur–Ganie–Pirzada (2021) text is paywalled; the abstract says only that they "propose a Brouwer-type conjecture" and prove it for graphs of diameter 1 and 2. Whether the exact inequality quoted here is the final conjecture of that paper, or an intermediate question already known to have exceptions, **could not be verified** from accessible sources. A draft PR (#2) asserts that Section 4 of the original already records $k=3,4$ counterexamples; that assertion is **unverified** and is not adopted. | **major, open** | **open** |
| R7 | **"994" is orders 3–7.** Including $n=2$ gives 995; including $n=1$ gives 996. The text should say "the 994 connected graphs of orders $3\le n\le 7$". | minor | documented here, needs text edit |
| R8 | **Bibliography metadata.** Verified against Crossref: Zhou–Wang–Chai is *Comput. Appl. Math.* **44**(3), article **138** (not 14), DOI `10.1007/s40314-025-03095-0`; Zhang–Wang–Miao is *J. Comb. Optim.* **52**(5), article **53**, DOI `10.1007/s10878-026-01488-3`; Huang is *AIMS Math.* **11**(10) 33617–33633, DOI `10.3934/math.20261314`. | major (citations) | **fixed** in this revision |
| R9 | **Numerical census is not certified.** Floating-point eigenvalues decide strict inequalities with smallest observed margin $0.0283$ (original bounds) and $9.7$ (corrected bound) on $n\le7$ / 3,600 random graphs; the decisions are numerically unambiguous but not kernel-checked. The manuscript now says so. | minor | disclosed |
| R10 | **Lean scope.** `ky_fan_majorization_lemma` is a statement about integer sequences (`lam w : Nat → Int`) with monotonicity and sum hypotheses; it does not derive Ky Fan's principle from the real spectral theorem, and the graph-to-matrix bridge is absent. The earlier claim that "all core arguments are formally verified" was wrong; the current text scopes it correctly. | major | **fixed** |

## 3. Independent computations performed for this report

| Check | Method | Result |
|---|---|---|
| Graph enumeration | independent canonical-form generator (permutations within colour classes), orders 2–7 | 1, 2, 6, 21, 112, 853 (A001349) |
| Spectra | NumPy `eigvalsh` on integer matrices | counts as R5 |
| Certificates | exact `Fraction` Rayleigh quotients, orthogonality | all six certificates strict and orthogonal |
| Corrected bound | 994 census graphs + 3,600 random graphs ($n=8\ldots13$, trees and random) | 0 violations, minimum margin 9.71 |
| $\Theta(n^3)$ families | $P_n$ ($9\le n\le150$), $B(n-2,2)$ ($10\le n\le150$), $L(3,n-3)$ ($12\le n\le150$), $r=2\lfloor n/3\rfloor$ | violation for every tested $n$; excess$/n^3\to0.0309$ at $n=150$, consistent with $0.032692$ |
| Lean | CI `lake build`, 18 `#print axioms` | build OK; all theorems depend only on `propext`, `Classical.choice`, `Quot.sound`; no `sorryAx` |

A false alarm during this review is worth recording: an initial independent census used depth-first traversal and produced inflated counts (7/26/97). The discrepancy was traced to the reviewer's own bug, not to the manuscript; with breadth-first distances all counts match. This is exactly the kind of error that makes independent re-implementation worthwhile.

## 4. Remaining required revisions

1. **Resolve R6.** Obtain the published Alhevaz et al. text (institutional access) and quote its final conjecture verbatim in the paper; if the inequality is not their final conjecture, either (a) rename the object as "the inequality studied in [ABGP]" and remove "conjecture" language, or (b) identify the secondary source that states it as an open conjecture (e.g. Zhang–Wang–Miao 2026) and cite that formulation.
2. **Adopt R7 wording** everywhere (README, abstracts, tables, figures).
3. **State the numerical status** of the census explicitly in the abstract (one clause).
4. **Rebuild both PDFs** from the revised sources and re-release.
5. **Add the AI-use disclosure and data-availability statements** required by the target venue (see `submission-readiness.md`).

## 5. Assessment

The mathematical content that can be checked independently is correct: the certificates verify exactly, the census reproduces exactly, the corrected bound holds on everything tested, and the asymptotic family computation is consistent with the stated constant. The defects found were in exposition, arithmetic bookkeeping and scope claims, not in the central results. With R6 resolved and the PDFs rebuilt, this is a publishable contribution — as an *extension* of Huang's refutation on the Laplacian side, and as the first systematic non-path counterexample census plus corrected bound on the signless side, subject to the priority caveat.
