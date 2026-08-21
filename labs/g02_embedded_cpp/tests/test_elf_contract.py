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
            symbols=frozenset({"g02_virtual_entry", "_ZTVTestClock"}),
            relocation_symbols=frozenset({"virtual-target"}),
        ),
        report(
            "static",
            symbols=frozenset({"g02_static_entry"}),
            relocation_symbols=frozenset({"static-target"}),
        ),
        report(
            "manual",
            symbols=frozenset({"g02_manual_entry"}),
            relocation_symbols=frozenset({"manual-target"}),
        ),
    )


def test_elf_contract_requires_variant_specific_relocation_targets() -> None:
    contract = {
        "virtual": "virtual-target",
        "static": "static-target",
        "manual": "manual-target",
    }
    reports = list(valid_reports())
    reports[0] = report(
        "virtual",
        symbols=frozenset({"g02_virtual_entry", "_ZTVTestClock"}),
        relocation_symbols=frozenset(),
    )
    with pytest.raises(ElfContractError, match="required relocation"):
        _ = verify_reports(tuple(reports), contract)


def test_elf_contract_accepts_all_required_relocation_targets() -> None:
    contract = {
        "virtual": "virtual-target",
        "static": "static-target",
        "manual": "manual-target",
    }
    assert verify_reports(valid_reports(), contract) == (48, 3)
