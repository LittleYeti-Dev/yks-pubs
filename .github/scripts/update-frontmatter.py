#!/usr/bin/env python3
"""update-frontmatter.py — point a Hugo paper's frontmatter at the new version.

Called by wp-pubs-site-mirror.yml after the new PDF has been copied into
yks-web/sites/nsq-pub/static/papers/. Updates these fields:
  - version: derived from target_label (e.g. v1-1-preprint -> 1.1-preprint)
  - doi: the supplied DOI, or "PENDING-ZENODO-MINT" if input was "pending"
  - zenodo_id: trailing portion of the DOI, or "" if pending
  - pdf: /papers/<slug>-<target_label>.pdf
  - prior_versions: prepend a record of the version we're replacing

Usage:
  update-frontmatter.py <fm_path> <target_label> <doi> <slug>
"""
import re
import sys
import pathlib
import yaml


def main():
    if len(sys.argv) != 5:
        print("usage: update-frontmatter.py <fm_path> <target_label> <doi> <slug>", file=sys.stderr)
        sys.exit(2)

    fm_path = pathlib.Path(sys.argv[1])
    target_label = sys.argv[2]
    doi = sys.argv[3]
    slug = sys.argv[4]

    if not fm_path.exists():
        print(f"FATAL: frontmatter not at {fm_path}", file=sys.stderr)
        sys.exit(1)

    text = fm_path.read_text(encoding="utf-8")
    m = re.match(r"---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if not m:
        print(f"FATAL: no frontmatter delimiters in {fm_path}", file=sys.stderr)
        sys.exit(1)

    fm = yaml.safe_load(m.group(1)) or {}
    body = m.group(2)

    # Preserve current version as a prior_versions entry
    prior_versions = list(fm.get("prior_versions") or [])
    current_pv = {
        "version": fm.get("version", ""),
        "doi": fm.get("doi", ""),
        "pdf": fm.get("pdf", ""),
        "published_date": fm.get("published_date") or fm.get("date", ""),
    }
    prior_versions.insert(0, current_pv)

    # Compute new version string from target_label
    # e.g. v1-1-preprint -> 1.1-preprint
    new_version = re.sub(r"^v", "", target_label)
    # Replace the first hyphen separating the version number with a dot
    parts = new_version.split("-", 2)
    if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
        # e.g. ['1','1','preprint'] -> '1.1-preprint'
        new_version = f"{parts[0]}.{parts[1]}" + (f"-{parts[2]}" if len(parts) > 2 else "")
    elif len(parts) == 2 and parts[0].isdigit() and not parts[1].isdigit():
        # e.g. ['1','preprint'] -> '1.0-preprint' (treat single-digit version as N.0)
        new_version = f"{parts[0]}.0-{parts[1]}"

    fm["version"] = new_version

    if doi and doi.lower() not in ("pending", ""):
        fm["doi"] = doi
        # Extract trailing numeric id from DOI like 10.5281/zenodo.NNNNN
        zid_match = re.search(r"zenodo\.(\d+)$", doi)
        fm["zenodo_id"] = zid_match.group(1) if zid_match else doi.rsplit("/", 1)[-1]
    else:
        fm["doi"] = "PENDING-ZENODO-MINT"
        fm["zenodo_id"] = ""

    fm["pdf"] = f"/papers/{slug}-{target_label}.pdf"
    fm["prior_versions"] = prior_versions

    out = (
        "---\n"
        + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False, default_flow_style=False)
        + "---\n"
        + body
    )
    fm_path.write_text(out, encoding="utf-8")
    print(
        f"frontmatter updated: version={new_version} doi={fm['doi']} "
        f"pdf={fm['pdf']} prior_versions={len(prior_versions)}"
    )


if __name__ == "__main__":
    main()
