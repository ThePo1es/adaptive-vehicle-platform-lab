from __future__ import annotations

import pytest

from labs.g02_embedded_cpp.elf_contract import (
    ElfContractError,
    ElfReport,
    verify_reports,
)


def report(
    variant: str,
    *,
    symbols: frozenset[str],
    relocation_symbols: frozenset[str],
) -> ElfReport:
    return ElfReport(variant, 16, len(relocation_symbols), symbols, relocation_symbols)


def valid_reports() -> tuple[ElfReport, ...]:
    return (
        report(
            "virtual",
            symbols=frozenset({"g02_virtual_entry", "_ZTV10FixedClock"}),
            relocation_symbols=frozenset({"_ZTV10FixedClock"}),
        ),
        report(
            "static",
            symbols=frozenset({"g02_static_entry"}),
            relocation_symbols=frozenset({"_Z10read_clockI10FixedClockEiRT_"}),
        ),
        report(
            "manual",
            symbols=frozenset({"g02_manual_entry"}),
            relocation_symbols=frozenset({"_Z10read_fixedPv"}),
        ),
    )


def test_elf_contract_requires_variant_specific_relocation_targets() -> None:
    reports = list(valid_reports())
    reports[0] = report(
        "virtual",
        symbols=frozenset({"g02_virtual_entry", "_ZTV10FixedClock"}),
        relocation_symbols=frozenset(),
    )
    with pytest.raises(ElfContractError, match="required relocation"):
        _ = verify_reports(tuple(reports))


def test_elf_contract_accepts_all_required_relocation_targets() -> None:
    assert verify_reports(valid_reports()) == (48, 3)
