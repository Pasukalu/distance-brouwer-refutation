# Submission-readiness report

**Date:** 2026-11-26. Venue facts were gathered from official pages on this date by a delegated source audit; pages behind Cloudflare/403 are marked **unverified**. Nothing in this report constitutes a submission, an endorsement, or a claim about acceptance probability.

## 1. Positioning

- **Primary object:** distance (signless) Laplacian eigenvalue sums, Brouwer-type bounds, counterexamples, exhaustive census $n\le7$, corrected diameter-penalty bound, asymptotic $\Theta(n^3)$ families.
- **Secondary object:** Lean 4 arithmetic formalization of the certificates and family inequalities.
- **Honest headline:** "A diameter-penalty correction for distance-Laplacian Brouwer-type inequalities, with an exhaustive $n\le7$ census and an asymptotic $\Theta(n^3)$ family analysis." Do **not** headline it as "disproving the Alhevaz conjecture" until §4 of Alhevaz et al. has been read (see `originality-audit.md`, R6).

## 2. Preprint plan

| Platform | Category / licence | Notes |
|---|---|---|
| **arXiv** | primary `math.CO`, cross-list `math.SP` | Official category text: math.CO covers "graph theory, enumeration"; math.SP covers "discrete models, numerical studies". Endorsement required for a first submission in a category (2025–26 rules: institutional email **and** prior authorship, or personal endorsement). Moderation is not peer review. Licence options include CC BY 4.0 (irrevocable). arXiv AI policy (official): report significant generative-AI use in the work; authors take full responsibility; AI cannot be an author. |
| **HAL** | `math.CO`, "Prépublication" | Manual validation of every file; since Feb 2026 a reuse licence is mandatory for each file (CC BY recommended); no AI-disclosure requirement found at repository level (**unverified** absence). Can be transferred to arXiv. |
| **Zenodo** | Software/Dataset record for the Lean project + census data | DOI minted; a licence must be specified for public files; metadata CC0; uploader responsible for content. Repository-level AI notice concerns Zenodo's own AI use, not authors'. |

Recommended sequence: arXiv (CC BY 4.0) → Zenodo DOI for code/data → journal submission with the DOI in the data-availability statement.

## 3. Journal shortlist (fit for this paper)

| Rank | Journal | Publisher | ISSN | Fit | OA / APC | Data status |
|---|---|---|---|---|---|---|
| 1 | Linear Algebra and its Applications | Elsevier | 0024-3795 | Natural home for distance-Laplacian/Brouwer-type matrix results | hybrid | metadata only (**unverified** scope/APC) |
| 2 | Linear and Multilinear Algebra | Taylor & Francis | 0308-1087 / 1563-5139 | Published the original signless paper; matrix-analysis readership | hybrid | metadata only (**unverified**) |
| 3 | Discrete Applied Mathematics | Elsevier | 0166-218X | Graph theory + computation, suits census/counterexamples | hybrid | metadata only (**unverified**) |
| 4 | Graphs and Combinatorics | Springer | 0911-0119 / 1435-5914 | Spectral graph theory with explicit counterexamples | hybrid | metadata only (**unverified**) |
| 5 | Electronic Journal of Combinatorics | editorial board (ANU) | 1077-8926 | Free, refereed, no page limit, publishes spectral graph theory | diamond OA, no APC | verified |
| 6 | Ars Mathematica Contemporanea | University of Primorska Press | 1855-3966 / 1855-3974 | Discrete math favouring work that combines fields (spectral + computation + formalization); formal research-data policy | diamond OA, CC BY 4.0 | verified |
| 7 | Special Matrices | De Gruyter Brill | 2300-7451 | Scope explicitly lists "spectral graph theory" and "combinatorial matrix theory" | OA, APC €1050 | verified |
| 8 | Experimental Mathematics | Taylor & Francis | 1058-6458 / 1944-950X | Computer-assisted/counterexample papers | hybrid | metadata only (**unverified**) |

Notes: **Electronic Journal of Linear Algebra** fits well but has suspended new submissions from 2026-11-03 until at latest February 2027 (official announcement) — not usable now. **MATCH** requires a chemistry connection (not applicable). **Journal of Symbolic Computation** is a poor fit: Lean formalization is not symbolic computation.

## 4. AI-use disclosure requirements (verified from official pages)

| Publisher / venue | AI drafting allowed | AI as author | Required disclosure |
|---|---|---|---|
| Elsevier | Yes, with human critical thinking | No | Separate **AI declaration statement** at submission, naming tool, purpose, extent of oversight; published with the article |
| Springer Nature | Yes, with accountability | No (LLMs do not meet authorship criteria) | **AI Use Declaration** at end of paper + Methods section if AI was used in research |
| Taylor & Francis | Yes, responsibly; some journals restrict to language editing | No | In-article statement with full tool name and version, how and why used |
| AIMS Press | Yes; content must be human-reviewed | No (follows COPE) | Disclosure not mandatory for purely assistive tools, but AI-generated content must be revealed; full wording should be re-checked live (**unverified** rendering) |
| AMS journals | Yes | No | Materials and Methods (or similar) describing how and which tool |
| EJC | Yes, if proofs are human-checked/rewritten | No | Journal AI policy; "papers mostly written by AI without thorough checking will not be accepted" |
| ELA | Yes, acknowledge recommended | No | Acknowledgements |
| ALCO | Yes, disclose unless clerical | No | In-paper disclosure (Leiden Declaration) |
| arXiv | Yes | No | Report significant generative-AI use in the work |

For this repository the honest statement is: the manuscript, code and formalization were produced with substantial AI assistance, every mathematical claim was independently re-derived or computationally reproduced by the authors, and all references were checked against Crossref/arXiv records on 2026-11-26. A draft disclosure paragraph is in `paper/paper_en.tex` §"Statements".

## 5. Pre-submission checklist

- [x] Independent census reproduction (994 graphs; counts match; script `verification/phase3_independent.py`)
- [x] Exact certificate verification (all six, orthogonality + strict inequality)
- [x] Corrected-bound stress test (0 failures on 994 + 3,600 graphs; min margin 9.71)
- [x] $\Theta(n^3)$ family check for $n\le150$; constant consistent
- [x] Bibliography metadata verified against Crossref (4 entries corrected)
- [x] Lean build green in CI; 18 axiom prints; no `sorryAx`; hygiene check added
- [x] Independent reports (this file, peer review, originality, formalization coverage)
- [ ] **Read Alhevaz et al. §4** (institutional access) and finalise conjecture language
- [ ] Rebuild PDFs and re-release (v1.1.0)
- [ ] Author identity, affiliation, ORCID, corresponding author and licence decision — **requires the human author's confirmation**
- [ ] AI-use disclosure text approved by the human author
- [ ] MathSciNet/zbMATH authenticated search recorded in a "Note added" paragraph

## 6. Blockers before actual submission

1. **Conjecture provenance (R6)** — the only substantive scientific blocker.
2. **Author metadata** — cannot be invented; must come from the human author.
3. **Licence choice** — repository is MIT; arXiv/Zenodo licence must be chosen by the author (CC BY 4.0 recommended for the preprint; note that einige publishers require copyright transfer and MIT/CC BY is compatible with green OA).
4. **Venue-specific formatting** — EJC/AMC/Special Matrices have their own classes; plan one day of reformatting after acceptance.

## 7. What this phase deliberately did not do

No submission was made, no DOI was minted, no author statement was signed, and no claim about journal acceptance is made. Those steps require the human author's confirmation, as instructed.
