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
    docs/gate-entry-diagnostics.md
    docs/curriculum-audit.md
    docs/embedded-foundations.md
    docs/adr/README.md
    docs/architecture-engineering.md
    docs/safety-security-engineering.md
    docs/lifecycle-ownership.md
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
    gates/g08/sprint-8.8.md
    gates/g08/sprint-8.9.md
    gates/g09/sprint-9.1.md
    gates/g09/sprint-9.2.md
    gates/g09/sprint-9.3.md
    gates/g09/sprint-9.4.md
    gates/g09/sprint-9.5.md
    gates/g09/sprint-9.6.md
    gates/g09/sprint-9.7.md
    gates/g09/sprint-9.8.md
    gates/g09/sprint-9.9.md
    gates/g09/sprint-9.10.md
    gates/g10/sprint-10.1.md
    gates/g10/sprint-10.2.md
    gates/g10/sprint-10.3.md
    gates/g10/sprint-10.4.md
    gates/g10/sprint-10.5.md
    gates/g10/sprint-10.6.md
    gates/g10/sprint-10.7.md
    gates/g10/sprint-10.8.md
    gates/g10/sprint-10.9.md
    gates/g10/sprint-10.10.md
    gates/g11/sprint-11.1.md
    gates/g11/sprint-11.2.md
    gates/g11/sprint-11.3.md
    gates/g11/sprint-11.4.md
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

specified_lab_files=(
    gates/g00/*.md
    gates/g01/*.md
    gates/g02/*.md
    gates/g03/*.md
    gates/g08/*.md
    gates/g09/*.md
    gates/g10/*.md
    gates/g11/*.md
)

if (( ${#specified_lab_files[@]} != 49 )); then
    echo "error: expected 49 specified lab packs, found ${#specified_lab_files[@]}" >&2
    exit 1
fi

for file in "${specified_lab_files[@]}"; do
    if ! grep -Eq '^## .*시간|^## 시간' "$file"; then
        echo "error: lab pack has no time section: $file" >&2
        exit 1
    fi
    if ! grep -Eq '^## 안내 실습' "$file"; then
        echo "error: lab pack has no guided implementation: $file" >&2
        exit 1
    fi
    if ! grep -Eq '^## 독립 실습' "$file"; then
        echo "error: lab pack has no independent implementation: $file" >&2
        exit 1
    fi
    if ! grep -Eq '^## 전이 과제' "$file"; then
        echo "error: lab pack has no transfer task: $file" >&2
        exit 1
    fi
    if ! grep -Eq '^## 판정 기준' "$file"; then
        echo "error: lab pack has no acceptance criteria: $file" >&2
        exit 1
    fi
    if ! tail -n 18 "$file" | grep -Eq '재시험|보강|보충|다시|축소|줄여|통과하지|통과를 미루|완료 처리를 미루|인정하지|사용하지|릴리스하지|중단|멈추'; then
        echo "error: lab pack has no retrial condition: $file" >&2
        exit 1
    fi
done

bash -n scripts/new-study-log.sh scripts/check_repo.sh
python3 -c 'import ast, pathlib; [ast.parse(pathlib.Path(path).read_text(encoding="utf-8")) for path in ("scripts/check_internal_links.py", "scripts/check_traceability.py")]'
python3 scripts/check_internal_links.py
python3 scripts/check_traceability.py

if find . -path './.git' -prune -o -type f \
    \( -name '*.pem' -o -name '*.key' -o -name '*.p12' \) \
    -print -quit | grep -q .; then
    echo "error: potentially sensitive key file found" >&2
    exit 1
fi

while IFS= read -r capture; do
    case "$capture" in
        ./evidence/public-fixtures/*.pcap|./evidence/public-fixtures/*.pcapng)
            metadata=${capture%.*}.metadata.yml
            if [[ ! -f $metadata ]]; then
                echo "error: public capture has no metadata sidecar: $capture" >&2
                exit 1
            fi
            for marker in 'synthetic: true' 'contains_real_vehicle_data: false' 'generator_commit:'; do
                if ! grep -Fq "$marker" "$metadata"; then
                    echo "error: capture metadata is missing '$marker': $metadata" >&2
                    exit 1
                fi
            done
            ;;
        *)
            echo "error: capture outside evidence/public-fixtures: $capture" >&2
            exit 1
            ;;
    esac
done < <(find . -path './.git' -prune -o -type f \( -name '*.pcap' -o -name '*.pcapng' \) -print)

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
