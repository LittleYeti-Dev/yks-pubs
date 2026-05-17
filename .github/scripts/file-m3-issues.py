#!/usr/bin/env python3
"""file-m3-issues.py — file Movement 3 future-study candidates as yks-spine-binder issues.

Reads JSON array from movement-3-candidates.json and creates one issue per entry
in yks-spine-binder via GitHub API. Outputs newline-separated issue refs to stdout.
"""
import argparse, json, os, sys, urllib.request, urllib.error

def file_issue(candidate, slug, token, dry_run=False):
    body = (
        f"**Filed by:** wp-framework-uplift (autonomous Movement 3 extraction from "
        f"`{slug}` backward-enrichment review)\n"
        f"**Type:** future-study candidate\n\n"
        f"## Working title\n{candidate['title']}\n\n"
        f"## Gap closed\n{candidate['gap_closed']}\n\n"
        f"## Series fit\n{candidate['series_fit']}\n\n"
        f"## Rationale\n{candidate['rationale']}\n\n"
        f"## Provenance\n"
        f"- Source: framework-uplift cycle for `{slug}`\n"
        f"- Extracted from: Edna Movement 3 future-study analysis\n"
        f"- Operator review required before drafting authorization\n"
    )
    title = f"wp:signal — {candidate['title'][:80]}"
    payload = {
        "title": title,
        "body": body,
        "labels": ["kind:wp-signal", "source:framework-uplift", f"paper:{slug}"],
    }
    if dry_run:
        print(f"[dry-run] would file: {title}", file=sys.stderr)
        return None
    req = urllib.request.Request(
        "https://api.github.com/repos/LittleYeti-Dev/yks-spine-binder/issues",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read())
            return d.get("number"), d.get("html_url")
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code} for '{title}': {e.read().decode()[:200]}", file=sys.stderr)
        return None, None

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--candidates-json", required=True)
    p.add_argument("--slug", required=True)
    p.add_argument("--token", default=os.environ.get("GH_TOKEN") or os.environ.get("MESH_TOKEN", ""))
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    if not args.token and not args.dry_run:
        print("ERROR: no GH_TOKEN/MESH_TOKEN", file=sys.stderr)
        sys.exit(2)

    candidates = json.load(open(args.candidates_json))
    print(f"Filing {len(candidates)} issues for slug={args.slug}", file=sys.stderr)
    filed = []
    for c in candidates:
        num, url = file_issue(c, args.slug, args.token, args.dry_run)
        if num:
            filed.append(f"yks-spine-binder#{num}")
            print(f"  filed #{num}: {c['title'][:60]}", file=sys.stderr)
    # stdout: comma-separated refs for shell consumption
    print(",".join(filed))
    print(f"Filed {len(filed)} of {len(candidates)} issues", file=sys.stderr)

if __name__ == "__main__":
    main()
