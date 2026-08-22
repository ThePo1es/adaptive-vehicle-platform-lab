# Sprint 5.1 — 요구에서 task model로

추적 대상: `OUT-XCUT-G5`, `REQ-RTOS-002`, `REQ-ARCH-001`. `FATAL-G5.1-MODEL`은 arrival, deadline, execution bound, blocking이 빠진 task를 구현 기준선으로 승인한 경우입니다.

## 시간과 기준 자료

22–28시간. Zephyr v4.4.0 scheduler·interrupt 문서와 고정 우선순위 scheduling 자료를 사용합니다. 공통 입력, 수치 판정, 시간 분해는 [G5 실행 계약](contract.md) 5.1과 [task-set-v1](../../fixtures/g05/task-set-v1.yml)에 고정했습니다.

## 모델을 만들기 전

periodic, sporadic, aperiodic event를 구분하고 release, start, finish, response time, deadline의 관찰 지점을 그립니다. ISR에서 깨우는 task는 ISR과 task 실행 시간을 따로 잡습니다.

## 안내 실습

각 task에 period 또는 minimum inter-arrival time, relative deadline, priority, CPU affinity, provisional WCET, release jitter, shared resource, blocking 후보, stack budget을 배정합니다. project에서 바꾼 수치는 `config/task_set.yml` 한 곳에 둡니다. end-to-end path에는 sensor timestamp부터 actuator 또는 publish 지점까지 별도 deadline을 둡니다.

수치를 추측한 근거를 `measured / datasheet / conservative placeholder`로 나눕니다. CPU utilization, critical instant, harmonic 관계를 계산하고 현재 모델로 답할 수 없는 질문을 uncertainty 목록에 남깁니다.

## 독립 실습

요구사항 하나를 골라 stimulus→task release→shared resource→observable response 경로를 추적합니다. overload, 큐 포화, deadline miss 때 계속할 기능과 중단할 기능을 hazard/functional analysis의 현재 가정에 맞춰 정합니다.

## 전이 과제

요구 변경 카드는 sensor rate 두 배, diagnostic burst, 더 짧은 end-to-end deadline 중 하나입니다. task split, 큐 정책, 기능 축소를 포함한 두 대안을 수치로 비교합니다.

## 판정 기준

- 모든 task에 period/arrival, deadline, priority, execution bound, jitter, blocking 후보가 있음
- ISR 시간과 deferred task 시간이 별도 budget으로 잡힘
- end-to-end path의 release와 completion 관찰 지점이 명확함
- placeholder WCET가 측정값처럼 표시되지 않음
- utilization 계산과 설정 parser test가 같은 수치를 사용
- overload response가 REQ-RTOS-004와 safety 기록에 연결됨

## 모델 변경 기록

하나의 task 안에 서로 다른 arrival이 섞였으면 event와 실행 문맥을 나눕니다. deadline의 기준 시점이 달라진 경우에는 이전 계산을 폐기하고 release 지점부터 정의합니다.

수치를 고칠 때는 값만 덮어쓰지 말고 `변경 전 값 / 바꾼 이유 / 영향받는 task`를 ADR에 적습니다. 그 표를 기준으로 계산을 다시 시작합니다.
