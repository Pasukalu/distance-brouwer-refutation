# Open lead: a sharper (conditional) diameter bound

**Status: conjecture-level lead, not a theorem.** Nothing here is claimed in the paper. It is recorded because the computation is reproducible and the shape of the bound is plausible; a rigorous derivation has not been verified.

## Candidate inequalities

For every connected graph $G$ of order $n\ge2$, diameter $D$, and $1\le r\le n$,

$$U_r(G)\ \le\ W(G) + (D-1)\binom{r+1}{2} + n\min(r,n-1) - \binom{n}{2},$$
$$M_r^{Q}(G)\ \le\ W(G) + (D-1)\binom{r+1}{2} + n + (n-2)r - \binom{n}{2}.$$

Both right-hand sides are $\le W(G) + D\binom{r+1}{2}$ (with equality at $r=n-1$ for the first), so they would strictly improve the corrected theorem of the manuscript for $r<n-1$.

## Where the shape comes from

Write the distance Laplacian as $D^L=(nI-J)+\sum_{s\ge2}L(Y_s)$, where $Y_s$ joins pairs at distance $\ge s$ (the decomposition already used in the paper, due to Huang). The term $nI-J$ contributes $n\min(r,n-1)$ to a sum of $r$ largest eigenvalues (and $\binom{n}{2}$ of the "complete graph" mass is already counted in $W$), while $\sum_s m(Y_s)=W-\binom{n}{2}$. Applying the ordinary Brouwer inequality $S_r(H)\le m(H)+\binom{r+1}{2}$ to each $Y_s$ and Ky Fan subadditivity gives the first display. The signless case uses the analogous ordinary signless Brouwer bound on $(n-2)I+J$ and the $Q(Y_s)$.

**Every step after "apply ordinary Brouwer" is unverified.** In particular: (i) the constant bookkeeping for $nI-J$ at $r=n$; (ii) whether $Y_s$ is always connected or whether the Brouwer bound applies to each component separately; (iii) the derivation is conditional on the 2026 preprints that prove the ordinary Brouwer inequalities (Kothari–Tudose, arXiv:2606.12197; Yuan–Zhang, arXiv:2609.31355).

## Computational evidence (2026-11-27)

Script: `verification/phase3_independent.py` (`sharper_candidates`, `sharper_bound_stress`).

| Domain | Failures | Notes |
|---|---|---|
| All 994 census graphs, all $r$ | 0 | Several exact equality cases (`margin = 0`): e.g. $L$ at $(n,r)=(6,2)$, $(7,2)$, $(7,4)$, $(7,5)$ |
| 4,900 random connected graphs, $8\le n\le14$ (half random trees) | 0 | no equality; smallest slack $0.5858$ at $(n,r)=(8,4)$ |

The census equality cases are the reason this is a lead rather than a discarded idea: a bound that is attained on several small graphs is usually the "right" shape. But equality also means a proof must handle those cases exactly, and a counterexample one step outside the tested range would kill it.

## What would close the lead

1. Re-derive the constant for $nI-J$ at $r=n$ and for disconnected $Y_s$ (if any), component by component.
2. Prove the ordinary Brouwer inequality unconditionally, or restate the result as conditional on the 2026 preprints.
3. Extend the random search to $n=15..18$ and to all trees of order $\le 12$ (exhaustive tree generation is cheap).
4. If it survives, add it as a theorem (with the equality characterisation) or as a remark with explicit hypotheses.
