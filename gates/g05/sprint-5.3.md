# Sprint 5.3 — Priority inversion과 blocking bound

추적 대상: `OUT-XCUT-G5`, `REQ-RTOS-003`. `FATAL-G5.3-LOCK`은 지원되지 않는 mutex protocol을 가정하거나 lock cycle을 합격시킨 경우입니다.

## 시간과 기준 자료

22–28시간. RTOS mutex, priority inheritance 지원 범위, ceiling 또는 lock ordering 문서와 scheduler 추적 방법을 읽습니다. binary semaphore를 mutex 대용으로 쓸 때 사라지는 보장을 따로 적습니다.

시험 입력, blocking 오차, 산출물 인계는 [G5 실행 계약](contract.md) 5.3에 있습니다.

## 재현할 장면

low task가 lock을 잡고, high task가 그 lock을 기다리며, medium task가 low task를 밀어내는 세-task 실험을 만듭니다. GPIO 또는 추적 event로 lock request/acquire/release와 context switch를 표시합니다.

## 안내 실습

보호 없음, priority inheritance, 지원된다면 ceiling/priority-protect 구성을 같은 workload로 비교합니다. high task의 blocking interval, low task의 effective priority, medium task 실행을 원시 추적 기록에서 계산합니다. 추적 overhead를 별도 calibration합니다.

recursive lock, timeout, 소유 task 종료, ISR access, lock order를 API contract에 포함합니다. RTOS가 제공하지 않는 protocol은 제공한다고 가정하지 않고 애플리케이션 구조 변경으로 해결합니다.

## 독립 실습

P00-A의 shared object를 하나 골라 critical section 최대 길이와 접근 task를 측정합니다. Sprint 5.2의 `B_i`가 실제 lock graph에서 나온 bound인지 검토하고, 긴 I/O나 log가 lock 안에 있으면 밖으로 이동합니다.

## 전이 과제

nested lock, timeout path, 같은 priority waiter가 들어간 낯선 workload를 실행합니다. deadlock 또는 예상보다 긴 blocking을 trace로 재현하고, lock ordering·ownership·message passing 중 가장 작은 수정으로 해결합니다.

## 판정 기준

- 세-task inversion이 반복 실행에서 같은 순서로 재현됨
- 선택 protocol 전후 high-task blocking을 raw trace에서 산출
- 분석의 blocking bound가 측정한 critical section과 lock graph를 포괄
- ISR이 blocking mutex를 획득하는 경로가 없음
- timeout·cancel 뒤 mutex owner와 protected state가 일관됨
- lock-order cycle을 정적 표 또는 runtime test가 잡음

## 수정 검토 질문

수정 뒤에도 세 질문에 답할 수 있어야 합니다. high task가 왜 기다렸는가? 그 대기 시간은 계산한 blocking bound 안에 있는가? 취소 뒤 lock 소유자는 누구인가?

priority를 최고값으로 고정하거나 interrupt 차단 구간을 넓힌 답안은 되돌립니다. lock 하나와 task 세 개에서 protocol을 다시 확인한 뒤 실제 구성 요소에 옮깁니다.
