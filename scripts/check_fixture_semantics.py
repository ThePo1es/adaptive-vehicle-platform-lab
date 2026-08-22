#!/usr/bin/env python3
"""Recalculate deterministic fixture oracles without third-party packages."""

from __future__ import annotations

import csv
import json
import math
import re
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
FAILURES: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        FAILURES.append(message)


def scalar(value: str) -> Any:
    value = value.strip()
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def task_rows() -> list[dict[str, Any]]:
    path = ROOT / "fixtures/g05/task-set-v1.yml"
    rows: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    in_tasks = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line == "tasks:":
            in_tasks = True
            continue
        if not in_tasks:
            continue
        start = re.fullmatch(r"  - id:\s*(\S+)", line)
        if start:
            current = {"id": start.group(1)}
            rows.append(current)
            continue
        field = re.fullmatch(r"    ([a-z_]+):\s*(.+)", line)
        if field and current is not None:
            current[field.group(1)] = scalar(field.group(2))
    return rows


def check_g05_rta() -> None:
    tasks = task_rows()
    required = {
        "id",
        "release_model",
        "priority",
        "period_or_min_interarrival",
        "deadline",
        "execution_bound",
        "release_jitter",
        "blocking_resource",
        "blocking_bound",
        "stack_budget_bytes",
        "expected_response_bound",
    }
    check(len(tasks) == 4, "G5 task fixture must contain four tasks")
    for task in tasks:
        missing = sorted(required - task.keys())
        check(not missing, f"G5 {task.get('id')}: missing fields {missing}")
        if missing:
            continue
        check(task["release_model"] in {"periodic", "sporadic"}, f"G5 {task['id']}: invalid release model")
        check(task["stack_budget_bytes"] > 0, f"G5 {task['id']}: stack budget must be positive")
        if task["blocking_bound"] == 0:
            check(task["blocking_resource"] == "none", f"G5 {task['id']}: zero blocking must name resource as none")
        else:
            check(task["blocking_resource"] != "none", f"G5 {task['id']}: positive blocking needs a resource")

    ordered = sorted(tasks, key=lambda item: item.get("priority", -1), reverse=True)
    check(len({item.get("priority") for item in ordered}) == len(ordered), "G5 priorities must be unique")
    for index, task in enumerate(ordered):
        if required - task.keys():
            continue
        response = task["execution_bound"] + task["blocking_bound"]
        for _ in range(100):
            interference = 0
            for higher in ordered[:index]:
                arrivals = math.ceil(
                    (response + higher["release_jitter"])
                    / higher["period_or_min_interarrival"]
                )
                interference += arrivals * higher["execution_bound"]
            next_response = task["execution_bound"] + task["blocking_bound"] + interference
            if next_response == response:
                break
            response = next_response
        else:
            check(False, f"G5 {task['id']}: RTA did not converge")
        check(response == task["expected_response_bound"], f"G5 {task['id']}: expected RTA {task['expected_response_bound']}, calculated {response}")
        check(response + task["release_jitter"] <= task["deadline"], f"G5 {task['id']}: deadline fixture is internally failing")


def check_dlc() -> None:
    path = ROOT / "fixtures/g06/can-fd-dlc-v1.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    actual = [(int(row["dlc_code"]), int(row["payload_length_bytes"])) for row in rows]
    expected = list(enumerate([0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 16, 20, 24, 32, 48, 64]))
    check(actual == expected, "CAN FD DLC fixture does not match the 16-code mapping")


def load_json(relative: str) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def check_can_rta() -> None:
    data = load_json("fixtures/g06/can-rta-three-message-v1.json")
    messages = sorted(data["messages"], key=lambda item: item["can_id"])
    bit_time = data["bus"]["bit_time_us"]
    epsilon = data["analysis"]["epsilon_us"]
    check(len(messages) == 3, "G6 CAN RTA fixture must contain three messages")
    for index, message in enumerate(messages):
        payload = message["payload_bytes"]
        stuffable = 34 + 8 * payload
        wire_bits = 44 + 8 * payload + (stuffable - 1) // 4 + data["bus"]["intermission_bits"]
        check(wire_bits == message["wire_bits_bound"], f"G6 {message['id']}: wire-bit bound mismatch")
        transmission = wire_bits * bit_time
        check(transmission == message["transmission_time_us"], f"G6 {message['id']}: transmission time mismatch")
        lower = messages[index + 1 :]
        blocking = max((item["transmission_time_us"] for item in lower), default=0)
        check(blocking == message["blocking_us"], f"G6 {message['id']}: non-preemptive blocking mismatch")

        waiting = blocking
        for _ in range(100):
            interference = sum(
                math.ceil(
                    (waiting + higher["release_jitter_us"] + epsilon)
                    / higher["period_or_min_interarrival_us"]
                )
                * higher["transmission_time_us"]
                for higher in messages[:index]
            )
            next_waiting = blocking + interference
            if next_waiting == waiting:
                break
            waiting = next_waiting
        else:
            check(False, f"G6 {message['id']}: CAN RTA did not converge")
        response = message["release_jitter_us"] + waiting + transmission
        check(waiting == message["expected_queueing_us"], f"G6 {message['id']}: queueing oracle mismatch")
        check(response == message["expected_response_us"], f"G6 {message['id']}: response oracle mismatch")
        check(response <= message["deadline_us"], f"G6 {message['id']}: response exceeds fixture deadline")

    load = sum(
        Fraction(message["transmission_time_us"], message["period_or_min_interarrival_us"])
        for message in messages
    )
    check(load * 1_000_000 == data["analysis"]["expected_load_ppm"], "G6 CAN load oracle mismatch")


def check_journal() -> None:
    data = load_json("fixtures/g07/dtc-journal-reset-v1.json")
    steps = data["journal"]["write_steps"]
    expected_boundaries = {"before_erase", *steps}
    actual_boundaries = {case["reset_after"] for case in data["cases"] if case["id"] <= "J06"}
    check(actual_boundaries == expected_boundaries, "G7 journal fixture does not cover every write boundary")
    check(data["journal"]["slot_count"] == 2, "G7 journal oracle requires two slots")
    for case in data["cases"]:
        candidate_committed = case["reset_after"] == "write_commit" and not case["corrupt_candidate"]
        selected = case["candidate"] if candidate_committed else case["previous"]
        selected_state = selected["state"] if selected else data["default_state"]
        selected_sequence = selected["sequence"] if selected else None
        check(selected_state == case["expected_state"], f"G7 {case['id']}: selected state mismatch")
        check(selected_sequence == case["expected_sequence"], f"G7 {case['id']}: selected sequence mismatch")


def check_mode_security() -> None:
    data = load_json("fixtures/g07/mode-security-permutations-v1.json")
    model = data["mode_model"]
    priority = {event: index for index, event in enumerate(model["event_priority"])}
    for case in data["mode_cases"]:
        if case["initial_state"] in model["terminal_states"]:
            state, reason = case["initial_state"], "already_shutdown"
        else:
            selected = min(case["events"], key=priority.__getitem__)
            rule = model["rules"][selected]
            state, reason = rule["next_state"], rule["reason"]
        check(state == case["expected_state"], f"G7 {case['id']}: mode state mismatch")
        check(reason == case["expected_reason"], f"G7 {case['id']}: mode reason mismatch")

    policy = data["freshness_policy"]
    allowed = set(policy["allowed_key_ids"])
    for case in data["freshness_cases"]:
        accepted = (
            case["tag_valid"]
            and case["key_id"] in allowed
            and case["incoming_counter"] > case["highest_accepted_counter"]
        )
        highest = case["incoming_counter"] if accepted else case["highest_accepted_counter"]
        quality = "valid" if accepted else policy["reject_effect"]["quality"]
        check(accepted == case["expected_accept"], f"G7 {case['id']}: freshness decision mismatch")
        check(accepted == case["expected_application_update"], f"G7 {case['id']}: application update mismatch")
        check(highest == case["expected_highest_counter"], f"G7 {case['id']}: freshness counter mismatch")
        check(quality == case["expected_quality"], f"G7 {case['id']}: freshness quality mismatch")


def check_text_fixtures() -> None:
    required_markers = {
        "fixtures/g06/isotp-rx-v1.yml": [
            "schema: isotp-rx-corpus/v1",
            "synthetic: true",
            "id: wrong-sequence",
            "result: capacity_exceeded",
            "allocation_attempts: 0",
        ],
        "fixtures/g06/uds-read-v1.yml": [
            "schema: uds-read-corpus/v1",
            'expected_response: "62 12 34 00 2A"',
            'expected_response: "7F 22 31"',
            "provider_calls: 0",
        ],
        "fixtures/g07/classic-config-v1.yml": [
            "schema: classic-concept-config/v1",
            "name: CanRxTask",
            "name: UpdateVehicleSpeed",
            "generated/runnable_table.hpp",
            "generated/com_routes.hpp",
            "generated/diagnostic_routes.hpp",
        ],
    }
    for relative, markers in required_markers.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        for marker in markers:
            check(marker in text, f"{relative}: missing semantic marker {marker!r}")


def check_g11_assurance_changes() -> None:
    data = load_json("fixtures/g11/assurance-change-v1.json")
    cases = {case["id"]: case for case in data["change_cases"]}
    check(
        set(cases) == {"SCENARIO-SPEED-001", "COMMON-CLOCK-001", "TRUST-ROOT-001"},
        "G11 assurance fixture must contain the three frozen change cases",
    )
    if "SCENARIO-SPEED-001" in cases:
        speed_impacts = set(cases["SCENARIO-SPEED-001"]["expected_impacts"])
        check(
            speed_impacts
            == {"item-definition", "HARA", "safety-goal", "safety-requirement", "fault-test", "assurance-claim"},
            "G11 speed change impact set drifted",
        )
    if "COMMON-CLOCK-001" in cases:
        clock_impacts = set(cases["COMMON-CLOCK-001"]["expected_impacts"])
        check(
            clock_impacts
            == {"FMEA", "FTA", "TARA", "freshness-contract", "timing-budget", "degraded-transition", "assurance-claim"},
            "G11 common-clock impact set drifted",
        )
        check(
            set(cases["COMMON-CLOCK-001"]["required_reviewers"]) == {"safety", "security"},
            "G11 common-clock change needs both reviewer roles",
        )
    if "TRUST-ROOT-001" in cases:
        check(
            cases["TRUST-ROOT-001"].get("expected_tier_ceiling") == "T2",
            "G11 removed trust root must cap the claim at T2",
        )


def expected_version_decision(case: dict[str, Any]) -> str:
    service = case["service"]
    gateway = case["gateway"]
    mcu = case["mcu"]
    fallback = case["fallback_translation"]
    if service == gateway == mcu:
        return "Compatible"
    if service > gateway and not fallback:
        return "Block activation"
    if service == gateway and gateway > mcu and fallback:
        return "Degraded read-only"
    return "Unspecified"


def check_g12_integration_contract() -> None:
    data = load_json("fixtures/g12/integration-contract-v1.json")
    budget = data["data_path_budget"]
    allocations = budget["allocations"]
    total = sum(item["budget_us"] for item in allocations)
    check(len(allocations) == 6, "G12 data-path budget must have six owned allocations")
    check(
        len({item["owner"] for item in allocations}) == len(allocations),
        "G12 data-path budget owners must be unique",
    )
    check(total == budget["expected_total_us"], "G12 allocation sum differs from expected total")
    check(total == budget["deadline_us"] == 20_000, "G12 data-path deadline must remain 20,000 us")

    version_cases = data["version_cases"]
    check(len({case["id"] for case in version_cases}) == 3, "G12 needs three unique version cases")
    for case in version_cases:
        check(
            expected_version_decision(case) == case["expected_decision"],
            f"G12 {case['id']}: version oracle mismatch",
        )

    lifecycle = {case["id"]: case for case in data["lifecycle_cases"]}
    expected_order = [
        "withdraw VehicleState",
        "mark source unavailable",
        "restart service",
        "observe new MCU session",
        "recheck version",
        "resume degraded read-only",
    ]
    check(
        lifecycle.get("LIFECYCLE-DUAL-FAULT-001", {}).get("expected_order") == expected_order,
        "G12 dual-fault lifecycle order drifted",
    )
    check(
        lifecycle.get("LIFECYCLE-DUAL-FAULT-001", {}).get("expected_terminal_state") == "Degraded read-only",
        "G12 dual-fault terminal state drifted",
    )

    faults = data["fault_catalog"]
    expected_fault_ids = {f"F{number:02d}" for number in range(1, 13)}
    check({fault["id"] for fault in faults} == expected_fault_ids, "G12 fault catalog must contain F01 through F12")
    for fault in faults:
        check(bool(fault.get("first_observer")), f"G12 {fault['id']}: first observer is empty")
        check(bool(fault.get("expected_state")), f"G12 {fault['id']}: expected state is empty")


def main() -> int:
    check_g05_rta()
    check_dlc()
    check_can_rta()
    check_journal()
    check_mode_security()
    check_text_fixtures()
    check_g11_assurance_changes()
    check_g12_integration_contract()
    if FAILURES:
        print("Fixture semantic checks failed:", file=sys.stderr)
        for failure in FAILURES:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print("Fixture semantic checks: OK (10 files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
