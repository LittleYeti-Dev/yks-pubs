#!/usr/bin/env python3
"""build-doctrine-corpus.py — scrape yks-web frontmatter to assemble doctrine corpus.

v2 (2026-05-17): replaced the prior regex+`line.partition(':')` frontmatter parser with
yaml.safe_load. The old parser iterated every `:`-containing line in the frontmatter as
a top-level key, so nested YAML (e.g. `series.prior: [{slug, title}, ...]`) overwrote
fm['title'] with the LAST nested title's value. Result: papers whose frontmatter declared
sibling-paper references inherited a sibling's title in the corpus, while their slug stayed
correct — the title↔slug "scramble" Edna refused the 2026-05-17 expansion batch on.

yaml.safe_load preserves nested structure, so `fm['title']` is unambiguously the top-level
title and cannot be polluted by nested blocks. As a defence-in-depth measure the script
now also hard-fails on any paper whose top-level title is missing or empty — a missing
top-level title in a published-or-near-published yks-web frontmatter is itself a data bug.
"""
import argparse, pathlib, sys, yaml

def parse_frontmatter(text):
    """Return (frontmatter_dict_or_None, body_text). Frontmatter is parsed with yaml.safe_load
    so nested keys do not pollute top-level keys (v2 fix for title↔slug scramble)."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 4)
    if end < 0:
        return None, text
    fm_raw = text[4:end]
    body_start = text.find("\n", end + 4)
    body = text[body_start + 1:] if body_start >= 0 else ""
    try:
        fm = yaml.safe_load(fm_raw) or {}
    except yaml.YAMLError as e:
        print(f"WARN: yaml parse failed: {e}", file=sys.stderr)
        return None, body
    if not isinstance(fm, dict):
        return None, body
    return fm, body

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--web-content", required=True, help="path to yks-web/sites/nsq-pub/content/pubs/white-papers")
    p.add_argument("--output", required=True)
    p.add_argument("--exclude-slug", default="", help="don't include this paper (the exemplar)")
    args = p.parse_args()

    base = pathlib.Path(args.web_content)
    if not base.is_dir():
        print(f"ERROR: {base} is not a directory", file=sys.stderr)
        sys.exit(1)

    entries = []
    skipped_no_title = []
    for md in sorted(base.glob("*.md")):
        slug = md.stem
        if slug == args.exclude_slug: continue
        if slug.startswith("_"): continue  # Hugo index files
        text = md.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if not fm: continue
        title = fm.get("title")
        if not title or not isinstance(title, str) or not title.strip():
            skipped_no_title.append(slug)
            continue
        abstract_raw = fm.get("description") or fm.get("abstract") or body.strip().split("\n\n", 1)[0]
        abstract = abstract_raw if isinstance(abstract_raw, str) else str(abstract_raw)
        series = fm.get("series")
        if isinstance(series, dict):
            series = series.get("name", "?")
        elif not isinstance(series, str):
            series = "?"
        entries.append({
            "slug": slug,
            "title": title.strip(),
            "version": str(fm.get("version", "?")),
            "series": series,
            "abstract": abstract.strip()[:1500],
        })

    if skipped_no_title:
        print(
            f"ERROR: {len(skipped_no_title)} papers lack a top-level title field — refusing to "
            f"write a corpus with missing titles. Slugs: {skipped_no_title}",
            file=sys.stderr,
        )
        sys.exit(2)

    out_lines = [f"# YKS doctrine corpus — {len(entries)} papers (auto-scraped from yks-web frontmatter)\n"]
    by_series = {}
    for e in entries:
        by_series.setdefault(e["series"], []).append(e)
    for series, papers in sorted(by_series.items()):
        out_lines.append(f"\n## Series: {series}\n")
        for paper in papers:
            out_lines.append(f"\n### {paper['title']} (`{paper['slug']}` {paper['version']})\n")
            out_lines.append(f"{paper['abstract']}\n")

    pathlib.Path(args.output).write_text("\n".join(out_lines), encoding="utf-8")
    print(f"wrote {args.output} ({len(entries)} papers)", file=sys.stderr)

if __name__ == "__main__":
    main()
