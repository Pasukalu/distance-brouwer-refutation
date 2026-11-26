# Formalization coverage report (Lean 4)

**Project:** `lean/DistanceBrouwerRefutation.lean` (15 audited theorems) + `lean/KyFanSpectral.lean` (3 audited theorems), Lean `v4.36.0`, zero dependencies, GPL-compatible MIT repository licence.
**Evidence date:** 2026-11-26.

## 1. Build and hygiene evidence (from CI, not from the author's claims)

`Verify Lean proofs` workflow, run on commit `8778f49` (Ubuntu 26.04, elan install, `lake build` in `lean/`):

- `Build completed successfully (7 jobs).`
- `18` occurrences of `#print axioms` in the build log; every one reports a dependency set contained in `{propext, Classical.choice, Quot.sound}`.
- `0` occurrences of `sorryAx` in the log.
- Static scan of the sources: no `sorry`, no `admit`, no `axiom`, no `native_decide`, no `unsafe`, no `partial`. The only textual matches of the word "sorry" are in the module docstrings claiming its absence.
- `lake-manifest.json` has no packages (`"packages": []`); the build needs no Mathlib.

This is reproducible by anyone with the repository: `cd lean && lake build` (22 s in CI).

## 2. Theorem-by-theorem coverage

Legend: **[A]** arithmetic statement, fully formalized and kernel-checked; **[S]** spectral statement *assumed* through explicit hypotheses (integer eigenvalues, unit vectors, Parseval/Rayleigh identities supplied), not derived from real symmetric matrices; **[P]** paper-level claim, not formalized.

| Lean name | Statement | Status | Paper claim it supports |
|---|---|---|---|
| `ky_fan_majorization_lemma` | For non-increasing integer `lam`, weights `0≤w≤D` with `∑w=rD`: `∑ w·lam ≤ D·∑_{i<r} lam` | [A] (integer majorization core) | Ky Fan maximum principle — **only the arithmetic core** |
| `ky_fan_maximum_principle_spectral` | Scaled spectral form with integer spectra and orthonormal data supplied | [S] | Ky Fan, Lemma 2.1 |
| `bessel_inequality_scaled` | Scaled Bessel inequality for integer vectors | [A]/[S] | Parseval step of the proof |
| `structural_transmission_identity` | Transmission-subset identity (integer form) | [A] | Lemma on transmission splits |
| `distance_threshold_decomp` | Threshold-graph decomposition identity (integer) | [A] | Distance-matrix decomposition lemma |
| `P4_refutes_DL_conjecture`, `K13_refutes_DL_conjecture` | Boolean certificate check `15>14`, `14>13` | [A] | Minimal $D^L$ counterexamples at $n=4$ |
| `P5_refutes_DL_conjecture` | Certificate check with $\sum=65/2>30$ | [A] | $U_3(P_5)=33>30$ (lower bound only) |
| `B32_refutes_DL_conjecture` | $\sum=291/10>28$ | [A] | $U_3(B(3,2))$ violation |
| `B42_refutes_DQ_conjecture` | $\sum=646/15>42$ | [A] | $M_3^Q(B(4,2))$ violation |
| `L33_refutes_DQ_conjecture` | $\sum=1888/45>41$ | [A] | $M_3^Q(L(3,3))$ violation |
| `sumEndTrPath_closed_form`, `wiener_path_closed_form` | Closed forms for path transmission sums and $W(P_n)$ | [A] | Path family computation |
| `path_schur_refutation_all_n` | $\Delta_P(n,t)>0$ for $n\ge9$, $t=\lfloor n/3\rfloor$ | [A] | $\Theta(n^3)$ path family |
| `broom_schur_refutation_all_n` | Broom family inequality | [A] | Broom family |
| `lollipop_schur_refutation_all_n` | Lollipop family inequality | [A] | Lollipop family |
| `corrected_DL_core`, `corrected_DQ_core` | Integer inequalities underlying $W+D\binom{r+1}{2}$ | [A] | Corrected bound — **core arithmetic only** [P] for the graph statement |

## 3. What is *not* formalized

1. **Real symmetric spectral theorem.** No construction of real symmetric matrices, no existence of an orthonormal eigenbasis, no Rayleigh-quotient theory over $\mathbb R$. The spectral lemmas take the spectral data as hypotheses.
2. **Graph → matrix bridge.** No graph type, no shortest-path distance function, no proof that the integer matrices used are the distance/signless Laplacian matrices of the stated graphs. (The validity predicates `isValidGraphDistance` check metric axioms, which is necessary but not sufficient for realizability by a graph.)
3. **Census.** The 994-graph enumeration, the violation counts and the "0/994" corrected-bound statement are computational, not formalized.
4. **Universal corrected theorem.** Only the arithmetic core is formalized; the derivation from the spectral decomposition is paper-level.
5. **Minimality claims** ("unique minimal counterexamples", "exactly six") are numerical, not formalized.

## 4. Statement-to-paper consistency check

The formalized statements were compared with the current `paper/paper_en.tex` and `paper/paper_zh.tex`:

- Certificate values match the paper's Table 1 after the v1.0.1 corrections ($10,194/9,52/5$; $646/15$; $291/10$; $65/2$).
- `path_schur_refutation_all_n` matches the paper's $\Delta_P$ formula.
- The paper's abstract no longer claims that Ky Fan's principle or the graph-level theorems are formalized; §"Scope of the Lean 4 Arithmetic Verification" matches the gaps listed above.

**One residual mismatch to fix:** the README still describes `DistanceBrouwerRefutation.lean` as containing "15 core theorems + `#print axioms` audit" while the paper says 18; both are right (15 + 3), but the wording should be unified.

## 5. Verification-CI hardening added in this phase

`verification/check_lean_hygiene.py` (run in the `Verify Lean proofs` workflow) fails the build if any `.lean` file contains `sorry`, `admit`, `axiom `, `native_decide`, `unsafe ` or `partial ` outside comments, and asserts that the number of `#print axioms` lines is 18. It also prints the list of audited theorem names so that a reviewer can diff it against this report.
