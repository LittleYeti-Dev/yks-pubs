#!/usr/bin/env python3
"""build-standards-compliance-dispatch.py — when a paper fails WP Standards v1.1 gate,
compose a complete Cowork-Edna substantive-expansion dispatch ready for LZ staging.

Inputs (CLI):
  --slug                paper slug
  --current-version     version under review (e.g., v1-1-preprint)
  --target-version      operator's target (e.g., v2-preprint) — the gate this is for
  --transition          the wp-level-up transition that failed
  --pages               current page count (int)
  --pages-required      floor (25 default)
  --paper-pdf           path to current PDF (for SHA + reference)
  --paper-md            path to current source markdown (inlined)
  --doctrine-corpus     path to scraped corpus md (full)
  --canon-foundations   path to canon snapshot md (full)
  --wp-standards        path to wp-publishing-standards md (full)
  --deficits            comma-separated standard ids that failed (e.g., "1,2,5")
  --output              where to write the composed dispatch

The dispatch directs Cowork-Edna (Tier B, operator-attached Opus session) to produce a substantive
v1.x expansion bringing the paper into WP Standards v1.1 compliance.

This is Tier C-gated work: the dispatch produces a draft; operator + Edna two-key approve before
the paper can move to major-revision via wp-level-up.
"""
import argparse, hashlib, pathlib, subprocess, sys
from datetime import datetime, timezone

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--slug", required=True)
    p.add_argument("--current-version", required=True)
    p.add_argument("--target-version", required=True)
    p.add_argument("--transition", required=True)
    p.add_argument("--pages", type=int, required=True)
    p.add_argument("--pages-required", type=int, default=25)
    p.add_argument("--paper-pdf", required=True)
    p.add_argument("--paper-md", required=True)
    p.add_argument("--doctrine-corpus", required=True)
    p.add_argument("--canon-foundations", required=True)
    p.add_argument("--wp-standards", required=True)
    p.add_argument("--deficits", default="1,2,5")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    paper_md = pathlib.Path(args.paper_md).read_text(encoding="utf-8")
    corpus = pathlib.Path(args.doctrine_corpus).read_text(encoding="utf-8")
    canon = pathlib.Path(args.canon_foundations).read_text(encoding="utf-8")
    standards = pathlib.Path(args.wp_standards).read_text(encoding="utf-8")
    pdf_sha = sha256(args.paper_pdf)
    # v2 (2026-05-17) AC-4: per-artifact SHA-256 so the §verifiable-assertions block can be
    # checked against the inlined blocks below. The prior version asserted "canon inlined below"
    # while inlining a literal placeholder string — Edna's 2026-05-17 bounce reason. With AC-1
    # the canon block is now real, and these hashes make the claim machine-checkable downstream.
    paper_md_sha = sha256(args.paper_md)
    corpus_sha = sha256(args.doctrine_corpus)
    canon_sha = sha256(args.canon_foundations)
    standards_sha = sha256(args.wp_standards)
    # Identify the substrate the source markdown came from. wp-level-up.yml v2 may pass either
    # the spine-binder intake draft (for errata-bump / preprint-promote) or the PDF-extracted
    # v1.0-published basis (for major-revision / peer-review-promote). The dispatch must say
    # which substrate Edna is reading so she can decide whether Standard 4 §265 is satisfied.
    substrate_label = ("v1.0-published PDF extract (Standard 4 substrate)"
                       if args.paper_md.endswith("-published-basis.md")
                       else "spine-binder intake draft (preprint/errata substrate)")
    deficit_ids = [d.strip() for d in args.deficits.split(",") if d.strip()]
    pages_gap = max(0, args.pages_required - args.pages)

    dispatch = f"""# Dispatch — Edna (Tier B, Cowork-attached Opus) — Substantive expansion to WP Standards v1.1 compliance

**Filed by:** wp-level-up.yml standards-compliance gate (autonomous)
**Filed:** {today}
**Reason:** `{args.slug}` ({args.current_version}) FAILED WP Standards v1.1 gate when operator attempted `transition: {args.transition}` → `target: {args.target_version}`.

## Standards-compliance verdict

| Standard | Required | Actual | Status |
|---|---|---|---|
| §1 Page floor | ≥{args.pages_required} pages | {args.pages} pages | {'❌ DEFICIT (+' + str(pages_gap) + ' pages owed)' if pages_gap > 0 else '✓ pass'} |
| §2 Chain-of-evidence citations | every YKS-internal cite carries upstream | (not verified) | {'❌ verify owed' if '2' in deficit_ids else '✓ pass'} |
| §3 Additive doctrine | no content removal vs prior | (verify post-compose) | (verify-time) |
| §4 v1.0 publishing-standards basis | format + writing match v1.0 | (verify post-compose) | (verify-time) |
| §5 Citation freshness | ≥3 post-2024 external primary sources | (not verified) | {'❌ verify owed' if '5' in deficit_ids else '✓ pass'} |
| §6 Major-version gate | all §1-§5 must pass for major-revision | failed | ❌ HALT |

Operator's `{args.transition}` request HALTED. Paper cannot advance until standards-pass verified.

## Core ask

Produce a **substantive v1.x expansion** of `{args.slug}` that brings it into WP Standards v1.1 compliance. This is operator-attached Tier B work:

1. **Expand body substance to ≥25 pages.** Currently at {args.pages} pages (gap: +{pages_gap}). Focus on the sections Edna's prior reviews flagged as substance-thin (typically §4 + §6 + sub-sections of letter-walks if the paper uses HGC³AE² structure).

2. **Apply chain-of-evidence citation discipline (WP Standards v1.1 §2).** For every YKS-internal assertion, cite BOTH the YKS source paper AND the upstream non-YKS source it drew from. Form: `[YKS:<slug> v<version> §<section>, citing <author> "<work>" (<year>) <DOI-or-URL>]`. Refuse-on-mismatch if a citation cannot carry the chain.

3. **Verify currency floor (WP Standards v1.1 §5).** At least 3 currently-active (post-2024) primary sources outside the YKS corpus must appear in citations. Surface stale citations (sole anchor >3 years) for refresh.

4. **Preserve v1.0 publishing standards as basis (WP Standards v1.1 §4).** Use the original v1.0 published prose as the substrate — voice fidelity, paragraph rhythm, citation density that matches the v1.0 publishing-quality work. NOT the intake-draft markdown shortcuts.

5. **Additive doctrine (WP Standards v1.1 §3).** Every word of the current {args.current_version} body MUST appear in the expanded version. New substance ADDS — no removals.

## Output

Commit a v{args.current_version.replace('v1-1-preprint','1.2').replace('v1-preprint','1.1').replace('v1-2-preprint','1.3')}-substantive-expansion markdown to `yks-spine-binder/works/non-fiction/white-papers/{args.slug}/release/{args.target_version}/` (or appropriate path based on the existing release layout).

When complete, the operator + Klaus will verify standards-pass and re-fire `wp-level-up.yml` with `transition: {args.transition}` and `target_label: {args.target_version}`.

## Verifiable assertions

Every inlined block below has its SHA-256 stated here. Edna can re-hash any block (paste it
into a fresh file, run `sha256sum`) and verify it matches. If a hash here does not match the
content below, refuse — the dispatch has been tampered with or generated from inconsistent inputs.

- Paper PDF SHA-256: `{pdf_sha}`  (artifact at `{args.paper_pdf}`)
- Source markdown SHA-256: `{paper_md_sha}`  (substrate: {substrate_label}; inlined below)
- WP Standards v1.1 SHA-256: `{standards_sha}`  (inlined below)
- Doctrine corpus SHA-256: `{corpus_sha}`  (inlined below)
- Foundational canon SHA-256: `{canon_sha}`  (inlined below; wp-level-up.yml v2 hard-fails if CANON.md is absent or empty, so this hash is for the real canon, never a placeholder)

---

# Source — current paper markdown

```markdown
{paper_md}
```

---

# WP Publishing Standards v1.1 (PROPOSED — pending operator ratification)

```markdown
{standards}
```

---

# Foundational canon snapshot

```markdown
{canon}
```

---

# Doctrine corpus snapshot

```markdown
{corpus}
```

---

# Execute

Produce the substantive expansion now per WP Standards v1.1. This is Cowork-attached operator-driven work. End with `## Self-check` per persona v1.3 + `## Bench-reality posture` + `## Cross-block consistency`.
"""
    pathlib.Path(args.output).write_text(dispatch, encoding="utf-8")
    print(f"composed standards-compliance dispatch: {args.output} ({len(dispatch)} bytes)", file=sys.stderr)

if __name__ == "__main__":
    main()
