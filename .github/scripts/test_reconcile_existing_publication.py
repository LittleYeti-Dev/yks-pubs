#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("reconcile-existing-publication.py")
SPEC = importlib.util.spec_from_file_location("reconcile_existing_publication", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ExistingPublicationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.source = root / "source.pdf"
        self.zenodo = root / "zenodo.pdf"
        payload = b"%PDF-1.4\nexact published bytes\n%%EOF\n"
        self.source.write_bytes(payload)
        self.zenodo.write_bytes(payload)
        self.digest = hashlib.sha256(payload).hexdigest()
        self.record_json = root / "record.json"
        self.record_json.write_text(
            json.dumps(
                {
                    "id": 123456,
                    "doi": "10.5281/zenodo.123456",
                    "metadata": {
                        "title": "Example Paper",
                        "version": "v0.1-preprint",
                        "publication_date": "2026-08-02",
                        "creators": [{"name": "Kuiper, Justin H."}],
                        "license": {"id": "cc-by-nd-4.0"},
                    },
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def args(self) -> argparse.Namespace:
        return argparse.Namespace(
            paper_id="PAP-TEST-001",
            slug="example-paper",
            title="Example Paper",
            author="Justin H. Kuiper",
            version="v0.1-preprint",
            published_date="2026-08-02",
            doi="10.5281/zenodo.123456",
            zenodo_record_url="https://zenodo.org/records/123456",
            canonical_url="https://nonsequitur.tech/white-papers/example-paper/",
            rights="CC BY-ND 4.0",
            expected_sha256=self.digest,
            source_pdf=self.source,
            zenodo_pdf=self.zenodo,
            zenodo_record_json=self.record_json,
            archive_pdf_path="papers/example-paper-v0.1-preprint.pdf",
            operator_decision_ref="https://github.com/LittleYeti-Dev/repo/issues/1#issuecomment-1",
            source_repo_commit="a" * 40,
            archive_base_commit="b" * 40,
            workflow_run_url="https://github.com/LittleYeti-Dev/yks-pubs/actions/runs/1",
            verified_at="2026-08-23T17:00:00Z",
        )

    def test_exact_existing_publication_receipts_without_mint(self) -> None:
        receipt = MODULE.validate(self.args())
        self.assertEqual(receipt["publication_action"], "reconcile-existing-doi")
        self.assertEqual(receipt["pdf_sha256"], self.digest)
        self.assertEqual(receipt["maturity_state"], "withheld")

    def test_zenodo_byte_mismatch_fails_closed(self) -> None:
        self.zenodo.write_bytes(b"different")
        with self.assertRaisesRegex(MODULE.ReconciliationError, "Zenodo PDF hash mismatch"):
            MODULE.validate(self.args())

    def test_metadata_mismatch_fails_closed(self) -> None:
        args = self.args()
        args.title = "Wrong Title"
        with self.assertRaisesRegex(MODULE.ReconciliationError, "title"):
            MODULE.validate(args)


if __name__ == "__main__":
    unittest.main()
