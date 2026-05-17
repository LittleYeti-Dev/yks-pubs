#!/usr/bin/env python3
"""orchestrator-pop-head.py — read maturation-queue.yml + emit (or pop) the head.

Two modes:
  - default (read-only): print head entry as JSON to stdout
  - --commit: pop the head entry from queue and rewrite the file

Skips entries with `enabled: false`. Returns empty (exit 0) when no enabled entries.
"""
import json
import pathlib
import sys

import yaml


def main():
    commit = "--commit" in sys.argv
    path = pathlib.Path("maturation-queue.yml")
    if not path.exists():
        sys.exit(0)

    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    queue = doc.get("queue") or []
    if not isinstance(queue, list) or not queue:
        sys.exit(0)

    # Find first enabled entry (default enabled=True)
    head_index = None
    for i, entry in enumerate(queue):
        if not isinstance(entry, dict):
            continue
        if entry.get("enabled", True) is False:
            continue
        head_index = i
        break

    if head_index is None:
        sys.exit(0)

    head = queue[head_index]

    if commit:
        # Pop the head entry and write back. Preserve comment-leading lines by
        # using the dump_all roundtrip — yaml.safe_dump loses comments but that's
        # acceptable for this file (the seed comment block at the top of the file
        # can be re-added manually or via ruamel.yaml in v2).
        queue.pop(head_index)
        doc["queue"] = queue
        path.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, default_flow_style=False), encoding="utf-8")
        print(f"popped entry: {head.get('slug')} -> {head.get('target_label')}", file=sys.stderr)
    else:
        # Emit head as JSON with all keys defaulted for downstream Actions output
        defaults = {
            "slug": "",
            "transition": "",
            "target_label": "",
            "source_repo": "YKS-Spine-Binder",
            "source_path": "",
            "addendum_path": "",
            "title_suffix": "",
            "tracker": "",
            "doi": "pending",
        }
        defaults.update({k: str(v) if v is not None else "" for k, v in head.items()})
        # Coerce types
        for k in ("slug", "transition", "target_label", "source_repo", "source_path",
                  "addendum_path", "title_suffix", "tracker", "doi"):
            defaults.setdefault(k, "")
            if defaults[k] is None:
                defaults[k] = ""
        # Map "tracker" -> "tracker_issue" naming convention compat
        defaults["tracker_issue"] = defaults.get("tracker", "")
        json.dump({k: v for k, v in defaults.items()}, sys.stdout)


if __name__ == "__main__":
    main()
