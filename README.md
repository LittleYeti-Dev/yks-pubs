# yks-pubs — Non Sequitur Publishing canonical paper archive

Released PDF artifacts for papers published under the **Non Sequitur Publishing** imprint of Yeti Knowledge Systems.

This repository is the released-artifact archive in the PAPYRUS pipeline. It
does not decide paper identity, maturity, series placement, or source authority.
PAPYRUS/D1 controls workflow state, Zenodo/DOI provides persistent publication
identity, Canon defines maturity, and the PUBS website presents approved state.



## How publishing is controlled

**A PDF push does not mint a DOI.** Building, preserving an existing
publication, and minting a new DOI are separate operations. A GitHub Release
can trigger the connected Zenodo integration, so release creation requires an
exact-PDF intent bound to a durable operator decision and a second explicit
mint confirmation.

### The chain

1. **Build:** `wp-level-up.yml` renders a new version, fails on an existing
   target path, and may place the controlled PDF in `papers/`. It does not mint.
2. **Gate:** PAPYRUS records the release gate, exact source commit/custody,
   25-page floor, 15 verified peer-reviewed sources, current-source floor,
   cross-paper evidence chain, ten-field preflight, and operator decision.
3. **Intent:** a tracked JSON under `release-intents/` binds those receipts to
   one exact PDF hash and the action `mint-new-doi`.
4. **Mint:** the operator manually runs `zenodo-deposit-release.yml` with the
   intent path and `confirm_mint=true`. Only then is a GitHub Release created.
5. **Read back:** after Zenodo resolves, the exact DOI, record, PDF hash,
   metadata, canonical URL, archive, website, citations, and supersession state
   are verified and receipted.

An already-published artifact takes a different path:
`wp-reconcile-existing-publication.yml` downloads the named Zenodo PDF, compares
its SHA-256 with the website mirror, validates identity metadata, and can place
the unchanged PDF plus a reconciliation receipt in this archive. That workflow
cannot mint a DOI and explicitly withholds source custody, series, citation, and
Canon maturity claims.

### Naming convention

`papers/<slug>-v<version>.pdf` where:
- `<slug>` matches the Hugo page slug at `yks-web/sites/nsq-pub/content/pubs/white-papers/<slug>.md`
- `<version>` uses dots for seed releases (`0.1-seed`, `0.1-seed-rev3`) and hyphens for preprints (`1-preprint`, `1.1-preprint`)

The workflow's `parse_pdf_name()` step is the canonical name parser.

### Operational notes

- Release is **fail-closed** — missing intent, hash mismatch, missing source
  custody, insufficient page/source floors, held cross-paper evidence, or a
  false mint confirmation stops before GitHub Release creation.
- Reconciliation is **non-overwriting** — an existing archive target with
  different bytes stops the workflow.
- Release tags remain idempotent; an existing tag is not recreated.
- There is no bulk backfill-to-mint mode. Each DOI action is paper-specific.
- Cross-repo reads require `MESH_TOKEN`; missing access stops reconciliation.
- **The Zenodo-GitHub integration must remain configured** on this repo. If it's removed, DOIs stop minting. Check at: https://zenodo.org/account/settings/github/

### What this repo is NOT for

- Draft or recovered manuscripts (those belong in PAPYRUS at an exact commit)
- Hugo source (that belongs in `yks1.0-web`)
- Maturity rules (those belong in Canon)
- Dynamic paper/workflow state (that belongs in PAPYRUS D1)
- Governing issue history (that belongs in `yks2.0-ops-hub`)

This repo holds released PDFs, prior-version archives, release intents, and
publication/reconciliation receipts. It does not hold the authoritative
editable manuscript.

## Where to find each part of a paper

- **Read it on the site:** https://nonsequitur.tech/white-papers/{slug}/
- **Download the PDF:** `papers/{slug}-v{version}-preprint.pdf` (here) or via the rendered site
- **Cite it:** every paper has a registered DOI on Zenodo (linked from the paper's site page)
- **Author:** Justin H. Kuiper, CISSP — ORCID [0009-0008-7099-3286](https://orcid.org/0009-0008-7099-3286)

## Pipeline position

| Stage | Repo | Visibility | Role |
|---|---|---|---|
| Authoring & R&E | `yks-spine-binder` | private | Manuscript drafting, narrative bibles, ADRs |
| Rendering | `yks-web` (`sites/nsq-pub/`) | private repo, **public site** | Hugo → Cloudflare Pages → nonsequitur.tech |
| **Publication archive** | **`yks-pubs`** | **public** | **Exact released PDFs, prior versions, receipts, and explicitly gated GitHub Releases** |

## Currently published — decalogy P1–P7

All v1.0-preprint as of 2026-04-28:

| # | Slug | Title | Published | DOI |
|---|---|---|---|---|
| P1 | hgc3ae2 | Mitigating Confident Misalignment in Agentic Systems: HGC³AE² Framework | 2026-04-19 | [10.5281/zenodo.19869285](https://doi.org/10.5281/zenodo.19869285) |
| P2 | epistemic-constraints | Epistemic Constraints and Semantic Compression in NLP | 2026-04-22 | [10.5281/zenodo.19869287](https://doi.org/10.5281/zenodo.19869287) |
| P3 | edge-ai-doctrine | Ten Critical Considerations for Edge AI | 2026-04-22 | [10.5281/zenodo.19869289](https://doi.org/10.5281/zenodo.19869289) |
| P4 | agentic-substrate | What an AI System Must Provide Under Governance | 2026-04-25 | [10.5281/zenodo.19869291](https://doi.org/10.5281/zenodo.19869291) |
| P5 | skipjack-protocol | Agile Scrum, Agentics, and the Skipjack Protocol | 2026-04-25 | [10.5281/zenodo.19869293](https://doi.org/10.5281/zenodo.19869293) |
| P6 | alistair-prime-in-a-box | Self-Sufficient Cognitive Systems at the Edge | 2026-04-25 | [10.5281/zenodo.19869307](https://doi.org/10.5281/zenodo.19869307) |
| P7 | operating-model-agentic-teams | Standup, Sprint Planning, Context Discipline (non-human dev team) | 2026-04-25 | [10.5281/zenodo.19869313](https://doi.org/10.5281/zenodo.19869313) |

`TBD` cells populate as Zenodo depositions complete (parent campaign: yks-ops-hub#135).

## *The Implications of Edge Degraded Ops* — v0.1-seed (P1, P2)

A separate 11-paper undecalogy on distributed state at the C5ISR edge. v0.1-seed deposits timestamp the IP claim while the full papers continue in R&E.

| # | Slug | Title | Published | DOI |
|---|---|---|---|---|
| P1 | tactical-substrate | The Tactical Substrate | 2026-05-01 | TBD |
| P2 | hgc3ae2-at-the-degraded-edge | HGC³AE² at the Degraded Edge | 2026-05-01 | TBD |

P3–P11 in R&E pipeline on `yks-spine-binder` (issues #325–#333).

## Forthcoming

The decalogy continues with the capstone arc:

- **P8** — Comprehension Instrument
- **P9** — Operational Plan: Heterogeneous Robo Stack Proof (Dell World 2026-05-21 anchor)
- **P10** — HGC³AE² Reference Architecture

Currently in Edna's R&E pipeline on `yks-spine-binder`.

## License & rights

See [LICENSE](LICENSE) for the rights envelope.

**Summary:** Citation permitted with full attribution. No reproduction, redistribution, derivative works, commercial republication, or AI/ML training use without written permission. Full citation policy at https://nonsequitur.tech/pubs/citation-policy/.

## Author

Justin H. Kuiper, CISSP — `justin@nonsequitur.tech`
ORCID: [0009-0008-7099-3286](https://orcid.org/0009-0008-7099-3286)
