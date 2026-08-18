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
