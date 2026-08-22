# pyright: reportMissingTypeStubs=false, reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, override

from elftools.common.exceptions import ELFError
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection


@dataclass(frozen=True, slots=True)
class ElfExpectation:
    machine: str
    sections: tuple[str, ...]
    symbols: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ElfCheckError(Exception):
    reason: str

    @override
    def __str__(self) -> str:
        return self.reason


@dataclass(frozen=True, slots=True)
class ElfView:
    machine: str
    sections: tuple[tuple[str, int], ...]
    symbols: frozenset[str]


def _bounded_view(stream: BinaryIO) -> ElfView:
    elf = ELFFile(stream)
    sections: list[tuple[str, int]] = []
    symbols: set[str] = set()
    for section in elf.iter_sections():
        sections.append((str(section.name), int(section["sh_size"])))
        if isinstance(section, SymbolTableSection):
            symbols.update(str(symbol.name) for symbol in section.iter_symbols() if symbol.name)
    machine = f"{elf['e_machine']}"
    return ElfView(machine, tuple(sections), frozenset(symbols))


def read_elf(path: Path) -> ElfView:
    try:
        with path.open("rb") as stream:
            return _bounded_view(stream)
    except (ELFError, OSError, TypeError, ValueError) as error:
        raise ElfCheckError(f"{path.name}: invalid ELF: {error}") from error


def verify_elf(path: Path, expectation: ElfExpectation) -> None:
    elf = read_elf(path)
    if elf.machine != expectation.machine:
        raise ElfCheckError(f"{path.name}: machine={elf.machine} expected={expectation.machine}")
    section_names = {name for name, _ in elf.sections}
    missing_sections = set(expectation.sections) - section_names
    if missing_sections:
        raise ElfCheckError(f"{path.name}: missing sections={sorted(missing_sections)}")
    missing_symbols = set(expectation.symbols) - elf.symbols
    if missing_symbols:
        raise ElfCheckError(f"{path.name}: missing symbols={sorted(missing_symbols)}")


def text_size(path: Path) -> int:
    sizes = tuple(
        size
        for name, size in read_elf(path).sections
        if name == ".text" or name.startswith(".text.")
    )
    if not sizes:
        raise ElfCheckError(f"{path.name}: .text sections are missing")
    return sum(sizes)
