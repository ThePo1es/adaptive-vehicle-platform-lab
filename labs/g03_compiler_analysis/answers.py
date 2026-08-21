from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import override

from .contracts import IssueCandidate, IssueDecision, decide_issue_report
from .submission import source_file


@dataclass(frozen=True, slots=True)
class AnswerError(Exception):
    reason: str

    @override
    def __str__(self) -> str:
        return self.reason


def parse_answers(path: Path) -> Mapping[str, str]:
    pairs: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        key, separator, value = line.partition("=")
        if not separator or not key or key in pairs:
            raise AnswerError(f"invalid answer line: {line}")
        pairs[key] = value
    return pairs


def verify_issue_answers(root: Path) -> IssueDecision:
    answers = parse_answers(source_file(root, "compiler_issue_decision.answers"))
    candidate_keys = (
        "source_contract_defined",
        "reproduced",
        "reduced",
        "expected_behavior_cited",
        "duplicate_search_done",
    )
    required = {*candidate_keys, "decision", "upstream_submitted"}
    if set(answers) != required or answers["upstream_submitted"] != "false":
        raise AnswerError("G3.5 answer schema or no-fake-upstream control failed")
    candidate = IssueCandidate(
        answers[candidate_keys[0]] == "true",
        answers[candidate_keys[1]] == "true",
        answers[candidate_keys[2]] == "true",
        answers[candidate_keys[3]] == "true",
        answers[candidate_keys[4]] == "true",
    )
    decision = decide_issue_report(candidate)
    if decision.value != answers["decision"] or decision is not IssueDecision.READY_FOR_PEER_REVIEW:
        raise AnswerError("G3.5 candidate is not ready for local peer review")
    return decision
