from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, override

InputProfile = Literal["A", "B"]


@dataclass(frozen=True, slots=True)
class DefinedInputError(Exception):
    reason: str

    @override
    def __str__(self) -> str:
        return self.reason


@dataclass(frozen=True, slots=True)
class DefinedCase:
    case_id: str
    value: int
    limit: int
    expected: int


@dataclass(frozen=True, slots=True)
class InputSet:
    profile: InputProfile
    defined: tuple[DefinedCase, ...]
    excluded_ub: tuple[str, ...]


def load_input_set(fixtures: Path, profile: InputProfile) -> InputSet:
    path = fixtures / f"input-{profile.lower()}.tsv"
    defined: list[DefinedCase] = []
    excluded: list[str] = []
    with path.open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            case_id = row.get("case", "")
            if row.get("defined") == "false":
                excluded.append(case_id)
                continue
            if row.get("defined") != "true":
                raise DefinedInputError(f"{path.name}: {case_id}: defined must be true or false")
            try:
                defined.append(
                    DefinedCase(
                        case_id,
                        int(row["value"]),
                        int(row["limit"]),
                        int(row["expected"]),
                    )
                )
            except (KeyError, ValueError) as error:
                raise DefinedInputError(
                    f"{path.name}: {case_id}: invalid defined input"
                ) from error
    if not defined or not excluded:
        raise DefinedInputError(f"{path.name}: defined and excluded UB cases are required")
    return InputSet(profile, tuple(defined), tuple(excluded))


def render_driver(input_set: InputSet) -> str:
    rows = ",\n".join(
        f'    {{{case.value}U, {case.limit}U, {case.expected}U, "{case.case_id}"}}'
        for case in input_set.defined
    )
    return f"""typedef unsigned int u32;
extern u32 bounded_step(u32 value, u32 limit);
struct test_case {{ u32 value; u32 limit; u32 expected; const char *name; }};
#ifdef _WIN32
__declspec(dllimport) void __stdcall ExitProcess(unsigned int);
#define G03_ENTRY void mainCRTStartup(void)
#define G03_EXIT(code) ExitProcess(code)
#else
#define G03_ENTRY int main(void)
#define G03_EXIT(code) return (code)
#endif
G03_ENTRY {{
  const struct test_case cases[] = {{
{rows}
  }};
  for (unsigned i = 0; i < sizeof(cases) / sizeof(cases[0]); ++i) {{
    const u32 actual = bounded_step(cases[i].value, cases[i].limit);
    if (actual != cases[i].expected) {{
      G03_EXIT(i + 1U);
    }}
  }}
  G03_EXIT(0U);
}}
"""
