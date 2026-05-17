#!/usr/bin/env python3
"""build-doctrine-corpus.py — scrape yks-web frontmatter to assemble doctrine corpus."""
import argparse, pathlib, re, sys

def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m: return None, text
    fm = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, _, v = line.partition(':')
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, text[m.end():]

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
    for md in sorted(base.glob("*.md")):
        slug = md.stem
        if slug == args.exclude_slug: continue
        text = md.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if not fm: continue
        # Pull abstract: prefer frontmatter "description" or first paragraph of body
        abstract = fm.get("description", "") or body.strip().split("\n\n",1)[0]
        entries.append({
            "slug": slug,
            "title": fm.get("title", slug),
            "version": fm.get("version", "?"),
            "series": fm.get("series", "?"),
            "abstract": abstract[:1500],
        })

    out_lines = [f"# YKS doctrine corpus — {len(entries)} papers (auto-scraped from yks-web frontmatter)\n"]
    by_series = {}
    for e in entries:
        by_series.setdefault(e["series"], []).append(e)
    for series, papers in sorted(by_series.items()):
        out_lines.append(f"\n## Series: {series}\n")
        for p in papers:
            out_lines.append(f"\n### {p['title']} (`{p['slug']}` {p['version']})\n")
            out_lines.append(f"{p['abstract']}\n")

    pathlib.Path(args.output).write_text("\n".join(out_lines), encoding="utf-8")
    print(f"wrote {args.output} ({len(entries)} papers)", file=sys.stderr)

if __name__ == "__main__":
    main()
