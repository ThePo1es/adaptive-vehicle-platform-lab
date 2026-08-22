# Sprint 7.2 — CanIf–PduR–COM–RTE vertical slice

추적 대상: `OUT-XCUT-G7`, `REQ-CP-COM-001`, `REQ-CP-SEC-001`. `FATAL-G7.2-COM`은 route 책임 혼합, invalid input 반영, E2E를 authenticity로 설명한 경우입니다.

## 시간과 기준 자료

26–32시간. [R25-11 자료 장부](source-ledger.md)의 Can Driver, CanIf, PduR, COM, RTE, E2E 절과 G6 frame contract를 사용합니다. 기준 packet과 산출물 계보는 [G7 실행 계약](contract.md) 7.2에 있습니다.

## route 설계

`frame ID → I-PDU → signal group/signal → RTE port` 경로를 versioned config로 표현합니다. byte order, bit position, scale, unit, range, timeout, update condition, invalid value, last-valid policy를 한 source에서 생성합니다.

## 안내 실습

P00-B RX frame을 CanIf-like indication, PduR-like route, COM-like unpack/update, RTE-like read로 전달합니다. 각 경계의 input/output identity와 timestamp를 trace에 남깁니다. unknown ID, short DLC, stale counter는 애플리케이션 값을 바꾸지 않습니다.

선택 E2E profile의 counter, Data ID, CRC가 보호하는 오류를 작은 reference model로 시험합니다. E2E는 authenticity나 confidentiality를 제공하지 않는다는 보장 표를 함께 둡니다.

## 독립 실습

TX on-change 또는 periodic path를 반대 방향으로 구현합니다. generated route table 밖의 수동 route를 금지하고, signal update race가 한 I-PDU snapshot을 섞지 않게 합니다.

## 전이 과제

endian, update bit, repeated counter, unknown route가 바뀐 packet 묶음을 순서 없이 풉니다. packet bytes, COM 상태, RTE-visible value를 한 표에서 비교하고 처음 어긋난 경계를 찾습니다.

## 판정 기준

- Can Driver와 CanIf, PduR, COM, RTE 책임이 코드·trace에서 분리됨
- route와 signal layout이 versioned 설정 한 곳에서 생성됨
- malformed·stale·E2E-invalid input 뒤 last-valid 값이 유지됨
- RX와 TX path가 기준 packet을 byte 단위로 재현
- E2E의 탐지 범위와 빠진 authenticity/confidentiality가 명시됨
- 생성 결과 hash와 packet-to-port trace를 깨끗한 환경에서 재생
- 설정 밖 frame이 애플리케이션 callback에 도달하지 않음

## signal 경로 복구 순서

packet parser와 route 책임이 섞였으면 signal 하나의 RX path만 남깁니다. E2E 오류가 애플리케이션 update를 막는지 확인하고, 통과한 packet-to-port trace를 저장합니다.

그다음 TX, 마지막으로 signal group을 붙입니다. 각 단계는 이전 fixture를 재사용하지 않고 해당 경계의 새 오류를 넣습니다.
