# Sprint 8.2 — 결정론적 Process Supervisor

## 시간과 기준 자료

22–28시간. [P01 설계 범위](../../projects/01-process-supervisor/README.md), POSIX의 [clock 선택 기준](https://pubs.opengroup.org/onlinepubs/9799919799/functions/V2_chap02.html), C++ working draft의 [`steady_clock`](https://eel.is/c++draft/time.clock.steady)을 읽습니다.

## 시작 조건과 입력

Sprint 8.1 launcher를 `ProcessLauncher` port 뒤에 둡니다. `Clock`, `TimerQueue`, `EventSink`도 교체 가능한 port로 만듭니다. 입력 policy는 `never`, `on-failure`, `always`, `max_attempts`, `initial_backoff`, `multiplier`, `max_backoff`, `stable_run_reset`을 포함합니다.

## 안내 실습

`Initializing`, `Running`, `Stopping`, `Exited`, `Backoff`, `Failed` 상태와 이벤트 표를 먼저 작성합니다. production에서는 monotonic clock을 쓰고 테스트에서는 수동으로 시간을 전진시킵니다. crash 세 번 뒤 backoff 값과 terminal 상태를 손으로 계산한 표를 oracle로 사용합니다.

## 독립 실습

여러 application을 독립적으로 감독합니다. restart budget은 sliding window로 제한하고, stable run을 만족했을 때만 attempt를 초기화합니다. supervisor 재시작 뒤 budget을 유지할지 초기화할지도 ADR로 고정합니다.

## 전이 과제

비공개 sequence에는 hanging child, stop과 crash 동시 발생, backoff 중 shutdown, clock jump 요청이 섞입니다. virtual time 테스트를 새로 작성해 한 번의 실행으로 최종 상태와 이벤트 순서를 판정합니다.

## 판정 기준

- 같은 seed와 이벤트 sequence에서 PID·실제 timestamp를 뺀 canonical 이벤트가 동일
- 테스트 suite에 실제 `sleep`이 없고 1초 안에 수 시간 분량의 backoff를 검증
- transition table의 모든 cell이 unit 테스트 또는 명시적 invalid 이벤트 테스트에 연결
- restart storm이 budget 상한에서 멈추고 이유가 남음
- stop 요청 후 재시작 timer가 child를 되살리지 않음
- model oracle과 구현을 1,000개 생성 sequence로 대조

## 힌트

1. 프로세스 이벤트를 받은 시점과 이벤트가 실제 발생한 시점을 구분합니다.
2. backoff 계산은 overflow와 상한 적용 순서를 테스트합니다.
3. 상태 전환 함수가 프로세스를 직접 실행하면 순수 모델 검사가 어려워집니다.

## 재시작 판단을 되돌릴 때

wall clock 변경이 restart 판단에 들어가거나, 한 child의 고장이 다른 application의 budget을 소비하거나, stop 뒤 재기동 경합이 남으면 재시험합니다. 단일 application 상태 머신으로 줄여 생성 sequence 200개를 다시 통과시킵니다.
