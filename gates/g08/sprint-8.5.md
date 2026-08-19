# Sprint 8.5 — Linux 서비스 격리와 자원 통제

## 시간과 기준 자료

24–30시간. systemd의 [`systemd.service`](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html), [`systemd.exec`](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html), [`systemd.resource-control`](https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html), Linux kernel의 [cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html), [seccomp filter](https://docs.kernel.org/userspace-api/seccomp_filter.html), Linux man-pages의 [`capabilities(7)`](https://man7.org/linux/man-pages/man7/capabilities.7.html)을 읽습니다.

## 시작 조건과 기준선

P01을 전용 user와 systemd unit으로 실행합니다. hardening 전 기능 test, syscall 목록, peak memory, CPU workload, 열린 경로·socket을 기록합니다. policy는 관찰 결과와 요구사항에서 한 줄씩 근거를 붙입니다.

## 안내 실습

`NoNewPrivileges`, filesystem 보호, private temporary directory, 제한된 capability set을 단계별로 적용합니다. 한 옵션씩 켤 때마다 기능 test를 돌립니다. cgroup v2로 memory, CPU, PID 상한을 설정하고 실제 cgroup 파일과 systemd 속성이 일치하는지 확인합니다.

## 독립 실습

seccomp allowlist 또는 deny policy를 적용합니다. P01이 필요한 syscall을 release별로 기록하고, 금지한 syscall을 호출하는 fixture가 예상한 signal 또는 errno로 막히는지 자동 시험합니다. memory pressure와 fork storm에서도 host를 위험하게 만들지 않는 작은 상한을 사용합니다.

## 전이 과제

검토자가 writable path, capability, syscall, resource limit 중 하나를 더 줄입니다. 실패한 기능을 찾아 최소 권한으로 복원하고 policy diff와 근거를 제출합니다.

## 판정 기준

- hardening 전후의 동일 기능 suite가 통과
- forbidden write, privilege escalation, denied syscall test가 각각 실패 이유를 확인
- memory·PID 한도 초과가 host 전체 장애로 번지지 않음
- service restart 횟수와 cgroup OOM/exit 이유가 audit log에 남음
- `systemd-analyze security` 결과와 남은 exposure의 이유를 기록
- production unit, test override, 개발 편의 설정이 분리됨

## 힌트

1. root로 실행한 뒤 옵션만 늘리는 방식은 capability 설계를 놓치기 쉽습니다.
2. seccomp profile은 architecture와 libc 차이를 test matrix에 넣습니다.
3. resource limit의 단위와 burst 허용 방식을 실험 기록에 적습니다.

## 치명적 실패와 보충

기능 test가 깨진 상태를 hardening 성공으로 처리하거나, 무제한 fork·memory fixture를 host에서 직접 돌리거나, 이유 없이 broad capability를 남기면 실패입니다. 보충 과제는 전용 VM에서 P01 단일 기능과 세 policy test만 다시 구성하는 것입니다.
