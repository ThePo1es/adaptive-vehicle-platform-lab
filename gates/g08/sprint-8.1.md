# Sprint 8.1 — Linux 프로세스 생명주기

## 시간과 기준 자료

24–30시간. POSIX.1-2024의 [`posix_spawn`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/posix_spawn.html), [`wait`/`waitpid`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/wait.html), [`kill`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/kill.html), [`setpgid`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/setpgid.html), Linux의 [`pidfd_open(2)`](https://man7.org/linux/man-pages/man2/pidfd_open.2.html)과 [cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)를 읽습니다. 사용한 libc와 kernel version을 실험 기록 첫 줄에 적습니다.

## 시작 조건과 fixture

P01 저장소에 `supervisor`, `child_fixture`, `lifecycle_test` 세 대상을 만듭니다. `child_fixture`는 인자로 다음 동작을 선택합니다.

- 즉시 0 또는 지정한 non-zero code로 종료
- SIGTERM을 받고 정리한 뒤 종료
- SIGTERM 무시
- grandchild를 하나 만든 뒤 부모만 종료
- `setsid()` 또는 double-fork로 기존 프로세스 group에서 이탈
- stdout/stderr를 번갈아 쓴 뒤 지정 시간 동안 대기

각 실행에는 `process_instance_id`, `pidfd`, cgroup identity를 묶은 handle을 붙입니다. PID는 로그용 관찰값이며 signal 대상의 identity로 단독 사용하지 않습니다.

## 안내 실습

`posix_spawn`으로 child를 시작하고 exit status를 수집합니다. executable 없음, permission 거부, child exit, signal 종료를 서로 다른 결과로 기록합니다. child마다 전용 프로세스 group과 cgroup을 만들고 `SIGTERM → grace period → cgroup-wide kill → reap` 순서로 닫습니다. subreaper는 이탈한 descendant의 종료 상태를 회수합니다.

## 독립 실습

동시에 세 child를 다루는 launcher를 작성합니다. stdout/stderr pipe는 non-blocking으로 읽고, supervisor가 종료될 때 열린 fd와 child 상태를 정리합니다. 종료 도중 새 child를 받지 않는 규칙도 테스트로 고정합니다.

## 전이 과제

봉인 고장 카드는 `grandchild가 SIGTERM을 무시함`, `setsid 뒤 double-fork`, `stop 요청과 자연 종료가 겹침`, `PID 재사용 뒤 stale timer` 중 하나입니다. 90분 안에 종료 이유, action 대상, 최종 reap 결과를 설명하고 자동 테스트를 추가합니다.

## 판정 기준

- 100회 반복 뒤 zombie와 fixture 프로세스가 0개
- 종료 요청부터 최종 reap까지 설정한 상한 이내
- 정상 종료, exit code, signal, spawn failure가 구조화 이벤트에서 구분됨
- `process_instance_id + pidfd + cgroup identity`로 실행 instance를 식별
- ASan/UBSan과 fd 누수 검사가 통과
- clean build 후 한 명이 README 명령만으로 전체 시나리오를 재현

## 힌트

1. signal handler에서는 async-signal-safe 동작만 남깁니다.
2. `waitpid`가 돌려준 PID와 status를 먼저 보관한 뒤 상태 머신에 전달합니다.
3. `/proc/<pid>/task/<pid>/children`과 `ps`는 조사 도구로 쓰고 합격 판정은 cgroup empty 상태와 reaped 이벤트로 확인합니다.

## PID 오인과 descendant 누락

descendant가 남거나, stale timer가 재사용된 PID에 action을 보내거나, `ECHILD`를 성공으로 뭉개면 다시 구현합니다. 보강 범위는 child 하나와 double-fork fixture 하나이며 spawn·TERM·cgroup kill·reap 순서를 50회 확인합니다.
