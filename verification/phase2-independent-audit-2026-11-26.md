# Phase II independent audit — 2026-11-26

**Status: major revision; not release-ready.** This is an AI-assisted independent recomputation and source review, not a human referee decision or a successful Lean build.

## 1. Referee report
- Alhevaz et al. (DOI 10.1080/03081087.2019.1679074), Section 4, explicitly states that Question 1 already had counterexamples at k=3,4 and proposes a different Conjecture 1. Do not claim to refute that final conjecture. Reframe as analysis of the earlier inequality.
- Huang (DOI 10.3934/math.20261314, arXiv:2606.06945) explicitly gives K1,3 and K1,4 exceptions to the distance Laplacian inequality. Priority for first refutation is not ours.
- Zhou–Wang–Chai is Comput. Appl. Math. 44 (2025), article 138, DOI 10.1007/s40314-025-03095-0; not article 14. Secondary sources differ on the r=1 range; check the original typeset theorem before submission.
- For L(3,3) with the paper's vertex order, the three rational Rayleigh quotients are 10, 194/9, 52/5, not 10, 196/9, 51/5. The sum is still 1888/45.
- For the comb on a path with 6 spine vertices and 6 leaves, W=206, U_7≈300.1091677861, threshold=290. For 8 spine vertices, W=456, U_9≈626.4519137919, threshold=621. The excesses remain positive. These are independent numerical checks; verify the published caterpillar definition and certify the spectral inequality exactly before claiming a correction to that article.
- 994 counts orders 3–7 only; including order 2 gives 995, including order 1 gives 996.

## 2. Originality audit
Confirmed sources: original signless paper Section 4 (publisher DOI above and accessible author-text mirror https://www.academia.edu/99033406/); Huang AIMS paper; Kothari and Tudose, On Brouwer's Laplacian conjecture, arXiv:2606.12197; signless preprint arXiv:2609.31355 (abstract indexed, full source not independently read); 2026 caterpillar paper DOI 10.3934/math.2026625. Original Zhou paper publisher full text was not accessible. Search terms: distance Laplacian Brouwer conjecture counterexample; distance signless Laplacian Brouwer counterexamples; Brouwer signless Laplacian proof 2026. Site-restricted searches of Scholar, MathSciNet, zbMATH and Crossref were attempted, not equivalent to authenticated or exhaustive database search. No assertion of novelty for the census, asymptotic theorem or corrected bound.

## 3. Formal coverage report
Reviewed DistanceBrouwerRefutation.lean and KyFanSpectral.lean. The six Boolean rational certificates, integer polynomial inequalities and scalar threshold identity are relevant arithmetic statements. KyFanSpectral uses Int eigenvalues and Int unit vectors, plus supplied Parseval/Rayleigh identities, not the real symmetric matrix spectral theorem. The corrected_DL_core and corrected_DQ_core are only integer inequalities; the graph/eigenvalue/decomposition and Ky Fan subadditivity bridge is not verified end-to-end. A metric checker alone is not a proof of shortest-path realizability. No lean/lake/elan executable was available in this independent session. No fresh compilation, kernel replay, or axiom audit claimed.

## 4. Independent computational reproduction
NetworkX graph_atlas_g, Floyd–Warshall, NumPy eigvalsh, threshold 1e-8. Observed (order, connected, DL violations, DQ nonpath violations, corrected violations):
```
2 1 0 0 0
3 2 0 0 0
4 6 2 0 0
5 21 6 0 0
6 112 19 6 0
7 853 61 16 0
```
All nine diameter-five nonpaths on seven vertices violated both original inequalities. Independently calculated exact rational certificate totals: 15,14,65/2,291/10,646/15,1888/45. Float census is not an exact eigenvalue sign certificate; zero cases must be certified separately.
Reproduction algorithm: for each connected atlas graph take d=floyd_warshall_numpy(g), T=diag(d.sum(1)), W=d.sum()/2, D=d.max(), k=arange(1,n+1). Compute descending cumulative eigvalsh(T-d), eigvalsh(T+d); compare to W+k*(k+1)*(k+2)/6 and W+D*k*(k+1)/2. Exclude paths from DQ by degree<=2 and edge count n-1. Use exact Fraction(v@A@v,v@v) for certificates.

## 5. Independent derivation / stronger bound
For any threshold graph Y_s on distances >=s, write the distance matrices as a complete graph contribution plus sum of ordinary (signless) Laplacians for s=2,...,D. If the respective ordinary Brouwer theorem is established, Ky Fan subadditivity gives the sharper bounds
- U_r <= W + (D-1) binom(r+1,2) + n min(r,n-1) - binom(n,2);
- M_r^Q <= W + (D-1) binom(r+1,2) + n+(n-2)r - binom(n,2).
Both can be intersected with 2W by positive semidefiniteness. This retains the exact complete-graph contribution rather than bounding it again. Priority not searched. Not formalized.

## 6. Submission and release report
Potential venues: Linear Algebra and its Applications, Linear and Multilinear Algebra, Electronic Journal of Linear Algebra, Discrete Applied Mathematics, Computational and Applied Mathematics. Recheck each journal's current policy and scope; AI research and drafting must be transparently disclosed, with human verification and accountable human authorship. Publisher policy: https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals ; https://www.springernature.com/gp/policies/editorial-policies/using-ai-in-research . No human author statement, license changes, submission or DOI created. Release gate: corrected bilingual papers; exact census; graph-to-real-spectral Lean bridge, clean build and axiom audit; full priority search and human review; source/data/software versions and checksums; author-approved CITATION.cff and Zenodo metadata. Do not tag v1.0.0 until these are satisfied.

## Exact spectral follow-up (same session)
A second executed independent check used SymPy exact characteristic polynomials and rational root isolation (eps=1/10^9), preserving root multiplicities. All original graph-level violation counts were certified: an offending partial sum had a strict rational lower bound, or every upper bound was at most the threshold. No unresolved graph classifications. All corrected inequalities were certified for every r and both matrices on the 995 connected atlas graphs of orders 2–7, including paths. The atlas completeness itself relies on NetworkX. For the 12-vertex comb, U_7 lies between approximately 300.109167784047 and 300.109167788460, strictly above 290; for the 16-vertex comb, U_9 lies between 626.451913789535 and 626.451913794585, strictly above 621. These decimal endpoints are displays of exact rational intervals; the comparison was rational. A standalone reproduction script is supplied at python/phase2_exact_atlas.py; the executed notebook used Floyd–Warshall for integer distances, whereas the script uses integer BFS. The exact interval algorithm was executed, but the committed standalone script has not separately been run in CI. No claim is made that the published caterpillar class matches until the exact paper definition is checked.
