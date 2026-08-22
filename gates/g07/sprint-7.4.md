# Sprint 7.4 — DEM-like event와 NvM-like journal

추적 대상: `OUT-XCUT-G7`, `REQ-DTC-001`, `REQ-DTC-002`, `REQ-CP-MEM-001`. `FATAL-G7.4-JOURNAL`은 corrupt/torn 기록 채택 또는 generation이 섞인 DTC snapshot입니다.

## 시간과 기준 자료

24–30시간. [R25-11 자료 장부](source-ledger.md)의 DEM, NvM 책임과 G6 DTC read model, [DTC journal reset 입력](../../fixtures/g07/dtc-journal-reset-v1.json)을 읽습니다. 허용 reboot 상태는 [G7 실행 계약](contract.md) 7.4에 고정합니다. CRC는 우발 corruption 탐지 범위로 한정합니다.

## reference model

event debounce, pending/confirmed/healed, occurrence, aging, snapshot, clear policy를 실행 가능한 상태 model로 둡니다. DTC ID와 event ID ownership, update transaction, read snapshot의 일관성을 정의합니다.

## 안내 실습

합성 event를 DEM-like component가 받아 DTC state와 metadata를 갱신하고, NvM-like append journal에 schema version, sequence, length, CRC, commit marker와 함께 저장합니다. reboot에서는 마지막으로 commit된 유효 기록 또는 설정 기본값만 선택합니다.

G6 `0x19` read는 immutable snapshot을 조회합니다. update와 read가 겹쳐도 서로 다른 generation의 field가 한 response에 섞이지 않게 합니다.

## 독립 실습

bit flip, torn header/body/commit, duplicated sequence, schema upgrade, full storage corpus를 만듭니다. compaction 중 reset과 endurance budget을 host fault injection으로 먼저 검증하고, 실제 flash run 횟수는 제한합니다.

## 전이 과제

debounce threshold, 기록 version, reset point가 달라진 세 run을 받습니다. executable model, persisted bytes, reboot 상태, UDS response를 대조해 차이를 설명합니다.

## 판정 기준

- event와 DTC transition이 executable model과 일치
- torn/corrupt record가 committed state로 선택되지 않음
- reboot 결과가 last committed valid 또는 documented default 중 하나임
- concurrent read가 generation-consistent snapshot을 반환
- journal full·compaction reset 뒤 정한 시간 안에 복구 가능
- CRC의 비보안 성격과 flash endurance 가정이 문서화됨
- DCM, DEM-like 책임 주체, NvM-like store가 분리됨

## 전원 차단 재현 절차

기록 두 개와 commit marker 하나로 작은 journal을 만듭니다. write 경계마다 reset을 넣고 부팅 결과를 `이전 commit / 새 commit / 기본값` 가운데 하나로 분류합니다.

가장 큰 sequence만 고르거나 손상 record를 부분 복구한 결과가 나오면 해당 경계를 고친 뒤 모든 reset 지점을 처음부터 다시 돕니다.
