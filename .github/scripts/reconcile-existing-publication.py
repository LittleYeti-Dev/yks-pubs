#!/usr/bin/env python3
"""Validate and receipt an already-published artifact without minting a DOI."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
DOI_RE = re.compile(r"^10\.5281/zenodo\.([0-9]+)$", re.IGNORECASE)
PAPER_ID_RE = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)+$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_RE = re.compile(r"^v[0-9]+(?:[.-][0-9]+)*(?:-[a-z0-9]+)*$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


class ReconciliationError(ValueError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_https(url: str, field: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ReconciliationError(f"{field} must be an absolute HTTPS URL")


def metadata(record: dict) -> dict:
    value = record.get("metadata")
    return value if isinstance(value, dict) else {}


def creator_names(record: dict) -> list[str]:
    creators = metadata(record).get("creators", [])
    names = []
    for creator in creators:
        if isinstance(creator, dict) and creator.get("name"):
            names.append(str(creator["name"]))
    return names


def license_id(record: dict) -> str:
    value = metadata(record).get("license")
    if isinstance(value, dict):
        return str(value.get("id") or value.get("title") or "")
    return str(value or "")


def normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def name_tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.lower()))


def validate(args: argparse.Namespace) -> dict:
    if not PAPER_ID_RE.fullmatch(args.paper_id):
        raise ReconciliationError("paper_id is not a canonical PAPYRUS identifier")
    if not SLUG_RE.fullmatch(args.slug):
        raise ReconciliationError("slug is not canonical kebab-case")
    if not VERSION_RE.fullmatch(args.version):
        raise ReconciliationError("version is not a supported version label")
    expected_archive_path = f"papers/{args.slug}-{args.version}.pdf"
    if args.archive_pdf_path != expected_archive_path:
        raise ReconciliationError(f"archive_pdf_path must be {expected_archive_path}")
    expected_hash = args.expected_sha256.lower()
    if not SHA256_RE.fullmatch(expected_hash):
        raise ReconciliationError("expected_sha256 must be 64 lowercase hexadecimal characters")

    doi_match = DOI_RE.fullmatch(args.doi)
    if not doi_match:
        raise ReconciliationError("doi must be an exact Zenodo DOI")
    require_https(args.zenodo_record_url, "zenodo_record_url")
    require_https(args.canonical_url, "canonical_url")
    require_https(args.workflow_run_url, "workflow_run_url")
    if urlparse(args.zenodo_record_url).hostname != "zenodo.org":
        raise ReconciliationError("zenodo_record_url must use zenodo.org")
    if urlparse(args.canonical_url).hostname not in {"nonsequitur.tech", "www.nonsequitur.tech"}:
        raise ReconciliationError("canonical_url must use nonsequitur.tech")
    if urlparse(args.workflow_run_url).hostname != "github.com":
        raise ReconciliationError("workflow_run_url must use github.com")
    expected_record_id = doi_match.group(1)
    if args.zenodo_record_url.rstrip("/").split("/")[-1] != expected_record_id:
        raise ReconciliationError("Zenodo record URL does not match DOI record ID")

    source_hash = sha256(args.source_pdf)
    zenodo_hash = sha256(args.zenodo_pdf)
    if source_hash != expected_hash:
        raise ReconciliationError(
            f"source PDF hash mismatch: expected={expected_hash}, actual={source_hash}"
        )
    if zenodo_hash != expected_hash:
        raise ReconciliationError(
            f"Zenodo PDF hash mismatch: expected={expected_hash}, actual={zenodo_hash}"
        )

    try:
        record = json.loads(args.zenodo_record_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReconciliationError(f"cannot read Zenodo record JSON: {exc}") from exc

    actual_id = str(record.get("id") or "")
    actual_doi = str(record.get("doi") or metadata(record).get("doi") or "")
    actual_title = str(metadata(record).get("title") or record.get("title") or "")
    actual_version = str(metadata(record).get("version") or record.get("version") or "")
    actual_date = str(
        metadata(record).get("publication_date") or record.get("publication_date") or ""
    )
    names = creator_names(record)

    if actual_id != expected_record_id:
        raise ReconciliationError("Zenodo API record ID does not match DOI")
    if actual_doi.lower() != args.doi.lower():
        raise ReconciliationError("Zenodo API DOI does not match requested DOI")
    if actual_title != args.title:
        raise ReconciliationError("Zenodo title does not exactly match requested title")
    if actual_version != args.version:
        raise ReconciliationError("Zenodo version does not exactly match requested version")
    if actual_date != args.published_date:
        raise ReconciliationError("Zenodo publication date does not match requested date")
    wanted_author = name_tokens(args.author)
    if not any(
        wanted_author == name_tokens(name)
        for name in names
    ):
        raise ReconciliationError("Zenodo creators do not include the requested author")
    actual_rights = license_id(record)
    if normalize_name(actual_rights) != normalize_name(args.rights):
        raise ReconciliationError(
            f"Zenodo rights mismatch: requested={args.rights}, actual={actual_rights}"
        )
    if not args.operator_decision_ref.startswith(("https://github.com/", "LittleYeti-Dev/")):
        raise ReconciliationError("operator_decision_ref must identify a durable GitHub decision")
    if not COMMIT_RE.fullmatch(args.source_repo_commit):
        raise ReconciliationError("source_repo_commit must be a full Git commit SHA")
    if not COMMIT_RE.fullmatch(args.archive_base_commit):
        raise ReconciliationError("archive_base_commit must be a full Git commit SHA")

    return {
        "schema_version": "1.0",
        "receipt_type": "existing-publication-reconciliation",
        "publication_action": "reconcile-existing-doi",
        "paper_id": args.paper_id,
        "slug": args.slug,
        "title": args.title,
        "author": args.author,
        "version": args.version,
        "published_date": args.published_date,
        "doi": args.doi,
        "zenodo_record_url": args.zenodo_record_url,
        "canonical_url": args.canonical_url,
        "archive_pdf_path": args.archive_pdf_path,
        "pdf_sha256": expected_hash,
        "rights": args.rights,
        "operator_decision_ref": args.operator_decision_ref,
        "source_repo_commit": args.source_repo_commit,
        "archive_base_commit": args.archive_base_commit,
        "workflow_run_url": args.workflow_run_url,
        "verified_at": args.verified_at,
        "verified_chain": {
            "doi_record_identity": "pass",
            "title": "pass",
            "author": "pass",
            "version": "pass",
            "publication_date": "pass",
            "rights": "pass",
            "source_pdf_hash": "pass",
            "zenodo_pdf_hash": "pass",
        },
        "authority_roles": {
            "zenodo_doi": "persistent published identity",
            "yks_pubs": "released artifact archive",
            "pubs_website": "public presentation",
            "papyrus_d1": "paper identity and workflow state",
            "canon": "maturity rules",
        },
        "maturity_state": "withheld",
        "non_claims": [
            "This receipt does not mint a DOI.",
            "This receipt does not prove editable-source custody.",
            "This receipt does not approve series placement or Canon maturity.",
            "Citation, editorial, supersession, and cross-paper evidence gates remain separate.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-id", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--author", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--published-date", required=True)
    parser.add_argument("--doi", required=True)
    parser.add_argument("--zenodo-record-url", required=True)
    parser.add_argument("--canonical-url", required=True)
    parser.add_argument("--rights", required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--source-pdf", required=True, type=Path)
    parser.add_argument("--zenodo-pdf", required=True, type=Path)
    parser.add_argument("--zenodo-record-json", required=True, type=Path)
    parser.add_argument("--archive-pdf-path", required=True)
    parser.add_argument("--operator-decision-ref", required=True)
    parser.add_argument("--source-repo-commit", required=True)
    parser.add_argument("--archive-base-commit", required=True)
    parser.add_argument("--workflow-run-url", required=True)
    parser.add_argument("--verified-at", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    try:
        receipt = validate(args)
    except (OSError, ReconciliationError) as exc:
        print(f"publication reconciliation failed: {exc}", file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
