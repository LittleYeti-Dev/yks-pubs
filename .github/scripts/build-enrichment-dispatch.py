#!/usr/bin/env python3
"""build-enrichment-dispatch.py — compose an Edna backward-enrichment dispatch.

Inputs (from env or argv):
  --slug       e.g., hgc3ae2-at-the-degraded-edge
  --paper-pdf  path to the paper PDF (extracted to text inline)
  --corpus     path to doctrine-corpus.md (scraped from yks-web frontmatter)
  --canon      path to canon-foundations.md (concatenated yks-canon CANON.md + paper-drafting-chain + register)
  --output     where to write the composed dispatch markdown

Output: a dispatch-edna-{slug}-doctrine-enrichment-{date}.md ready to drop into yks-ops-hub/execute/lz/.
"""
import argparse, hashlib, pathlib, subprocess, sys
from datetime import datetime, timezone

def extract_pdf_text(pdf_path):
    """Use pdftotext (poppler-utils) to extract paper body text."""
    out = subprocess.run(["pdftotext", "-layout", str(pdf_path), "-"], capture_output=True, check=True)
    return out.stdout.decode("utf-8", errors="replace")

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--slug", required=True)
    p.add_argument("--paper-pdf", required=True)
    p.add_argument("--corpus", required=True)
    p.add_argument("--canon", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--current-version", default="v1-preprint",
                   help="Current published version of the paper (e.g., v1-preprint, v1-1-preprint)")
    args = p.parse_args()

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    paper_text = extract_pdf_text(args.paper_pdf)
    corpus_text = pathlib.Path(args.corpus).read_text(encoding="utf-8")
    canon_text = pathlib.Path(args.canon).read_text(encoding="utf-8")
    paper_sha = sha256(args.paper_pdf)

    dispatch = f"""# Dispatch — Edna (Tier A, Opus) — Backward-enrichment, {args.slug} vs complete doctrine

**Filed by:** wp-framework-uplift (autonomous)
**Date:** {today}
**Tracker:** framework-uplift cycle for `{args.slug}` (operator-gated: produces v1.x errata addendum draft; canon mint requires operator-fired errata-bump)
**Verifiable assertion:** Paper SHA-256 = `{paper_sha}` (source: yks-pubs/papers/{args.slug}-{args.current_version}.pdf)

## Task framing

This is a **backward-enrichment review** triggered by the framework-uplift transition in wp-framework-uplift.yml. You receive:

1. The **exemplar** — the paper named in this dispatch's slug, currently at {args.current_version}.
2. The **complete YKS doctrine corpus** — every currently-published paper across every series, frontmatter inlined.
3. The **foundational canon** — yks-canon governance + framework documents.

Your job has three movements, in order, exactly as your editorial discipline specifies:

### Movement 1 — Connecting-dots identification
Identify every load-bearing concept in the doctrine that was introduced AFTER the exemplar was published and which now provides retrospective context the exemplar should reference. Cite each connecting dot with specific later-paper slug + version and the specific section/claim in the exemplar it lands against.

### Movement 2 — Retrofit prose with insertion points
For each connecting dot worth retrofitting, produce exact prose to insert into the exemplar. Each retrofit:
- **Insertion target** (section heading + before/after sentence + ~10 words anchor text)
- **Anchor sentence** (existing sentence in exemplar)
- **Replacement / insertion prose** (new text)
- **Rationale** (which later paper + why this dot is load-bearing)

Use `[FORWARD — see <slug> v<version>]` notation for cross-references.

### Movement 3 — Future-study candidates
List 5-10 candidate white papers the comparison surfaces as gaps. Each candidate:
- Working title
- Gap it closes
- Series fit (or new series)
- 2-3 sentence rationale grounded in specific corpus citations

## Constraints

- Honest citations only. No invented papers or DOIs.
- Refuse-on-mismatch with `INCOMPLETE: <reason>` if inputs are malformed.
- This is NOT a canon mint. Your work product is a **draft** for operator review. The v1.x bump itself is operator-gated (Tier C invariant).
- Output the standard persona-prompt-required sections + Movement 1, 2, 3.

---

# Exemplar — {args.slug} ({args.current_version})

```text
{paper_text}
```

---

# Complete YKS doctrine corpus

```markdown
{corpus_text}
```

---

# Foundational canon

```markdown
{canon_text}
```

---

# Execute

Produce the three-movement output now per your editorial discipline.
"""
    pathlib.Path(args.output).write_text(dispatch, encoding="utf-8")
    print(f"wrote {args.output} ({len(dispatch)} bytes; paper sha {paper_sha[:12]})", file=sys.stderr)

if __name__ == "__main__":
    main()
