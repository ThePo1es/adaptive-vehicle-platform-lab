from __future__ import annotations

import subprocess
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, cast

from elftools.elf.elffile import ELFFile

from .harness_toolchain import compiler_prefix


class ElfContractError(Exception):
    pass


class _SymbolView(Protocol):
    @property
    def name(self) -> str: ...


class _SymbolTableView(Protocol):
    def iter_symbols(self) -> Iterator[_SymbolView]: ...

    def get_symbol(self, index: int) -> _SymbolView: ...


class _SectionView(Protocol):
    def __getitem__(self, key: str) -> int: ...


class _RelocationView(Protocol):
    def num_relocations(self) -> int: ...

    def iter_relocations(self) -> Iterator[_SectionView]: ...

    def __getitem__(self, key: str) -> int: ...


class _ElfView(Protocol):
    def get_section_by_name(self, name: str) -> object | None: ...

    def get_section(self, index: int) -> object | None: ...

    def iter_sections(self) -> Iterator[object]: ...


@dataclass(frozen=True, slots=True)
class ElfReport:
    variant: str
    text_bytes: int
    relocation_count: int
    symbols: frozenset[str]
    relocation_symbols: frozenset[str]


@dataclass(frozen=True, slots=True)
class FreestandingBuild:
    compiler: Path
    source: Path
    target: str
    output: Path


@dataclass(frozen=True, slots=True)
class AbiVerification:
    compiler: Path
    include_root: Path
    test_root: Path
    corpus_root: Path
    build_root: Path


def compile_freestanding_object(request: FreestandingBuild) -> None:
    result = subprocess.run(
        [
            *compiler_prefix(request.compiler),
            "-std=c++20",
            "-O2",
            "-fno-exceptions",
            "-fno-rtti",
            "-ffreestanding",
            "-nostdlib",
            "-target",
            request.target,
            "-c",
            str(request.source),
            "-o",
            str(request.output),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise ElfContractError(result.stdout + result.stderr)


def inspect_elf(path: Path, variant: str) -> ElfReport:
    with path.open("rb") as stream:
        elf = cast(_ElfView, cast(object, ELFFile(stream)))
        text_object = elf.get_section_by_name(".text")
        symbols_object = elf.get_section_by_name(".symtab")
        if text_object is None or symbols_object is None:
            raise ElfContractError(f"{variant} object has no .text or .symtab")
        text = cast(_SectionView, text_object)
        symbols = cast(_SymbolTableView, symbols_object)
        names = frozenset(symbol.name for symbol in symbols.iter_symbols() if symbol.name)
        relocation_count = 0
        relocation_symbols: set[str] = set()
        for section_object in elf.iter_sections():
            if not hasattr(section_object, "iter_relocations"):
                continue
            section = cast(_RelocationView, section_object)
            relocation_count += section.num_relocations()
            symbol_table_object = elf.get_section(int(section["sh_link"]))
            if symbol_table_object is None:
                raise ElfContractError(f"{variant} relocation section has no symbol table")
            symbol_table = cast(_SymbolTableView, symbol_table_object)
            for relocation in section.iter_relocations():
                symbol_index = int(relocation["r_info_sym"])
                if symbol_index == 0:
                    continue
                symbol_name = symbol_table.get_symbol(symbol_index).name
                if symbol_name:
                    relocation_symbols.add(symbol_name)
        return ElfReport(
            variant,
            int(text["sh_size"]),
            relocation_count,
            names,
            frozenset(relocation_symbols),
        )


def verify_reports(reports: tuple[ElfReport, ...]) -> tuple[int, int]:
    by_variant = {report.variant: report for report in reports}
    if set(by_variant) != {"virtual", "static", "manual"}:
        raise ElfContractError("all three ABI variants are required")
    if not any(name.startswith("_ZTV") for name in by_variant["virtual"].symbols):
        raise ElfContractError("virtual variant has no vtable symbol")
    for variant, symbol in (
        ("virtual", "g02_virtual_entry"),
        ("static", "g02_static_entry"),
        ("manual", "g02_manual_entry"),
    ):
        if symbol not in by_variant[variant].symbols:
            raise ElfContractError(f"{variant} entry symbol is missing")
    required_relocations = {
        "virtual": "_ZTV10FixedClock",
        "static": "_Z10read_clockI10FixedClockEiRT_",
        "manual": "_Z10read_fixedPv",
    }
    for variant, symbol in required_relocations.items():
        if symbol not in by_variant[variant].relocation_symbols:
            raise ElfContractError(
                f"{variant} required relocation target is missing: {symbol}"
            )
    return (
        sum(report.text_bytes for report in reports),
        sum(report.relocation_count for report in reports),
    )


def verify_abi_contract(request: AbiVerification) -> None:
    c_header = subprocess.run(
        [
            str(request.compiler),
            "cc",
            "-std=c17",
            "-Wall",
            "-Wextra",
            "-Wpedantic",
            "-Werror",
            f"-I{request.include_root}",
            "-c",
            str(request.test_root / "test_c_abi_header.c"),
            "-o",
            str(request.build_root / "c-abi-header.o"),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if c_header.returncode != 0:
        raise ElfContractError(c_header.stdout + c_header.stderr)
    print("PASS lab=G2.4 c17-header=compatible")
    for target in ("thumb-freestanding-eabi", "aarch64-freestanding-none"):
        reports: list[ElfReport] = []
        for variant in ("virtual", "static", "manual"):
            output = request.build_root / f"{target}-{variant}.o"
            compile_freestanding_object(
                FreestandingBuild(
                    request.compiler,
                    request.corpus_root / f"{variant}.cpp",
                    target,
                    output,
                )
            )
            reports.append(inspect_elf(output, variant))
        text_bytes, relocations = verify_reports(tuple(reports))
        print(
            f"PASS lab=G2.4 abi-target={target} variants=3 text-bytes={text_bytes} "
            + f"relocations={relocations}"
        )
