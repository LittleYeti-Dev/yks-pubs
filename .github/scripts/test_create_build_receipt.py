#!/usr/bin/env python3

from __future__ import annotations

import argparse
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("create-build-receipt.py")
SPEC = importlib.util.spec_from_file_location("create_build_receipt", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class BuildReceiptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.previous = Path.cwd()
        os.chdir(self.temp.name)
        Path("papers").mkdir()
        self.source = Path("manuscript.md")
        self.source.write_text("# Controlled source\n", encoding="utf-8")
        self.pdf = Path("papers/example-paper-v1-preprint.pdf")
        self.pdf.write_bytes(b"%PDF-1.4\ncontrolled artifact\n%%EOF\n")

    def tearDown(self) -> None:
        os.chdir(self.previous)
        self.temp.cleanup()

    def args(self) -> argparse.Namespace:
        return argparse.Namespace(
            paper_id="PAP-TEST-001",
            slug="example-paper",
            transition="preprint-promote",
            target_version="v1-preprint",
            source_repo="papyrus-factory-recurring",
            source_path="release-packages/PAP-TEST-001/manuscript.md",
            source_file=self.source,
            source_commit="a" * 40,
            addendum_repo=None,
            addendum_path=None,
            addendum_file=None,
            addendum_commit=None,
            canon_commit="b" * 40,
            website_metadata_commit="c" * 40,
            pdf_path=self.pdf,
            total_pages=40,
            tracker="LittleYeti-Dev/yks2.0-ops-hub#984",
            workflow_run_url="https://github.com/LittleYeti-Dev/yks-pubs/actions/runs/1",
            built_at="2026-08-23T18:00:00Z",
        )

    def test_receipt_binds_source_and_pdf_without_release_authority(self) -> None:
        receipt = MODULE.build(self.args())
        self.assertFalse(receipt["release_authority"])
        self.assertEqual(receipt["publication_action"], "none")
        self.assertEqual(receipt["artifact"]["total_pages"], 40)
        self.assertEqual(receipt["source"]["repo"], "papyrus-factory-recurring")

    def test_non_papyrus_source_fails_closed(self) -> None:
        args = self.args()
        args.source_repo = "YKS-Spine-Binder"
        with self.assertRaisesRegex(MODULE.BuildReceiptError, "papyrus"):
            MODULE.build(args)

    def test_existing_target_identity_must_match_slug_and_version(self) -> None:
        args = self.args()
        args.pdf_path = Path("papers/other.pdf")
        with self.assertRaisesRegex(MODULE.BuildReceiptError, "pdf_path must be"):
            MODULE.build(args)


if __name__ == "__main__":
    unittest.main()
