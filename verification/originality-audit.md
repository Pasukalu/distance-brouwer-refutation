# Originality audit

**Date:** 2026-11-26. **Method:** Crossref REST API, OpenAlex, Semantic Scholar, Unpaywall, zbMATH Open API, arXiv API, publisher pages. MathSciNet and Google Scholar require authenticated access and were **not** searched; the audit below is therefore not exhaustive, and no statement here should be read as a certified novelty claim.

## 1. The two inequalities and their provenance

| Item | Source | Verified facts |
|---|---|---|
| Signless inequality $M_k^Q(G)\le W(G)+\binom{k+2}{3}$ | Alhevaz, Baghipur, Ganie, Pirzada, *Linear Multilinear Algebra* **69**(13) (2021) 2423–2440, DOI `10.1080/03081087.2019.1679074` | Metadata verified. **Full text is paywalled** (Unpaywall: `is_oa=false`, no repository copy; T&F returned 403). Abstract (Semantic Scholar + OpenAlex): the authors obtain bounds for $M_k$ and $N_k$ in terms of $n$ and the transmission, "propose a Brouwer-type conjecture for $M_k(G)$", and "show that it holds for graphs of diameter one and graphs of diameter two for all $k$", plus $k=n-1,n$ for all graphs and some results for $r$-transmission-regular graphs. **The exact final conjecture could not be read.** |
| Laplacian inequality $U_r(G)\le W(G)+\binom{r+2}{3}$ | Zhou, Wang, Chai, *Comput. Appl. Math.* **44**(3) (2025), **article 138**, DOI `10.1007/s40314-025-03095-0` | Metadata verified via Crossref (title, authors, volume, issue, article number, date 2025-01-25). Full text not accessed. |
| Same Laplacian inequality, diameter 3/4 case | Zhang, Wang, Miao, *J. Comb. Optim.* **52**(5) (2026), **article 53**, DOI `10.1007/s10878-026-01488-3`, published 2026-11-11 | Metadata verified via Crossref. |
| Distance-Laplacian analog, prior refutation | Huang, *AIMS Math.* **11**(10) (2026) 33617–33633, DOI `10.3934/math.20261314`, arXiv:2606.06945 | Metadata verified via Crossref. The manuscript's own summary of Huang's theorem lists the exceptions $K_{1,3}$ ($r=2$) and $K_{1,4}$ ($r=3$), i.e. **the Laplacian inequality was already known to fail**. |
| Uniform caterpillars | Alali, Rani, Mir, Nisar, *AIMS Math.* **11**(5) (2026) 15199–15214, DOI `10.3934/math.2026625` | Metadata verified via Crossref. |
| Brouwer's Laplacian conjecture (background) | Kothari, Tudose, arXiv:2606.12197 | Preprint; cited as "On Brouwer's Laplacian conjecture" (the earlier manuscript entry with different authors/title was corrected). Status of the claimed proof not independently assessed. |
| Signless-Laplacian (ordinary, not distance) Brouwer conjecture | arXiv:2609.31355 | Preprint, abstract indexed. **Not the same object** as the distance signless inequality; cite only as background, not as prior art on the distance inequality. |

## 2. What is genuinely new (as far as these searches reach)

1. **Simultaneous $\Theta(n^3)$ asymptotic refutation** of the two *distance* inequalities on three explicit infinite families, with the constant $\left(\tfrac{\sqrt3}{2}-\tfrac56\right)\approx0.032692$ obtained from Schur diagonal majorization. No prior publication with this asymptotic statement was found. *Caveat:* the Laplacian-side refutation itself is Huang's (2026); what is new here is the asymptotic mechanism and the signless-side families.
2. **Exhaustive $n\le7$ census** (994 connected graphs, orders 3–7) with **exact rational Ky Fan certificates** for the minimal examples and a diameter-based phase transition (all 9 diameter-5 non-path graphs violate both inequalities; 0/994 violate the corrected bound). Exhaustive small-order counterexample tables for these two matrices were not found in the literature.
3. **Corrected universal bound** $U_r(G),M_r^Q(G)\le W(G)+D\binom{r+1}{2}$ for all connected graphs, with $0$ violations on the census and $0$ on 3,600 random graphs ($n\le13$). A bound with the diameter factor is, to our search, not previously stated.
4. **Lean 4 formalization** of the integer certificates, the scaled Bessel/majorization core lemma and the three family inequalities. The scope is arithmetic, not the real spectral theorem; the manuscript now says so.

## 3. What is not new

- The fact that the **distance Laplacian** inequality fails: **Huang (2026)**, and the small exceptions $K_{1,3}$, $K_{1,4}$ were already known to him. This repository must not claim that refutation.
- The two inequalities themselves, their motivation from Brouwer's conjecture, and the diameter-1/2 verification: Alhevaz et al. (2021) and Zhou–Wang–Chai (2025).
- The $W(G)+\binom{r+2}{3}$ shape of the bound and the Ky Fan/Rayleigh technique: classical.

## 4. Priority risks

| Risk | Evidence | Mitigation |
|---|---|---|
| Signless counterexamples may be predated | Full text of ABGP (2021) unread; PR #2 asserts §4 already lists $k=3,4$ counterexamples, possibly of a different inequality | Obtain the PDF and quote §4; if their final conjecture differs, rename our object as "the inequality of [ABGP, §?]" and drop "conjecture" language |
| Laplacian refutation priority | Huang (2026) already has explicit exceptions | Manuscript now says "we extend"; keep that framing in title/abstract |
| Signless literature review incomplete | MathSciNet/Scholar unavailable; zbMATH API returns metadata only | Before submission: one human MathSciNet/zbMATH search by an authenticated author; record the query and date in the paper's "Note added" |

## 5. Verdict

The repository contains real, independently reproducible mathematics. Its **defensible contribution** is: (i) the asymptotic $\Theta(n^3)$ family analysis for both inequalities, (ii) the exhaustive $n\le7$ census with exact certificates, (iii) the corrected diameter-penalty bound, (iv) an honest arithmetic formalization. It is **not** the first refutation of the distance Laplacian inequality, and its claim to refute "the Alhevaz conjecture" is contingent on a text that could not be verified. Both caveats are now stated in the repository; resolving §4 is the last blocking item for submission.
