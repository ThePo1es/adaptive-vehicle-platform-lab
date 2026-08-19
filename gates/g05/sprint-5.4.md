# Sprint 5.4 — Zephyr로 P00-A 구성

추적 대상: `OUT-XCUT-G5`, `REQ-RTOS-001`, `REQ-RTOS-004`–`REQ-RTOS-006`. `FATAL-G5.4-RUNTIME`은 큐/stack overflow 또는 deadline miss가 관찰되지 않고 계속 실행되는 경우입니다.

## 시간과 기준 자료

26–34시간. G0에서 pin한 Zephyr release의 thread lifecycle, scheduling, interrupt, timer, workqueue, `k_msgq`, memory slab, userspace 적용 범위를 읽습니다. board와 RTOS release 조합은 manifest에 고정합니다.

큐 32개, allocation·deadline 보존식, 시간 배분은 [G5 실행 계약](contract.md) 5.4를 따릅니다.

## 구현 범위

Sprint 5.1의 task model을 acquisition, processing, communication, diagnostics, health thread로 옮깁니다. static stack과 크기가 정해진 queue를 기본으로 사용합니다. framework가 내부에서 만드는 system workqueue와 timer thread도 timing inventory에 넣습니다.

## 안내 실습

각 release에 scheduled time과 actual time을 붙이고 start·finish·deadline 결과를 binary trace에 남깁니다. ISR은 Sprint 4.3 큐 계약을 통해 work를 넘깁니다. 큐 포화, missed deadline, task overrun에 대해 count, event, 정해 둔 대응이 실행됩니다.

virtual clock으로 가능한 상태 logic은 host test에서 빠르게 돌리고, scheduler와 interrupt 동작은 board test로 분리합니다. configuration error는 boot 뒤 조용히 계속하지 않고 self-check 결과로 드러냅니다.

## 독립 실습

sensor sample부터 processed output까지 한 path를 완성합니다. sequence, 원천 timestamp, quality, stale policy를 payload에 넣고, producer restart와 큐 포화를 시험합니다. heap 사용 여부는 map과 allocation hook으로 확인합니다.

## 전이 과제

한 task의 WCET를 늘린 fixture와 interrupt phase를 옮긴 fixture를 차례로 적용합니다. overload counter와 fallback을 확인하고 낮은 중요도 work를 줄여 core path의 deadline을 회복합니다.

## 판정 기준

- 설정 task model과 생성된 thread priority·stack·period가 자동 대조됨
- 모든 큐·pool·stack에 상한, high-water mark, full/overflow response가 있음
- deadline miss와 overrun이 서로 구별되는 추적 event를 남김
- ISR에서 blocking call과 동적 할당을 사용하지 않음
- host logic test와 board scheduler test의 판정 범위를 구분
- overload에서도 health·fallback path가 정한 시간 안에 실행
- 초기화한 flash에서 P00-A smoke scenario를 한 명령 순서로 재현

## 최소 구성으로 돌아가는 기준

우선 acquisition과 health thread, 큐 하나만 남깁니다. 이 구성에서 다음을 다시 확인합니다.

- 설정 파일과 실제 priority가 일치한다.
- 큐 상한과 포화 처리가 보인다.
- overload 중에도 health 경로가 deadline 안에 돈다.

system thread의 priority 관계까지 설명되고 나면 communication과 diagnostics를 차례로 복구합니다.
