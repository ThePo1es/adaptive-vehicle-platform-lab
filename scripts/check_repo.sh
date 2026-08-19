#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repo_root=$(cd -- "$script_dir/.." && pwd)
cd "$repo_root"

required_files=(
    README.md
    ROADMAP.md
    ASSESSMENTS.md
    PROGRESS.md
    SECURITY.md
    compiler-analysis/README.md
    docs/competency-map.md
    docs/baseline.md
    docs/gate-playbook.md
    docs/embedded-foundations.md
    docs/architecture-engineering.md
    docs/safety-security-engineering.md
    docs/requirements.md
    docs/traceability.md
    docs/autosar-mapping.md
    docs/templates/mastery-review.md
    assessments/README.md
    gates/README.md
    gates/g00/sprint-0.1.md
    gates/g00/sprint-0.2.md
    gates/g01/sprint-1.1.md
    gates/g01/sprint-1.2.md
    gates/g01/sprint-1.3.md
    gates/g01/sprint-1.4.md
    gates/g01/sprint-1.5.md
    gates/g02/sprint-2.1.md
    gates/g02/sprint-2.2.md
    gates/g02/sprint-2.3.md
    gates/g02/sprint-2.4.md
    gates/g03/sprint-3.1.md
    gates/g03/sprint-3.2.md
    gates/g03/sprint-3.3.md
    gates/g03/sprint-3.4.md
    gates/g03/sprint-3.5.md
    gates/g08/sprint-8.1.md
    gates/g08/sprint-8.2.md
    gates/g08/sprint-8.3.md
    gates/g08/sprint-8.4.md
    gates/g08/sprint-8.5.md
    gates/g08/sprint-8.6.md
    gates/g08/sprint-8.7.md
    gates/g09/sprint-9.1.md
    gates/g09/sprint-9.2.md
    gates/g09/sprint-9.3.md
    gates/g09/sprint-9.4.md
    gates/g09/sprint-9.5.md
    gates/g09/sprint-9.6.md
    gates/g09/sprint-9.7.md
    gates/g09/sprint-9.8.md
    gates/g10/sprint-10.1.md
    gates/g10/sprint-10.2.md
    gates/g10/sprint-10.3.md
    gates/g10/sprint-10.4.md
    gates/g10/sprint-10.5.md
    gates/g10/sprint-10.6.md
    gates/g10/sprint-10.7.md
    gates/g10/sprint-10.8.md
    projects/00-mcu-rtos-ecu/README.md
    projects/05-can-ethernet-vertical-slice/README.md
    projects/06-heterogeneous-vehicle-platform/README.md
)

for file in "${required_files[@]}"; do
    if [[ ! -f $file ]]; then
        echo "error: required file is missing: $file" >&2
        exit 1
    fi
done

ready_lab_files=(
    gates/g00/*.md
    gates/g01/*.md
    gates/g02/*.md
    gates/g03/*.md
    gates/g08/*.md
    gates/g09/*.md
    gates/g10/*.md
)

if (( ${#ready_lab_files[@]} != 39 )); then
    echo "error: expected 39 ready lab packs, found ${#ready_lab_files[@]}" >&2
    exit 1
fi

required_lab_sections=(
    "안내 실습"
    "독립 실습"
    "전이 과제"
    "판정 기준"
    "힌트"
    "치명적 실패"
)

for file in "${ready_lab_files[@]}"; do
    if ! grep -Eq '^## .*시간|^## 시간' "$file"; then
        echo "error: lab pack has no time section: $file" >&2
        exit 1
    fi
    for section in "${required_lab_sections[@]}"; do
        if ! grep -Fq "## $section" "$file"; then
            echo "error: lab pack is missing '$section': $file" >&2
            exit 1
        fi
    done
done

bash -n scripts/new-study-log.sh scripts/check_repo.sh
python3 -c 'import ast, pathlib; [ast.parse(pathlib.Path(path).read_text(encoding="utf-8")) for path in ("scripts/check_internal_links.py", "scripts/check_traceability.py")]'
python3 scripts/check_internal_links.py
python3 scripts/check_traceability.py

if find . -path './.git' -prune -o -type f \
    \( -name '*.pem' -o -name '*.key' -o -name '*.p12' -o -name '*.pcap' -o -name '*.pcapng' \) \
    -print -quit | grep -q .; then
    echo "error: potentially sensitive key or capture file found" >&2
    exit 1
fi

if find . -path './.git' -prune -o -type f \
    \( -name '*.c' -o -name '*.cpp' -o -name '*.h' -o -name '*.hpp' -o -name 'CMakeLists.txt' \) \
    -print -quit | grep -q .; then
    if [[ ! -f LICENSE && ! -f LICENSE.md ]]; then
        echo "error: code exists but LICENSE or LICENSE.md is missing" >&2
        exit 1
    fi
    for file in THIRD_PARTY_NOTICES.md .github/workflows/code-build.yml; do
        if [[ ! -f $file ]]; then
            echo "error: code exists but $file is missing" >&2
            exit 1
        fi
    done
fi

echo "Documentation integrity checks: OK"
