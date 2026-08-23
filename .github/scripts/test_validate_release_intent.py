#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate-release-intent.py")
SPEC = importlib.util.spec_from_file_location("validate_release_intent", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ReleaseIntentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "papers").mkdir()
        self.pdf = self.root / "papers/example-paper-v1-preprint.pdf"
        self.pdf.write_bytes(b"%PDF-1.4\ncontrolled test artifact\n%%EOF\n")
        self.digest = hashlib.sha256(self.pdf.read_bytes()).hexdigest()
        self.intent = {
            "schema_version": "1.0",
            "publication_action": "mint-new-doi",
            "paper_id": "PAP-TEST-001",
            "slug": "example-paper",
            "version_label": "v1-preprint",
            "pdf_path": "papers/example-paper-v1-preprint.pdf",
            "pdf_sha256": self.digest,
            "operator_decision_ref": "https://github.com/LittleYeti-Dev/repo/issues/1#issuecomment-1",
            "operator_approved_at": "2026-08-23T13:00:00-04:00",
            "author": "Justin H. Kuiper",
            "rights": "CC BY-ND 4.0",
            "papyrus_release_gate_ref": "d1://yks-corpus-ledger/papyrus_release_gate/PAP-TEST-001",
            "validation_receipt_ref": "https://github.com/LittleYeti-Dev/repo/blob/abc1234/receipt.json",
            "ten_field_preflight_ref": "https://github.com/LittleYeti-Dev/repo/blob/abc1234/preflight.json",
            "source_commit": "abc1234",
            "source_custody": "complete-original",
            "substantive_page_count": 25,
            "verified_peer_reviewed_source_count": 15,
            "verified_post_2024_primary_source_count": 3,
            "outbound_cross_paper_reference_count": 1,
            "cross_paper_evidence_gate": "pass",
        }
        self.intent_path = self.root / "intent.json"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_intent(self) -> None:
        self.intent_path.write_text(json.dumps(self.intent), encoding="utf-8")

    def test_valid_intent_binds_exact_pdf(self) -> None:
        self.write_intent()
        result = MODULE.validate(self.intent_path, self.root)
        self.assertEqual(result["pdf_sha256"], self.digest)

    def test_hash_mismatch_fails_closed(self) -> None:
        self.intent["pdf_sha256"] = "0" * 64
        self.write_intent()
        with self.assertRaisesRegex(MODULE.IntentError, "hash mismatch"):
            MODULE.validate(self.intent_path, self.root)

    def test_non_mint_action_fails_closed(self) -> None:
        self.intent["publication_action"] = "reconcile-existing-doi"
        self.write_intent()
        with self.assertRaisesRegex(MODULE.IntentError, "mint-new-doi"):
            MODULE.validate(self.intent_path, self.root)

    def test_path_must_match_slug_and_version(self) -> None:
        self.intent["pdf_path"] = "papers/some-other-paper.pdf"
        self.write_intent()
        with self.assertRaisesRegex(MODULE.IntentError, "pdf_path must be"):
            MODULE.validate(self.intent_path, self.root)

    def test_research_floor_fails_closed(self) -> None:
        self.intent["verified_peer_reviewed_source_count"] = 14
        self.write_intent()
        with self.assertRaisesRegex(MODULE.IntentError, "at least 15"):
            MODULE.validate(self.intent_path, self.root)

    def test_cross_paper_chain_fails_closed(self) -> None:
        self.intent["cross_paper_evidence_gate"] = "hold"
        self.write_intent()
        with self.assertRaisesRegex(MODULE.IntentError, "must pass"):
            MODULE.validate(self.intent_path, self.root)


if __name__ == "__main__":
    unittest.main()
