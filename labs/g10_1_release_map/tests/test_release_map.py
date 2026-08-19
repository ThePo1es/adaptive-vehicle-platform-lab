from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


LAB_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = LAB_DIR.parents[1]
sys.path.insert(0, str(LAB_DIR))

from run_harness import apply_operation, run  # noqa: E402
import validator  # noqa: E402
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
            "STRUCTURE_PASS G10.1-MAP profile=harness nodes=11 edges=11 citations=1 statuses=Mapped:0,Partial:11,Missing:0,Out of scope:0 review=Pending",
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
        self.assertEqual("G10.1 harness: PASS (1 valid, 23 negative cases)", run()[-1])

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
            "reviewer_key_fingerprint": "SHA256:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            "subject_commit": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "subject_path": "fixtures/g10/synthetic-reviewed-submission.json",
            "review_manifest_path": "fixtures/g10/review-manifest-v1.json",
            "review_manifest_sha256": hashlib.sha256(review_path.read_bytes()).hexdigest(),
            "review_signature_path": "",
            "reviewed_citation_ids": ["SYN-BOUNDARY-001"],
        }
        self.assertEqual([], validate_harness(document))
        self.assertTrue(pass_line(document).startswith("HARNESS_REVIEW_BINDING_PASS G10.1-MAP profile=harness"))
        self.assertNotIn("REVIEWED_PASS", pass_line(document))
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

    def test_fake_pdf_is_rejected_without_official_digest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            fake_pdf = directory / "AUTOSAR_AP_TPS_ManifestSpecification.pdf"
            payload = b"%PDF-1.4\nFAKE AUTOSAR DOCUMENT\n%%EOF\n"
            fake_pdf.write_bytes(payload)
            source = {
                "source_file_path": "sources/autosar-r25-11/AUTOSAR_AP_TPS_ManifestSpecification.pdf",
                "source_file_sha256": hashlib.sha256(payload).hexdigest(),
            }
            locked = {
                "filename": fake_pdf.name,
                "official_sha512": None,
            }
            findings: list[validator.Finding] = []
            with (
                mock.patch.object(validator, "_repo_path", return_value=fake_pdf),
                mock.patch.object(validator, "SOURCE_DIRECTORY", directory),
            ):
                validator._validate_source_file(source, locked, 1, findings)
            self.assertIn("E_SOURCE_TRUST", {finding.code for finding in findings})

    def test_submission_review_needs_detached_trusted_signature(self) -> None:
        document = copy.deepcopy(self.case_set["guided_submission"])
        review_path = REPO_ROOT / "fixtures/g10/review-manifest-v1.json"
        review = {
            "status": "Reviewed",
            "reviewer_id": "synthetic-harness-reviewer",
            "reviewer_key_fingerprint": "SHA256:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            "subject_commit": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "subject_path": "fixtures/g10/synthetic-reviewed-submission.json",
            "review_manifest_path": "fixtures/g10/review-manifest-v1.json",
            "review_manifest_sha256": hashlib.sha256(review_path.read_bytes()).hexdigest(),
            "review_signature_path": "fixtures/g10/missing-review.sig",
            "reviewed_citation_ids": ["SYN-BOUNDARY-001"],
        }
        findings: list[validator.Finding] = []
        validator._validate_review_manifest(
            review,
            document,
            {"SYN-BOUNDARY-001"},
            {node["id"] for node in document["nodes"]},
            "submission",
            {},
            {},
            None,
            findings,
        )
        self.assertIn("E_REVIEW_TRUST", {finding.code for finding in findings})

    def test_release_policy_signature_and_hashes_are_valid(self) -> None:
        findings: list[validator.Finding] = []
        source_lock, reviewers, hashes = validator._load_attested_trust(None, findings)
        self.assertEqual([], findings)
        self.assertEqual(5, len(source_lock))
        self.assertEqual({}, reviewers)
        self.assertEqual(
            {"source_lock_sha256", "reviewer_registry_sha256", "review_policy_sha256"},
            set(hashes),
        )

    def test_unsigned_source_lock_change_invalidates_policy(self) -> None:
        findings: list[validator.Finding] = []
        original = validator._trust_bytes

        def changed_trust_file(commit: str | None, relative_path: str) -> bytes:
            payload = original(commit, relative_path)
            if relative_path == validator.SOURCE_LOCK_RELATIVE:
                return payload + b"\n"
            return payload

        with mock.patch.object(validator, "_trust_bytes", side_effect=changed_trust_file):
            source_lock, reviewers, hashes = validator._load_attested_trust(None, findings)
        self.assertEqual({}, source_lock)
        self.assertEqual({}, reviewers)
        self.assertEqual({}, hashes)
        self.assertIn("E_TRUST_POLICY", {finding.code for finding in findings})

    def test_both_authority_signatures_are_required(self) -> None:
        findings: list[validator.Finding] = []
        original = validator._trust_bytes

        def missing_second_signature(commit: str | None, relative_path: str) -> bytes:
            if relative_path == validator.REVIEW_POLICY_SIGNATURE_RELATIVES[1]:
                return b"invalid signature\n"
            return original(commit, relative_path)

        with mock.patch.object(validator, "_trust_bytes", side_effect=missing_second_signature):
            source_lock, reviewers, hashes = validator._load_attested_trust(None, findings)
        self.assertEqual(({}, {}, {}), (source_lock, reviewers, hashes))
        self.assertIn("E_TRUST_POLICY", {finding.code for finding in findings})

    def test_unrelated_subject_commit_is_rejected(self) -> None:
        document = copy.deepcopy(self.case_set["guided_submission"])
        review_path = REPO_ROOT / "fixtures/g10/review-manifest-v1.json"
        head = "a" * 40
        review = {
            "status": "Reviewed",
            "reviewer_id": "synthetic-harness-reviewer",
            "reviewer_key_fingerprint": "SHA256:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            "subject_commit": head,
            "subject_path": "README.md",
            "review_manifest_path": "fixtures/g10/review-manifest-v1.json",
            "review_manifest_sha256": hashlib.sha256(review_path.read_bytes()).hexdigest(),
            "review_signature_path": "fixtures/g10/missing-review.sig",
            "reviewed_citation_ids": ["SYN-BOUNDARY-001"],
        }
        findings: list[validator.Finding] = []
        with mock.patch.object(validator, "_git_blob", return_value=b"# unrelated file\n"):
            validator._validate_review_manifest(
                review,
                document,
                {"SYN-BOUNDARY-001"},
                {node["id"] for node in document["nodes"]},
                "submission",
                {},
                {},
                REPO_ROOT / "README.md",
                findings,
            )
        messages = {finding.message for finding in findings if finding.code == "E_REVIEW_TRUST"}
        self.assertIn("subject commit does not contain the reviewed submission at subject_path", messages)


if __name__ == "__main__":
    unittest.main()
