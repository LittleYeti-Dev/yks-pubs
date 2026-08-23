#!/usr/bin/env python3
"""Create a source-bound, non-release PAPYRUS PDF build receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse


PAPER_ID_RE = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)+$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_RE = re.compile(r"^v[0-9]+(?:[.-][0-9]+)*(?:-[a-z0-9]+)*$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


class BuildReceiptError(ValueError):
    pass


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def validate_relative_path(value: str, field: str) -> None:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise BuildReceiptError(f"{field} must be a bounded relative path")


def validate_commit(value: str, field: str) -> None:
    if not COMMIT_RE.fullmatch(value):
        raise BuildReceiptError(f"{field} must be a full Git commit SHA")


def build(args: argparse.Namespace) -> dict:
    if not PAPER_ID_RE.fullmatch(args.paper_id):
        raise BuildReceiptError("invalid PAPYRUS paper_id")
    if not SLUG_RE.fullmatch(args.slug):
        raise BuildReceiptError("invalid canonical slug")
    if not VERSION_RE.fullmatch(args.target_version):
        raise BuildReceiptError("invalid target version")
    if args.source_repo != "papyrus-factory-recurring":
        raise BuildReceiptError("source_repo must be papyrus-factory-recurring")
    validate_relative_path(args.source_path, "source_path")
    validate_commit(args.source_commit, "source_commit")
    validate_commit(args.canon_commit, "canon_commit")
    validate_commit(args.website_metadata_commit, "website_metadata_commit")
    if not args.source_file.is_file():
        raise BuildReceiptError("source manuscript file is missing")
    expected_pdf = f"papers/{args.slug}-{args.target_version}.pdf"
    if args.pdf_path.as_posix() != expected_pdf:
        raise BuildReceiptError(f"pdf_path must be {expected_pdf}")
    if not args.pdf_path.is_file():
        raise BuildReceiptError("rendered PDF is missing")
    if args.total_pages < 1:
        raise BuildReceiptError("total_pages must be positive")
    try:
        datetime.fromisoformat(args.built_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise BuildReceiptError("built_at must be an ISO-8601 timestamp") from exc
    parsed_run = urlparse(args.workflow_run_url)
    if parsed_run.scheme != "https" or parsed_run.hostname != "github.com":
        raise BuildReceiptError("workflow_run_url must be a GitHub HTTPS URL")

    addendum = None
    addendum_values = (
        args.addendum_repo,
        args.addendum_path,
        args.addendum_commit,
        args.addendum_file,
    )
    if any(value not in (None, "") for value in addendum_values):
        if not all(value not in (None, "") for value in addendum_values):
            raise BuildReceiptError("addendum fields must be supplied together")
        if args.addendum_repo != "papyrus-factory-recurring":
            raise BuildReceiptError("addendum_repo must be papyrus-factory-recurring")
        validate_relative_path(args.addendum_path, "addendum_path")
        validate_commit(args.addendum_commit, "addendum_commit")
        if not args.addendum_file.is_file():
            raise BuildReceiptError("addendum file is missing")
        addendum = {
            "repo": args.addendum_repo,
            "path": args.addendum_path,
            "commit": args.addendum_commit,
            "sha256": digest(args.addendum_file),
        }

    return {
        "schema_version": "1.0",
        "receipt_type": "papyrus-build",
        "release_authority": False,
        "publication_action": "none",
        "paper_id": args.paper_id,
        "slug": args.slug,
        "transition": args.transition,
        "target_version": args.target_version,
        "source": {
            "repo": args.source_repo,
            "path": args.source_path,
            "commit": args.source_commit,
            "sha256": digest(args.source_file),
        },
        "addendum": addendum,
        "canon_commit": args.canon_commit,
        "website_metadata_commit": args.website_metadata_commit,
        "artifact": {
            "path": args.pdf_path.as_posix(),
            "sha256": digest(args.pdf_path),
            "bytes": args.pdf_path.stat().st_size,
            "total_pages": args.total_pages,
        },
        "tracker": args.tracker or None,
        "workflow_run_url": args.workflow_run_url,
        "built_at": args.built_at,
        "non_claims": [
            "This build receipt is not publication authority.",
            "This build receipt does not mint a DOI.",
            "Substantive-page, research, citation, editorial, integrity, ten-field, and operator gates remain separate.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-id", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--transition", required=True)
    parser.add_argument("--target-version", required=True)
    parser.add_argument("--source-repo", required=True)
    parser.add_argument("--source-path", required=True)
    parser.add_argument("--source-file", required=True, type=Path)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--addendum-repo")
    parser.add_argument("--addendum-path")
    parser.add_argument("--addendum-file", type=Path)
    parser.add_argument("--addendum-commit")
    parser.add_argument("--canon-commit", required=True)
    parser.add_argument("--website-metadata-commit", required=True)
    parser.add_argument("--pdf-path", required=True, type=Path)
    parser.add_argument("--total-pages", required=True, type=int)
    parser.add_argument("--tracker")
    parser.add_argument("--workflow-run-url", required=True)
    parser.add_argument("--built-at", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    try:
        receipt = build(args)
    except (OSError, BuildReceiptError) as exc:
        print(f"build receipt failed: {exc}", file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
