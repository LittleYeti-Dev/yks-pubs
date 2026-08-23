#!/usr/bin/env python3
"""Validate the explicit operator release intent required before DOI minting."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
import re
import sys
from pathlib import Path


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_RE = re.compile(r"^v[0-9]+(?:[-.][0-9]+)*(?:-[a-z0-9]+)*$")
PAPER_ID_RE = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)+$")


class IntentError(ValueError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_text(record: dict, key: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise IntentError(f"{key} must be a non-empty string")
    value = value.strip()
    if "\n" in value or "\r" in value:
        raise IntentError(f"{key} cannot contain a newline")
    return value


def require_count(record: dict, key: str) -> int:
    value = record.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise IntentError(f"{key} must be a non-negative integer")
    return value


def validate(intent_path: Path, repo_root: Path, expected_pdf: str | None = None) -> dict:
    try:
        record = json.loads(intent_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IntentError(f"cannot read release intent: {exc}") from exc

    if not isinstance(record, dict):
        raise IntentError("release intent must be a JSON object")
    if record.get("schema_version") != "1.0":
        raise IntentError("schema_version must be 1.0")
    if record.get("publication_action") != "mint-new-doi":
        raise IntentError("publication_action must be mint-new-doi")

    paper_id = require_text(record, "paper_id")
    slug = require_text(record, "slug")
    version = require_text(record, "version_label")
    pdf_path_text = require_text(record, "pdf_path")
    expected_hash = require_text(record, "pdf_sha256").lower()
    decision = require_text(record, "operator_decision_ref")
    approved_at = require_text(record, "operator_approved_at")
    author = require_text(record, "author")
    rights = require_text(record, "rights")
    release_gate_ref = require_text(record, "papyrus_release_gate_ref")
    validation_ref = require_text(record, "validation_receipt_ref")
    ten_field_ref = require_text(record, "ten_field_preflight_ref")
    source_commit = require_text(record, "source_commit")
    source_repository = require_text(record, "source_repository")
    source_custody = require_text(record, "source_custody")
    cross_paper_gate = require_text(record, "cross_paper_evidence_gate")
    page_count = require_count(record, "substantive_page_count")
    peer_reviewed = require_count(record, "verified_peer_reviewed_source_count")
    post_2024 = require_count(record, "verified_post_2024_primary_source_count")
    outbound_cross_paper = require_count(record, "outbound_cross_paper_reference_count")

    if not PAPER_ID_RE.fullmatch(paper_id):
        raise IntentError("paper_id is not a canonical PAPYRUS identifier")
    if not SLUG_RE.fullmatch(slug):
        raise IntentError("slug is not canonical kebab-case")
    if not VERSION_RE.fullmatch(version):
        raise IntentError("version_label is not a supported version label")
    if not SHA256_RE.fullmatch(expected_hash):
        raise IntentError("pdf_sha256 must be 64 lowercase hexadecimal characters")
    expected_path = f"papers/{slug}-{version}.pdf"
    if pdf_path_text != expected_path:
        raise IntentError(f"pdf_path must be {expected_path}")
    if expected_pdf and pdf_path_text != expected_pdf:
        raise IntentError(f"intent PDF {pdf_path_text} does not match requested PDF {expected_pdf}")
    if not decision.startswith(("https://github.com/", "LittleYeti-Dev/")):
        raise IntentError("operator_decision_ref must identify a durable GitHub decision")
    for field, value in (
        ("papyrus_release_gate_ref", release_gate_ref),
        ("validation_receipt_ref", validation_ref),
        ("ten_field_preflight_ref", ten_field_ref),
    ):
        if not value.startswith(("https://github.com/", "LittleYeti-Dev/", "d1://")):
            raise IntentError(f"{field} must identify durable evidence")
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise IntentError("source_commit must be a full Git commit SHA")
    if source_repository != "LittleYeti-Dev/papyrus-factory-recurring":
        raise IntentError("source_repository must be LittleYeti-Dev/papyrus-factory-recurring")
    if source_custody not in {"complete-original", "complete-recovered-verified"}:
        raise IntentError("source_custody must be complete-original or complete-recovered-verified")
    if cross_paper_gate != "pass":
        raise IntentError("cross_paper_evidence_gate must pass")
    if page_count < 25:
        raise IntentError("substantive_page_count must be at least 25")
    if peer_reviewed < 15:
        raise IntentError("verified_peer_reviewed_source_count must be at least 15")
    if post_2024 < 3:
        raise IntentError("verified_post_2024_primary_source_count must be at least 3")
    if outbound_cross_paper < 1:
        raise IntentError("outbound_cross_paper_reference_count must be at least 1")
    try:
        datetime.fromisoformat(approved_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise IntentError("operator_approved_at must be an ISO-8601 timestamp") from exc

    pdf_path = (repo_root / pdf_path_text).resolve()
    papers_root = (repo_root / "papers").resolve()
    if papers_root not in pdf_path.parents:
        raise IntentError("pdf_path escapes the papers directory")
    if not pdf_path.is_file():
        raise IntentError(f"PDF does not exist: {pdf_path_text}")
    actual_hash = sha256(pdf_path)
    if actual_hash != expected_hash:
        raise IntentError(
            f"PDF hash mismatch: intent={expected_hash}, actual={actual_hash}"
        )

    return {
        "paper_id": paper_id,
        "slug": slug,
        "version_label": version,
        "pdf_path": pdf_path_text,
        "pdf_sha256": actual_hash,
        "operator_decision_ref": decision,
        "operator_approved_at": approved_at,
        "author": author,
        "rights": rights,
        "papyrus_release_gate_ref": release_gate_ref,
        "validation_receipt_ref": validation_ref,
        "ten_field_preflight_ref": ten_field_ref,
        "source_commit": source_commit,
        "source_repository": source_repository,
        "source_custody": source_custody,
        "substantive_page_count": page_count,
        "verified_peer_reviewed_source_count": peer_reviewed,
        "verified_post_2024_primary_source_count": post_2024,
        "outbound_cross_paper_reference_count": outbound_cross_paper,
        "cross_paper_evidence_gate": cross_paper_gate,
    }


def write_github_output(path: Path, values: dict) -> None:
    with path.open("a", encoding="utf-8") as handle:
        for key, value in values.items():
            handle.write(f"{key}={value}\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intent", required=True, type=Path)
    parser.add_argument("--repo-root", default=Path.cwd(), type=Path)
    parser.add_argument("--expected-pdf")
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()

    try:
        values = validate(
            args.intent.resolve(), args.repo_root.resolve(), args.expected_pdf
        )
    except IntentError as exc:
        print(f"release-intent validation failed: {exc}", file=sys.stderr)
        return 1

    if args.github_output:
        write_github_output(args.github_output, values)
    print(json.dumps(values, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
