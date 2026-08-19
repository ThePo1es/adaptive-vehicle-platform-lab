#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repo_root=$(cd -- "$script_dir/.." && pwd)
cd "$repo_root"

required_files=(
    .python-version
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
    gates/g04/sprint-4.1.md
    gates/g04/sprint-4.2.md
    gates/g04/sprint-4.3.md
    gates/g04/sprint-4.4.md
    gates/g04/sprint-4.5.md
    gates/g04/sprint-4.6.md
    gates/g04/contract.md
    gates/g05/sprint-5.1.md
    gates/g05/sprint-5.2.md
    gates/g05/sprint-5.3.md
    gates/g05/sprint-5.4.md
    gates/g05/sprint-5.5.md
    gates/g05/sprint-5.6.md
    gates/g05/sprint-5.7.md
    gates/g05/contract.md
    gates/g06/sprint-6.1.md
    gates/g06/sprint-6.2.md
    gates/g06/sprint-6.3.md
    gates/g06/sprint-6.4.md
    gates/g06/sprint-6.5.md
    gates/g06/sprint-6.6.md
    gates/g06/sprint-6.7.md
    gates/g06/sprint-6.8.md
    gates/g06/bench-contract.md
    gates/g06/contract.md
    gates/g07/sprint-7.1.md
    gates/g07/sprint-7.2.md
    gates/g07/sprint-7.3.md
    gates/g07/sprint-7.4.md
    gates/g07/sprint-7.5.md
    gates/g07/sprint-7.6.md
    gates/g07/contract.md
    gates/g07/source-ledger.md
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
    gates/g11/sprint-11.5.md
    gates/g11/sprint-11.6.md
    gates/g11/sprint-11.7.md
    gates/g11/assurance-contract.md
    gates/g12/sprint-12.1.md
    gates/g12/sprint-12.2.md
    gates/g12/sprint-12.3.md
    gates/g12/sprint-12.4.md
    gates/g12/sprint-12.5.md
    gates/g12/sprint-12.6.md
    gates/g12/sprint-12.7.md
    gates/g12/sprint-12.8.md
    gates/g12/sprint-12.9.md
    gates/g12/sprint-12.10.md
    gates/g12/sprint-12.11.md
    gates/g12/sprint-12.12.md
    gates/g12/contract.md
    fixtures/README.md
    fixtures/g05/task-set-v1.yml
    fixtures/g06/can-fd-dlc-v1.csv
    fixtures/g06/can-rta-three-message-v1.json
    fixtures/g06/isotp-rx-v1.yml
    fixtures/g06/uds-read-v1.yml
    fixtures/g07/classic-config-v1.yml
    fixtures/g07/dtc-journal-reset-v1.json
    fixtures/g07/mode-security-permutations-v1.json
    fixtures/g10/release-map-cases-v1.json
    fixtures/g10/review-manifest-v1.json
    fixtures/g11/assurance-change-v1.json
    fixtures/g12/integration-contract-v1.json
    labs/g10_1_release_map/README.md
    labs/g10_1_release_map/r25-11-document-lock.json
    labs/g10_1_release_map/trusted-reviewers.json
    labs/g10_1_release_map/validator.py
    labs/g10_1_release_map/run_harness.py
    labs/g10_1_release_map/starter/release-map.json
    labs/g10_1_release_map/tests/test_release_map.py
    sources/autosar-r25-11/README.md
    evidence/runnable/g10.1/README.md
    evidence/runnable/g10.1/harness.stdout
    evidence/runnable/g10.1/harness-v2.stdout
    evidence/runnable/g10.1/harness-v3.stdout
    evidence/runnable/g10.1/repository-check-v2.stdout
    evidence/runnable/g10.1/repository-check-v2.stderr
    evidence/runnable/g10.1/repository-check-v3.stdout
    evidence/runnable/g10.1/repository-check-v3.stderr
    evidence/runnable/g10.1/run-manifest.json
    evidence/runnable/g10.1/run-manifest-v2.json
    evidence/runnable/g10.1/run-manifest-v3.json
    evidence/runnable/index.json
    projects/00-mcu-rtos-ecu/README.md
    projects/05-can-ethernet-vertical-slice/README.md
    projects/06-heterogeneous-vehicle-platform/README.md
    scripts/check_fixture_semantics.py
    scripts/check_runnable_evidence.py
)

for file in "${required_files[@]}"; do
    if [[ ! -f $file ]]; then
        echo "error: required file is missing: $file" >&2
        exit 1
    fi
done

documented_lab_files=(
    gates/g00/sprint-*.md
    gates/g01/sprint-*.md
    gates/g02/sprint-*.md
    gates/g03/sprint-*.md
    gates/g04/sprint-*.md
    gates/g05/sprint-*.md
    gates/g06/sprint-*.md
    gates/g07/sprint-*.md
    gates/g08/sprint-*.md
    gates/g09/sprint-*.md
    gates/g10/sprint-*.md
    gates/g11/sprint-*.md
    gates/g12/sprint-*.md
)

if (( ${#documented_lab_files[@]} != 91 )); then
    echo "error: expected 91 documented lab packs, found ${#documented_lab_files[@]}" >&2
    exit 1
fi

for file in "${documented_lab_files[@]}"; do
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
python3 -c 'import ast, pathlib; [ast.parse(pathlib.Path(path).read_text(encoding="utf-8")) for path in ("scripts/check_internal_links.py", "scripts/check_traceability.py", "scripts/check_fixture_semantics.py", "scripts/check_runnable_evidence.py", "labs/g10_1_release_map/validator.py", "labs/g10_1_release_map/run_harness.py", "labs/g10_1_release_map/tests/test_release_map.py")]'
python3 scripts/check_internal_links.py
python3 scripts/check_traceability.py
python3 scripts/check_fixture_semantics.py
python3 labs/g10_1_release_map/run_harness.py
unit_output=$(python3 -m unittest discover -s labs/g10_1_release_map/tests -p 'test_*.py' 2>&1)
if ! grep -Fq 'Ran 10 tests' <<<"$unit_output" || ! grep -Fxq 'OK' <<<"$unit_output"; then
    printf '%s\n' "$unit_output" >&2
    echo "error: G10.1 unit-test count or result changed" >&2
    exit 1
fi
echo "G10.1 unit tests: OK (10 tests)"
if [[ ${SKIP_RUNNABLE_EVIDENCE:-0} != 1 ]]; then
    python3 scripts/check_runnable_evidence.py
fi

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
