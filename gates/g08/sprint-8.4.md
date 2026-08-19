# Sprint 8.4 — 크래시와 멈춤 진단

## 시간과 기준 자료

18–24시간. [GDB manual](https://sourceware.org/gdb/current/onlinedocs/gdb.html), [strace 문서](https://strace.io/), Linux kernel의 [perf 문서](https://docs.kernel.org/tools/perf/index.html), systemd의 [`coredumpctl`](https://www.freedesktop.org/software/systemd/man/latest/coredumpctl.html)을 읽습니다. 개발 host가 core를 저장하는 방식을 먼저 확인합니다.

## 시작 조건과 incident corpus

별도 branch에 네 고장을 심습니다: null dereference, use-after-free, mutex deadlock, blocking syscall hang. binary는 build ID와 debug symbol을 보존하고 릴리스 binary와 symbol file의 hash를 짝으로 기록합니다.

## 안내 실습

null dereference를 core에서 열어 signal, thread, backtrace, register, faulting source를 찾습니다. hang은 `strace -f`와 thread backtrace로 마지막 syscall과 대기 관계를 확인합니다. 처음 20분은 코드를 고치지 않고 관찰 자료만 모읍니다.

## 독립 실습

검토자가 고장 하나를 골라 이름을 가린 incident bundle을 줍니다. 증상 재현, 영향 범위, 첫 잘못된 상태, root cause, 최소 수정, regression 테스트 순서로 incident report를 작성합니다. CPU saturation 사례에는 `perf stat`과 `perf record`를 추가합니다.

## 전이 과제

symbol이 분리된 대상 core 또는 최적화된 binary를 받습니다. build ID를 맞춰 symbol을 찾고 inline·optimized-out 상태를 고려해 결론의 확실성을 `confirmed`, `supported`, `open`으로 표시합니다.

## 판정 기준

- clean 환경에서 증상을 재현하는 단일 명령 또는 script
- core와 binary의 build ID가 일치
- symptom, trigger, root cause, contributing condition이 구분됨
- 수정 전 실패하고 수정 후 통과하는 regression 테스트
- hang 진단에서 모든 관련 thread와 프로세스를 조사
- 보고서의 각 결론이 log, trace, core 위치 중 하나에 연결

## 조사 순서

1. core가 없으면 `ulimit`, `core_pattern`, systemd-coredump 설정을 확인합니다.
2. `strace` 자체가 timing을 바꿀 수 있으므로 재현 횟수와 관찰 영향을 적습니다.
3. `perf` sample 비율을 함수 실행 시간으로 단정하지 않습니다.

## 분석을 다시 해야 하는 경우

증상만으로 원인을 정했거나 다른 빌드의 심벌을 붙였거나 회귀 테스트 없이 고쳤다면 분석 기록을 사용하지 않습니다. 공개 크래시 입력 하나로 core 수집부터 수정 전후 테스트까지 다시 이어 봅니다.
