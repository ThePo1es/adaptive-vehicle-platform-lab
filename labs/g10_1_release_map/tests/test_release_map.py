from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path


LAB_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = LAB_DIR.parents[1]
sys.path.insert(0, str(LAB_DIR))

from run_harness import apply_operation, run  # noqa: E402
from validator import pass_line, validate_harness, validate_submission  # noqa: E402


class ReleaseMapValidatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        case_path = REPO_ROOT / "fixtures/g10/release-map-cases-v1.json"
        cls.case_set = json.loads(case_path.read_text(encoding="utf-8"))

    def test_guided_submission_passes(self) -> None:
        self.assertEqual([], validate_harness(self.case_set["guided_submission"]))

    def test_pass_line_is_stable(self) -> None:
        self.assertEqual(
            "STRUCTURE_PASS G10.1-MAP nodes=11 edges=11 citations=1 statuses=Mapped:0,Partial:11,Missing:0,Out of scope:0 review=Pending",
            pass_line(self.case_set["guided_submission"]),
        )

    def test_each_negative_case_has_only_its_declared_error(self) -> None:
        for case in self.case_set["negative_cases"]:
            with self.subTest(case=case["id"]):
                document = copy.deepcopy(self.case_set["guided_submission"])
                apply_operation(document, case)
                observed = sorted({finding.code for finding in validate_harness(document)})
                self.assertEqual(sorted(case["expected_errors"]), observed)

    def test_harness_summary(self) -> None:
        self.assertEqual("G10.1 harness: PASS (1 valid, 17 negative cases)", run()[-1])

    def test_submission_profile_rejects_synthetic_fixture(self) -> None:
        observed = {finding.code for finding in validate_submission(self.case_set["guided_submission"])}
        self.assertIn("E_PROFILE_DOWNGRADE", observed)
        self.assertIn("E_CITATION_ID", observed)

    def test_reviewed_pass_is_bound_to_a_real_manifest(self) -> None:
        document = copy.deepcopy(self.case_set["guided_submission"])
        review_path = REPO_ROOT / "fixtures/g10/review-manifest-v1.json"
        document["review"] = {
            "status": "Reviewed",
            "reviewer_id": "synthetic-harness-reviewer",
            "review_manifest_path": "fixtures/g10/review-manifest-v1.json",
            "review_manifest_sha256": hashlib.sha256(review_path.read_bytes()).hexdigest(),
            "reviewed_citation_ids": ["SYN-BOUNDARY-001"],
        }
        self.assertEqual([], validate_harness(document))
        self.assertTrue(pass_line(document).startswith("REVIEWED_PASS G10.1-MAP"))
        document["review"]["review_manifest_sha256"] = "d" * 64
        self.assertIn("E_REVIEW", {finding.code for finding in validate_harness(document)})
        with self.assertRaises(ValueError):
            pass_line(document)

    def test_submission_source_must_match_lock_and_local_pdf(self) -> None:
        document = copy.deepcopy(self.case_set["guided_submission"])
        document["profile"] = "submission"
        readme = REPO_ROOT / "README.md"
        document["source_ledger"][0] = {
            "citation_id": "SYN-BOUNDARY-001",
            "source_kind": "official",
            "release": "R25-11",
            "document_id": "AUTOSAR_AP_TPS_ManifestSpecification",
            "document_revision": "R25-11",
            "section_title": "Manifest deployment artifact overview",
            "section_locator": "1.2",
            "source_url": "https://www.autosar.org/not-a-document",
            "source_file_path": "README.md",
            "access_status": "Direct",
            "accessed_on": "2026-08-19",
            "source_file_sha256": hashlib.sha256(readme.read_bytes()).hexdigest(),
        }
        observed = {finding.code for finding in validate_submission(document)}
        self.assertIn("E_SOURCE_URL", observed)
        self.assertIn("E_SOURCE_PATH", observed)
        self.assertIn("E_CITATION_ROLE", observed)

    def test_required_role_edge_cannot_be_removed(self) -> None:
        document = copy.deepcopy(self.case_set["guided_submission"])
        document["edges"].pop()
        observed = {finding.code for finding in validate_harness(document)}
        self.assertEqual({"E_GRAPH_CONNECTIVITY"}, observed)


if __name__ == "__main__":
    unittest.main()
