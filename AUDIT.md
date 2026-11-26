# Research audit and proof obligations

Updated 2026-11-26 (phase 3). Full details: `verification/peer-review-report.md`, `verification/originality-audit.md`, `verification/formalization-coverage.md`, `verification/submission-readiness.md`.

## Established scope

- Concrete integer Rayleigh certificates give strict counterexamples by the real Ky Fan inequality. All six certificates are verified exactly (orthogonal, strict) by `verification/phase3_independent.py`.
- **Priority (Laplacian side).** Huang (2026), AIMS Math. **11**(10) 33617–33633, DOI `10.3934/math.20261314`, arXiv:2606.06945, already records the exceptions $K_{1,3}$ ($r=2$) and $K_{1,4}$ ($r=3$). No priority is claimed for refuting the distance Laplacian inequality; this work extends that refutation.
- **Priority (signless side).** Unresolved. The full text of Alhevaz et al. (2021) is paywalled (Unpaywall: no OA copy; T&F returned 403), so the exact final conjecture of that paper could not be quoted. A draft PR (#2) asserts that its §4 already lists $k=3,4$ counterexamples; **that assertion is unverified and is not adopted**. The object studied here is quoted as "the inequality of [ABGP 2021]" until the source is read.
- The numerical census is not a certified spectral classification. Exact graph isomorphism checks do not establish the sign of a floating-point spectral excess; the smallest observed margins are $0.0283$ (original bounds) and $9.71$ (corrected bound), far above numerical error but not exact proofs.
- Paths are outside the domain of the signless inequality.
- Lean checks arithmetic statements, not the real spectral theorem, and not the graph-to-matrix bridge.

## Corrected arithmetic (verified exactly in this phase)

- $L(3,3)$: Rayleigh quotients $10$, $194/9$, $52/5$; total $1888/45>41$ ($W=31$).
- $P_5$: third vector $(1,-1,0,-1,1)$; total $65/2>30$; the previously printed $(1,-2,2,-2,1)$ is not orthogonal to the second vector.
- $B(3,2)$: total $291/10>28$ ($W=18$).
- $B(4,2)$: $646/15>42$ ($W=32$), unchanged.
- Comb on $P_6$: $W=206$, $U_7\approx300.1091677861>290$ (excess $+10.1092$). The previously reported $W=246$, $U_7=376.1092$ were wrong.

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
