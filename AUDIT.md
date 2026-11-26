# Research audit and proof obligations

Updated 2026-11-26 (phase 3). Full details: `verification/peer-review-report.md`, `verification/originality-audit.md`, `verification/formalization-coverage.md`, `verification/submission-readiness.md`.

## Established scope

- Concrete integer Rayleigh certificates give strict counterexamples by the real Ky Fan inequality. All six certificates are verified exactly (orthogonal, strict) by `verification/phase3_independent.py`.
- **Priority (Laplacian side).** Huang (2026), AIMS Math. **11**(10) 33617–33633, DOI `10.3934/math.20261314`, arXiv:2606.06945, already records the exceptions $K_{1,3}$ ($r=2$) and $K_{1,4}$ ($r=3$). No priority is claimed for refuting the distance Laplacian inequality; this work extends that refutation.
- **Priority (signless side).** The full text of Alhevaz et al. (2021) is paywalled (Unpaywall: no OA copy; T&F 403; zbMATH API returns metadata only), so its exact final conjecture could not be read. What *is* verified (2026-11-26): two independent 2026 papers attribute the non-path inequality to that paper in the form used here --- Zhang, Wang and Miao, *J. Comb. Optim.* **52**(5), Art. 53, DOI `10.1007/s10878-026-01488-3` ("for any graph G that is not a path and 1 ≤ k ≤ n"), and Mushtaq, Pirzada and Khan, *Rev. Un. Mat. Argentina* **69**(1) 193--202, DOI `10.33044/revuma.5147` ("for any k = 2,...,n"). The admissible range is therefore **not fixed** by the secondary literature (1..n vs 2..n), and a draft PR (#2) claim that §4 already lists k=3,4 counterexamples remains **unverified and is not adopted**. The object studied here is quoted as "the inequality of [ABGP 2021]"; every counterexample reported occurs at k ≥ 3 and is valid under either reading.
- The numerical census is not a certified spectral classification. Exact graph isomorphism checks do not establish the sign of a floating-point spectral excess; the smallest observed margins are $0.0283$ (original bounds) and $9.71$ (corrected bound), far above numerical error but not exact proofs.
- Paths are outside the domain of the signless inequality.
- Lean checks arithmetic statements, not the real spectral theorem, and not the graph-to-matrix bridge.

## Corrected arithmetic (verified exactly in this phase)

- $L(3,3)$: Rayleigh quotients $10$, $194/9$, $52/5$; total $1888/45>41$ ($W=31$).
- $P_5$: third vector $(1,-1,0,-1,1)$; total $65/2>30$; the previously printed $(1,-2,2,-2,1)$ is not orthogonal to the second vector.
- $B(3,2)$: total $291/10>28$ ($W=18$).
- $B(4,2)$: $646/15>42$ ($W=32$), unchanged.
- Comb on $P_6$: $W=206$, $U_7\approx300.1091677861>290$ (excess $+10.1092$). The previously reported $W=246$, $U_7=376.1092$ were wrong. This is also a counterexample to Theorem~3.2 of the May 2026 AIMS paper (uniform caterpillars, diameter $\ge6$, $1\le r\le n-1$): the comb has $\ell=1$, diameter $7$, and $r=7\le11$.

## Independence and reproduction (phase 3)

- Second implementation, no shared code: graph generation, spectra, certificates, corrected-bound stress test ($0/3600$ violations), $\Theta(n^3)$ families to $n=150$. All census counts reproduce exactly: $D^L$ $0,2,6,19,61$; $D^Q$ non-path $0,0,0,6,16$; $0/994$ corrected violations; $9$ diameter-5 non-path graphs, all violating.
- Lean: CI `lake build` green; 18 `#print axioms` outputs; all in $\{\texttt{propext},\texttt{Classical.choice},\texttt{Quot.sound}\}$; no `sorryAx`; hygiene guard added to CI.
- A false alarm in this phase (an initial DFS-based census giving inflated counts) was traced to the reviewer's own code and is recorded in the peer-review report.

## Remaining publication gates

- **Read Alhevaz et al. (2021) §4** and finalise the wording of the signless "conjecture".
- Rebuild both PDFs (done automatically by CI) and re-release.
- Author identity, affiliation, ORCID, licence and the final AI disclosure statement: require the human author.
- Record one authenticated MathSciNet/zbMATH search and a "Note added" paragraph before submission.
- The corrected universal bound is conditional on two 2026 arXiv preprints (Kothari–Tudose, arXiv:2606.12197; Yuan–Zhang, arXiv:2609.31355); the paper states the unconditional fallback bound as well.
