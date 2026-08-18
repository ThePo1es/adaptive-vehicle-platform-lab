# Compiler Analysis Track

LLVM 활동은 차량 프로젝트의 critical C/C++ 모듈을 분석하는 지속 트랙입니다. 같은 corpus로 신뢰성, 코드 크기, 실행시간을 확인합니다.

## Corpus

```text
compiler-analysis/
├── can-decode/
├── crc-checksum/
├── ring-buffer/
├── uds-parser/
├── state-machine/
├── signal-processing/
└── report.md
```

각 디렉터리는 source, test, build script, raw results, generated IR/assembly를 재생성하는 명령을 가집니다. 생성물을 무조건 커밋하지 않고 재현 비용과 review 가치가 있을 때만 최소 증거를 보존합니다.

## Experiment matrix

| Dimension | Values |
| --- | --- |
| Compiler | GCC, Clang |
| Optimization | `-O0`, `-O2`, compiler/version이 지원하는 size profile |
| Link optimization | LTO off/on |
| Language | C, equivalent C++ where meaningful |
| Target | Cortex-M, AArch64 |
| Safety checks | warnings, UBSan/ASan where target permits, static analysis |
| Output | Clang LLVM IR, GCC GIMPLE/RTL dump, assembly, section/code size, runtime/cycle, stack |

## Per-function questions

- Clang에서는 source construct가 어떤 LLVM IR과 instruction으로 내려가는가?
- GCC에서는 같은 construct가 GIMPLE/RTL과 assembly에서 어떻게 보이는가?
- optimization이 제거·결합·vectorize한 것은 무엇인가?
- compiler가 가정한 UB가 실제 차량 입력에서 가능한가?
- load/store, branch, call, stack frame이 target별로 어떻게 다른가?
- size profile이 code size, latency, jitter에 어떤 trade-off를 만드는가?
- C++ abstraction이 zero-cost인지, code bloat/lifetime risk를 만드는가?
- benchmark가 실제 workload와 cache/timing behavior를 대표하는가?

## Required report

| Section | Content |
| --- | --- |
| Problem | 차량 모듈과 성능/신뢰성 질문 |
| Source contract | input bounds, ownership, alignment, concurrency |
| IR | optimization 전후 key transformation |
| Machine code | ABI, load/store, branch, vectorization, stack |
| Code size | text/data/bss and link map |
| Runtime | cycle/latency distribution and conditions |
| UB | sanitizer/static analysis and remaining blind spots |
| Decision | 어떤 구현/flag/target을 선택하며 왜 그런가 |
| Reproduction | exact commands, compiler version, commit |

## Connection to upstream LLVM

- 발견한 이상 동작이 source UB인지 optimizer/backend defect인지 먼저 분리합니다.
- 최소 IR/Clang reproducer와 target-independent/target-specific behavior를 비교합니다.
- Alive2 적용 가능 범위 또는 semantic proof limitation을 적습니다.
- failing test와 expected behavior를 정한 뒤 patch를 작성합니다.
- upstream 결과가 local 차량 코드에 주는 영향은 별도 workload로 측정합니다.

## Mastery gate

- [ ] 동일 corpus를 Cortex-M과 AArch64에서 자동 생성·비교한다.
- [ ] ABI와 assembly를 source/IR로 역추적한다.
- [ ] 최소 하나의 UB-induced miscompile-like symptom을 정확히 분류한다.
- [ ] 최소 하나의 optimizer/backend 이슈를 작은 reproducer와 failing test로 분석하고 reviewer feedback을 반영한다.
- [ ] code size와 runtime trade-off를 architecture budget에 반영한다.
