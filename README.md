# yks-pubs — Non Sequitur Publishing canonical paper archive

Canonical PDF artifacts for white papers published under the **Non Sequitur Publishing** imprint of Yeti Knowledge Systems.

This repository is the publication endpoint in the YKS pipeline. It holds only published v1.0+ artifacts — never working drafts, R&E state, or narrative source.



## How publishing fires (the reason this repo exists)

**Drop a PDF → GitHub Release auto-fires → Zenodo mints a DOI.** This repo is the publication endpoint of the YKS pipeline; its sole job is to be the trigger surface for the Zenodo-GitHub integration that has been configured on this repository.

### The chain

1. **PDF lands** in `papers/<slug>-v<version>.pdf` (via PR merge, direct push, or LZ sync from upstream — `yks-spine-binder/works/non-fiction/white-papers/<slug>/release/<version>/<slug>-v<version>.pdf`).
2. **`zenodo-deposit-release.yml`** workflow fires on the push (or via `workflow_dispatch` for backfill). Creates a GitHub Release tagged `<slug>-v<version>` with the PDF as the release asset and a metadata-rich body pulled from the matching `yks-web` Hugo frontmatter (title, abstract, version, slug, live-page URL).
3. **Zenodo-GitHub integration** (pre-configured on this repo — that's the *why* of yks-pubs) detects the new Release, ingests the PDF + Release metadata, and mints a DOI (`10.5281/zenodo.<N>`).
4. **DOI back-stamp** — a downstream step (manual or follow-on workflow) pulls the new DOI and updates the `doi:` + `zenodo_id:` fields on the corresponding `yks-web` Hugo frontmatter. The DOI badge then renders on `nonsequitur.tech/pubs/white-papers/<slug>/`.

### Naming convention

`papers/<slug>-v<version>.pdf` where:
- `<slug>` matches the Hugo page slug at `yks-web/sites/nsq-pub/content/pubs/white-papers/<slug>.md`
- `<version>` uses dots for seed releases (`0.1-seed`, `0.1-seed-rev3`) and hyphens for preprints (`1-preprint`, `1.1-preprint`)

The workflow's `parse_pdf_name()` step is the canonical name parser.

### Operational notes

- The workflow is **idempotent** — re-runs do not double-Release. Releases are keyed off git tag; existing tags are skipped.
- **Backfill mode** — `workflow_dispatch` with `backfill: true` releases every PDF in `papers/` that lacks a matching tag. Use this for catch-up after manual PDF drops.
- **Cross-repo metadata fetch** requires `MESH_TOKEN` repo secret with `yks-web` read access. Without it, Releases still create but with degraded body content (slug-only, no title/abstract).
- **The Zenodo-GitHub integration must remain configured** on this repo. If it's removed, DOIs stop minting. Check at: https://zenodo.org/account/settings/github/

### What this repo is NOT for

- Draft manuscripts (those live in `yks-spine-binder`)
- Hugo source (that's `yks-web`)
- Architecture / process docs (that's `yks-build` / `yks-ops-hub`)

This repo holds **only the final PDFs of published papers** + the workflow that fires their Zenodo deposits. Nothing else.

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
| **Publication archive** | **`yks-pubs`** | **public** | **Final PDFs + GitHub Releases for Zenodo DOI auto-mint** |

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
