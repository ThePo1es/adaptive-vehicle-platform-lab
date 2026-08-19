from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


LAB_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = LAB_DIR.parents[1]
sys.path.insert(0, str(LAB_DIR))

from run_harness import replace_at_pointer, run  # noqa: E402
from validator import pass_line, validate  # noqa: E402


class ReleaseMapValidatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        case_path = REPO_ROOT / "fixtures/g10/release-map-cases-v1.json"
        cls.case_set = json.loads(case_path.read_text(encoding="utf-8"))

    def test_guided_submission_passes(self) -> None:
        self.assertEqual([], validate(self.case_set["guided_submission"], "harness"))

    def test_pass_line_is_stable(self) -> None:
        self.assertEqual(
            "PASS G10.1-MAP rows=7 citations=1 statuses=Mapped:0,Partial:7,Missing:0,Out of scope:0",
            pass_line(self.case_set["guided_submission"]),
        )

    def test_each_negative_case_has_only_its_declared_error(self) -> None:
        for case in self.case_set["negative_cases"]:
            with self.subTest(case=case["id"]):
                document = copy.deepcopy(self.case_set["guided_submission"])
                replace_at_pointer(document, case["mutation"]["path"], case["mutation"]["value"])
                observed = sorted({finding.code for finding in validate(document, "harness")})
                self.assertEqual(sorted(case["expected_errors"]), observed)

    def test_harness_summary(self) -> None:
        self.assertEqual("G10.1 harness: PASS (1 valid, 5 negative cases)", run()[-1])


if __name__ == "__main__":
    unittest.main()
