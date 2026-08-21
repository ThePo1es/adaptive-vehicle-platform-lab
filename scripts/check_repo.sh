#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repo_root=$(cd -- "$script_dir/.." && pwd)
cd "$repo_root"

python_cmd=python
if ! "$python_cmd" -c 'import sys; raise SystemExit(sys.version_info[:2] != (3, 12))' >/dev/null 2>&1; then
    python_cmd=python3
fi
if ! "$python_cmd" -c 'import sys; raise SystemExit(sys.version_info[:2] != (3, 12))' >/dev/null 2>&1; then
    echo "error: Python 3.12 is required" >&2
    exit 1
fi

required_files=(
    .python-version
    pytest.ini
    LICENSE.md
    README.md
    ROADMAP.md
    ASSESSMENTS.md
    PROGRESS.md
    SECURITY.md
    THIRD_PARTY_NOTICES.md
    toolchain/pyproject.toml
    toolchain/uv.lock
    toolchain/README.md
    .github/workflows/code-build.yml
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
    assessments/g02-embedded-cpp.md
    assessments/g03-compiler-analysis.md
    gates/README.md
    gates/g00/sprint-0.1.md
    gates/g00/sprint-0.2.md
    gates/g01/sprint-1.1.md
    gates/g01/sprint-1.2.md
    gates/g01/sprint-1.3.md
    gates/g01/sprint-1.4.md
    gates/g01/sprint-1.5.md
    gates/g01/README.md
    gates/g01/contract.md
    gates/g02/sprint-2.1.md
    gates/g02/sprint-2.2.md
    gates/g02/sprint-2.3.md
    gates/g02/sprint-2.4.md
    gates/g02/README.md
    gates/g02/contract.md
    gates/g03/sprint-3.1.md
    gates/g03/sprint-3.2.md
    gates/g03/sprint-3.3.md
    gates/g03/sprint-3.4.md
    gates/g03/sprint-3.5.md
    gates/g03/README.md
    gates/g03/contract.md
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
    fixtures/g01/sprint-1.1-v1.h
    fixtures/g01/sprint-1.2-v1.h
    fixtures/g01/sprint-1.3-v1.h
    fixtures/g01/sprint-1.4-v1.h
    fixtures/g01/sprint-1.5-v1.h
    fixtures/g01/retest-1.1-v1.h
    fixtures/g01/retest-1.2-v1.h
    fixtures/g01/retest-1.3-v1.h
    fixtures/g01/retest-1.4-v1.h
    fixtures/g01/retest-1.5-v1.h
    fixtures/g02/sprint-2.1-v1.hpp
    fixtures/g02/sprint-2.2-v1.hpp
    fixtures/g02/sprint-2.3-v1.hpp
    fixtures/g02/sprint-2.4-v1.hpp
    fixtures/g02/retest-2.1-v1.hpp
    fixtures/g02/retest-2.2-v1.hpp
    fixtures/g02/retest-2.3-v1.hpp
    fixtures/g02/retest-2.4-v1.hpp
    fixtures/g03/README.md
    fixtures/g03/input-a.tsv
    fixtures/g03/input-b.tsv
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
    labs/g10_1_release_map/review-policy.json
    labs/g10_1_release_map/review-policy.authority-a.sshsig
    labs/g10_1_release_map/review-policy.authority-b.sshsig
    labs/g10_1_release_map/trusted-reviewers.json
    labs/g10_1_release_map/validator.py
    labs/g10_1_release_map/run_harness.py
    labs/g10_1_release_map/starter/release-map.json
    labs/g10_1_release_map/tests/test_release_map.py
    labs/g01_safe_c/README.md
    labs/__init__.py
    labs/g01_safe_c/__init__.py
    labs/g01_safe_c/include/g01_lab.h
    labs/g01_safe_c/reference/codec.c
    labs/g01_safe_c/reference/storage.c
    labs/g01_safe_c/reference/parser.c
    labs/g01_safe_c/reference/driver.c
    labs/g01_safe_c/starter/codec.c
    labs/g01_safe_c/starter/storage.c
    labs/g01_safe_c/starter/parser.c
    labs/g01_safe_c/starter/driver.c
    labs/g01_safe_c/tests/test_run_harness.py
    labs/g01_safe_c/harness_toolchain.py
    labs/g01_safe_c/run_harness.py
    labs/g02_embedded_cpp/README.md
    labs/g02_embedded_cpp/__init__.py
    labs/g02_embedded_cpp/elf_contract.py
    labs/g02_embedded_cpp/harness_toolchain.py
    labs/g02_embedded_cpp/run_harness.py
    labs/g02_embedded_cpp/include/g02_abi.hpp
    labs/g02_embedded_cpp/include/g02_abi_c.h
    labs/g02_embedded_cpp/include/g02_lifetime.hpp
    labs/g02_embedded_cpp/include/g02_queue.hpp
    labs/g02_embedded_cpp/include/g02_runtime.hpp
    labs/g02_embedded_cpp/reference/abi.cpp
    labs/g02_embedded_cpp/reference/lifetime.cpp
    labs/g02_embedded_cpp/reference/queue.cpp
    labs/g02_embedded_cpp/reference/runtime.cpp
    labs/g02_embedded_cpp/starter/abi.cpp
    labs/g02_embedded_cpp/starter/lifetime.cpp
    labs/g02_embedded_cpp/starter/queue.cpp
    labs/g02_embedded_cpp/starter/runtime.cpp
    labs/g02_embedded_cpp/tests/test_abi.cpp
    labs/g02_embedded_cpp/tests/test_c_abi_header.c
    labs/g02_embedded_cpp/tests/test_lifetime.cpp
    labs/g02_embedded_cpp/tests/test_queue.cpp
    labs/g02_embedded_cpp/tests/test_run_harness.py
    labs/g02_embedded_cpp/tests/test_runtime.cpp
    labs/g02_embedded_cpp/tests/test_support.hpp
    labs/g02_embedded_cpp/freestanding/manual.cpp
    labs/g02_embedded_cpp/freestanding/static.cpp
    labs/g02_embedded_cpp/freestanding/virtual.cpp
    labs/g03_compiler_analysis/README.md
    labs/g03_compiler_analysis/__init__.py
    labs/g03_compiler_analysis/answers.py
    labs/g03_compiler_analysis/contracts.py
    labs/g03_compiler_analysis/elf_checks.py
    labs/g03_compiler_analysis/run_harness.py
    labs/g03_compiler_analysis/submission.py
    labs/g03_compiler_analysis/toolchain.py
    labs/g03_compiler_analysis/reference/arm32_call_path.c
    labs/g03_compiler_analysis/reference/aarch64_error_recovery.c
    labs/g03_compiler_analysis/reference/aarch64_error_recovery.answers
    labs/g03_compiler_analysis/reference/c_to_ir_to_machine.c
    labs/g03_compiler_analysis/reference/fair_compiler_comparison.c
    labs/g03_compiler_analysis/reference/compiler_issue_decision.answers
    labs/g03_compiler_analysis/starter/arm32_call_path.c
    labs/g03_compiler_analysis/starter/aarch64_error_recovery.c
    labs/g03_compiler_analysis/starter/aarch64_error_recovery.answers
    labs/g03_compiler_analysis/starter/c_to_ir_to_machine.c
    labs/g03_compiler_analysis/starter/fair_compiler_comparison.c
    labs/g03_compiler_analysis/starter/compiler_issue_decision.answers
    labs/g03_compiler_analysis/tests/test_contracts.py
    labs/g03_compiler_analysis/tests/test_run_harness.py
    labs/g03_compiler_analysis/mutants/101_missing_call.c
    labs/g03_compiler_analysis/mutants/201_hidden_symbol.c
    labs/g03_compiler_analysis/mutants/301_wrong_boundary.c
    labs/g03_compiler_analysis/mutants/401_missing_crc.c
    labs/g03_compiler_analysis/mutants/501_fake_upstream.answers
    portfolio/g01-safe-c-components-v1/CMakeLists.txt
    portfolio/g01-safe-c-components-v1/README.md
    portfolio/g01-safe-c-components-v1/demo.c
    portfolio/g02-embedded-cpp-runtime-v1/ADR-template.md
    portfolio/g02-embedded-cpp-runtime-v1/CMakeLists.txt
    portfolio/g02-embedded-cpp-runtime-v1/README.md
    portfolio/g02-embedded-cpp-runtime-v1/demo.cpp
    portfolio/g02-embedded-cpp-runtime-v1/demo_c.c
    portfolio/g03-compiler-analysis-v1/README.md
    portfolio/g03-compiler-analysis-v1/report-template.md
    sources/autosar-r25-11/README.md
    evidence/runnable/g10.1/README.md
    evidence/runnable/g10.1/harness.stdout
    evidence/runnable/g10.1/harness-v2.stdout
    evidence/runnable/g10.1/harness-v3.stdout
    evidence/runnable/g10.1/harness-v4.stdout
    evidence/runnable/g10.1/harness-v5.stdout
    evidence/runnable/g10.1/harness-v5.stderr
    evidence/runnable/g10.1/harness-v6.stdout
    evidence/runnable/g10.1/harness-v6.stderr
    evidence/runnable/g10.1/repository-check-v2.stdout
    evidence/runnable/g10.1/repository-check-v2.stderr
    evidence/runnable/g10.1/repository-check-v3.stdout
    evidence/runnable/g10.1/repository-check-v3.stderr
    evidence/runnable/g10.1/repository-check-v4.stdout
    evidence/runnable/g10.1/repository-check-v4.stderr
    evidence/runnable/g10.1/repository-check-v5.stdout
    evidence/runnable/g10.1/repository-check-v5.stderr
    evidence/runnable/g10.1/repository-check-v6.stdout
    evidence/runnable/g10.1/repository-check-v6.stderr
    evidence/runnable/g10.1/run-manifest.json
    evidence/runnable/g10.1/run-manifest-v2.json
    evidence/runnable/g10.1/run-manifest-v3.json
    evidence/runnable/g10.1/run-manifest-v4.json
    evidence/runnable/g10.1/run-manifest-v5.json
    evidence/runnable/g10.1/run-manifest-v6.json
    evidence/runnable/index.json
    projects/00-mcu-rtos-ecu/README.md
    projects/05-can-ethernet-vertical-slice/README.md
    projects/06-heterogeneous-vehicle-platform/README.md
    scripts/check_fixture_semantics.py
    scripts/check_runnable_evidence.py
    scripts/runnable_evidence_replay.py
    scripts/runnable_evidence_support.py
    scripts/runnable_evidence_validator.py
    scripts/tests/test_check_runnable_evidence.py
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
"$python_cmd" -c 'import ast, pathlib; [ast.parse(pathlib.Path(path).read_text(encoding="utf-8")) for path in ("scripts/check_internal_links.py", "scripts/check_traceability.py", "scripts/check_fixture_semantics.py", "scripts/check_runnable_evidence.py", "scripts/runnable_evidence_replay.py", "scripts/runnable_evidence_support.py", "scripts/runnable_evidence_validator.py", "scripts/tests/test_check_runnable_evidence.py", "labs/g01_safe_c/harness_toolchain.py", "labs/g01_safe_c/run_harness.py", "labs/g01_safe_c/tests/test_run_harness.py", "labs/g02_embedded_cpp/elf_contract.py", "labs/g02_embedded_cpp/harness_toolchain.py", "labs/g02_embedded_cpp/run_harness.py", "labs/g02_embedded_cpp/tests/test_run_harness.py", "labs/g03_compiler_analysis/answers.py", "labs/g03_compiler_analysis/contracts.py", "labs/g03_compiler_analysis/elf_checks.py", "labs/g03_compiler_analysis/run_harness.py", "labs/g03_compiler_analysis/submission.py", "labs/g03_compiler_analysis/toolchain.py", "labs/g03_compiler_analysis/tests/test_contracts.py", "labs/g03_compiler_analysis/tests/test_run_harness.py", "labs/g10_1_release_map/validator.py", "labs/g10_1_release_map/run_harness.py", "labs/g10_1_release_map/tests/test_release_map.py")]'
"$python_cmd" scripts/check_internal_links.py
"$python_cmd" scripts/check_traceability.py
"$python_cmd" scripts/check_fixture_semantics.py
"$python_cmd" -m labs.g01_safe_c.run_harness
G01_LAB_ID=G1.RETEST "$python_cmd" -m labs.g01_safe_c.run_harness
"$python_cmd" -m labs.g02_embedded_cpp.run_harness
G02_LAB_ID=G2.RETEST "$python_cmd" -m labs.g02_embedded_cpp.run_harness
"$python_cmd" -m labs.g03_compiler_analysis.run_harness
"$python_cmd" labs/g10_1_release_map/run_harness.py
unit_output=$("$python_cmd" -m unittest discover -s labs/g10_1_release_map/tests -p 'test_*.py' 2>&1)
if ! grep -Fq 'Ran 14 tests' <<<"$unit_output" || ! grep -Fxq 'OK' <<<"$unit_output"; then
    printf '%s\n' "$unit_output" >&2
    echo "error: G10.1 unit-test count or result changed" >&2
    exit 1
fi
echo "G10.1 unit tests: OK (14 tests)"
if [[ ${SKIP_RUNNABLE_EVIDENCE:-0} != 1 ]]; then
    "$python_cmd" -m scripts.check_runnable_evidence
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
