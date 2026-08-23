# Operator release intents

A GitHub Release in this repository can trigger the connected Zenodo DOI
integration. For that reason, a PDF landing in `papers/` is not release
authority and does not mint by itself.

Before running `zenodo-deposit-release.yml`, create one tracked JSON intent for
one exact PDF. Copy `release-intent.template.json`, fill every field, replace
the placeholder SHA-256 with the hash of the final PDF, and cite the durable
operator decision. The workflow validates the record and the PDF bytes before
it creates a release.

Rules:

- one intent authorizes one paper version and one exact PDF hash;
- the path must be `papers/<slug>-<version_label>.pdf`;
- `publication_action` must be `mint-new-doi`;
- a reconciliation of an already-published DOI never uses this intent;
- editing a PDF after approval invalidates the intent;
- the bound manuscript has at least 25 substantive pages, 15 verified
  peer-reviewed sources, three verified post-2024 primary sources, and one
  outbound cross-paper reference with a passing chain-of-evidence gate;
- the exact editable source is retained in `LittleYeti-Dev/papyrus-factory-recurring`
  at the recorded commit, whether it is
  the original controlled source or a transparently recovered and verified source;
- the PAPYRUS release gate, validation receipt, and ten-field preflight are
  durable and named;
- a green build, review, or validator does not replace operator authority;
- the workflow still requires the human dispatcher to set `confirm_mint=true`.

The final publication receipt—DOI, Zenodo record, canonical URL, hash, author,
version/date, rights, archive, website readback, citations, and supersession
state—is recorded separately after DOI resolution and exact-file readback.
