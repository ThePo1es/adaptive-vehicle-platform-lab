from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final, override

MACHINES: Final = {40: "EM_ARM", 183: "EM_AARCH64"}
SYMBOL_TABLE_TYPES: Final = {2, 11}


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
class Section:
    name_offset: int
    section_type: int
    offset: int
    size: int
    link: int
    entry_size: int


@dataclass(frozen=True, slots=True)
class ElfView:
    machine: str
    sections: tuple[tuple[str, Section], ...]
    symbols: frozenset[str]


def _unsigned(data: bytes, offset: int, width: int) -> int:
    return int.from_bytes(data[offset : offset + width], "little")


def _cstring(data: bytes, offset: int) -> str:
    end = data.find(b"\0", offset)
    if end < 0:
        raise ElfCheckError("unterminated ELF string table entry")
    return data[offset:end].decode("utf-8")


def _section(data: bytes, offset: int, elf_class: int) -> Section:
    if elf_class == 1:
        return Section(
            _unsigned(data, offset, 4),
            _unsigned(data, offset + 4, 4),
            _unsigned(data, offset + 16, 4),
            _unsigned(data, offset + 20, 4),
            _unsigned(data, offset + 24, 4),
            _unsigned(data, offset + 36, 4),
        )
    return Section(
        _unsigned(data, offset, 4),
        _unsigned(data, offset + 4, 4),
        _unsigned(data, offset + 24, 8),
        _unsigned(data, offset + 32, 8),
        _unsigned(data, offset + 40, 4),
        _unsigned(data, offset + 56, 8),
    )


def read_elf(path: Path) -> ElfView:
    data = path.read_bytes()
    if data[:4] != b"\x7fELF" or data[5] != 1:
        raise ElfCheckError(f"{path.name}: little-endian ELF is required")
    elf_class = data[4]
    if elf_class not in {1, 2}:
        raise ElfCheckError(f"{path.name}: unsupported ELF class={elf_class}")
    header = (32, 46, 48, 50) if elf_class == 1 else (40, 58, 60, 62)
    section_offset = _unsigned(data, header[0], 4 if elf_class == 1 else 8)
    section_entry_size = _unsigned(data, header[1], 2)
    section_count = _unsigned(data, header[2], 2)
    name_index = _unsigned(data, header[3], 2)
    raw_sections = tuple(
        _section(data, section_offset + index * section_entry_size, elf_class)
        for index in range(section_count)
    )
    names_section = raw_sections[name_index]
    names = data[names_section.offset : names_section.offset + names_section.size]
    sections = tuple((_cstring(names, section.name_offset), section) for section in raw_sections)
    symbols: set[str] = set()
    for _, section in sections:
        if section.section_type not in SYMBOL_TABLE_TYPES or section.entry_size == 0:
            continue
        strings_section = raw_sections[section.link]
        strings = data[strings_section.offset : strings_section.offset + strings_section.size]
        for entry in range(section.offset, section.offset + section.size, section.entry_size):
            symbol_name_offset = _unsigned(data, entry, 4)
            if symbol_name_offset:
                symbols.add(_cstring(strings, symbol_name_offset))
    machine = MACHINES.get(_unsigned(data, 18, 2), "UNKNOWN")
    return ElfView(machine, sections, frozenset(symbols))


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
    section = next((value for name, value in read_elf(path).sections if name == ".text"), None)
    if section is None:
        raise ElfCheckError(f"{path.name}: .text section is missing")
    return section.size
