#!/usr/bin/env python3
"""parse-edna-movements.py — extract Movement 2 retrofits + Movement 3 candidates from Edna work product.

Inputs:
  --work-product  path to Edna's .work.md file
  --slug          paper slug (for filename derivation)
  --output-dir    directory to write parsed outputs

Outputs:
  movement-2-retrofits.md  — extracted retrofit blocks as a single addendum draft
  movement-3-candidates.json  — array of {title, gap, series_fit, rationale} for issue filing
  movement-2-count.txt       — integer count
  movement-3-count.txt       — integer count
"""
import argparse, json, pathlib, re, sys

def extract_movement(text, n):
    """Extract one of the three Movements (1, 2, 3) by header detection."""
    pat = re.compile(rf"^##\s*Movement\s+{n}\b.*?$", re.MULTILINE)
    m = pat.search(text)
    if not m: return ""
    start = m.end()
    # End at the next "## " top-level header (any number) or EOF
    end_pat = re.compile(r"^##\s+(?!Movement\s*\d|$)", re.MULTILINE)
    end_m = end_pat.search(text, pos=start)
    return text[start:end_m.start() if end_m else len(text)].strip()

def parse_retrofits(m2_text):
    """Parse Movement 2 into individual retrofit blocks.
    Each retrofit starts with '### R' or '### Retrofit' marker."""
    parts = re.split(r"^###\s+(?:R\d+|Retrofit\s+R\d+|D\d+→R\d+)\b", m2_text, flags=re.MULTILINE)
    retrofits = []
    for i, p in enumerate(parts[1:], start=1):
        p = p.strip()
        if not p: continue
        # First line is typically the retrofit title; rest is the block
        retrofits.append(p)
    return retrofits

def parse_candidates(m3_text):
    """Parse Movement 3 into individual candidate blocks. Each starts with '### F' or '### Candidate'."""
    parts = re.split(r"^###\s+(?:F\d+|Candidate\s+F?\d+|C\d+)\b", m3_text, flags=re.MULTILINE)
    candidates = []
    for p in parts[1:]:
        p = p.strip()
        if not p: continue
        # Extract title (first line, often after a long-dash separator)
        first_line = p.split("\n",1)[0]
        # Title: text after the first "—" if present, else the first line itself
        title = first_line.split("—",1)[-1].strip(" *_")
        # Pull "Gap closes" + "Series fit" + "Rationale" lines if present
        gap = re.search(r"\*\*Gap closes:\*\*\s*(.+?)(?=\n\*\*|\Z)", p, re.DOTALL)
        series = re.search(r"\*\*Series fit:\*\*\s*(.+?)(?=\n\*\*|\Z)", p, re.DOTALL)
        rationale = re.search(r"\*\*Rationale:\*\*\s*(.+?)(?=\n\*\*|\Z|\n###)", p, re.DOTALL)
        candidates.append({
            "title": title or "(untitled)",
            "gap_closed": (gap.group(1).strip() if gap else "(not specified)"),
            "series_fit": (series.group(1).strip() if series else "(not specified)"),
            "rationale": (rationale.group(1).strip() if rationale else p[:500]),
        })
    return candidates

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--work-product", required=True)
    p.add_argument("--slug", required=True)
    p.add_argument("--output-dir", required=True)
    args = p.parse_args()

    text = pathlib.Path(args.work_product).read_text(encoding="utf-8")
    outdir = pathlib.Path(args.output_dir); outdir.mkdir(parents=True, exist_ok=True)

    m2 = extract_movement(text, 2)
    m3 = extract_movement(text, 3)

    retrofits = parse_retrofits(m2)
    candidates = parse_candidates(m3)

    # Write Movement 2 addendum draft
    addendum = f"""# v1.1 Errata addendum — backward-enrichment retrofits

**Source:** automated extraction from Edna backward-enrichment review.
**Status:** DRAFT — operator review required before canon mint.
**Movement 2 retrofit count:** {len(retrofits)}

The following retrofit insertions are proposed for v1.1 errata. Each preserves the original paper's voice and extends its argument with forward-reference notation to subsequently-published doctrine. The operator-fired `errata-bump` transition will compose these into the v1.1 PDF and mint a new Zenodo DOI.

---

{m2}

---

## Operator review checklist

- [ ] Review each retrofit insertion for voice fidelity
- [ ] Verify all `[FORWARD — see <slug> v<version>]` citations resolve to real published papers
- [ ] Optionally trim/edit retrofits before firing errata-bump
- [ ] Fire `wp-level-up` with `transition: errata-bump` to compose v1.1 PDF + mint DOI
"""
    (outdir / "movement-2-addendum-draft.md").write_text(addendum, encoding="utf-8")
    (outdir / "movement-3-candidates.json").write_text(json.dumps(candidates, indent=2), encoding="utf-8")
    (outdir / "movement-2-count.txt").write_text(str(len(retrofits)), encoding="utf-8")
    (outdir / "movement-3-count.txt").write_text(str(len(candidates)), encoding="utf-8")

    print(f"Movement 2 retrofits parsed: {len(retrofits)}", file=sys.stderr)
    print(f"Movement 3 candidates parsed: {len(candidates)}", file=sys.stderr)

if __name__ == "__main__":
    main()
