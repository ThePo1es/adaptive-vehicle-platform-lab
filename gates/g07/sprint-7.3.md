# Sprint 7.3 — CanTp–PduR–DCM–provider 경계

추적 대상: `OUT-XCUT-G7`, `REQ-CP-DIAG-001`. `FATAL-G7.3-DIAG`은 transport/routing/provider/NRC 결과를 합치거나 DCM-like component가 DTC를 소유한 경우입니다.

## 시간과 기준 자료

24–30시간. [R25-11 자료 장부](source-ledger.md)의 CanTp, PduR, DCM 절과 G6 ISO-TP/UDS timer matrix를 사용합니다. G6 protocol 상태기를 유지하고 adapter와 route configuration으로 감쌉니다. 판정값은 [G7 실행 계약](contract.md) 7.3을 따릅니다.

## 오류 vocabulary

transport timeout, PduR route 없음, DCM policy rejection, provider unavailable, provider timeout, UDS NRC를 별도 result로 정의합니다. packet에 같은 NRC가 보이더라도 내부 원인과 audit event는 구별합니다.

## 안내 실습

CAN frame→CanTp-like PDU→PduR-like route→DCM-like dispatcher→typed provider의 read DID 경로를 만듭니다. buffer request·copy·completion callback 순서와 ownership을 trace로 확인합니다. DCM은 DTC record를 직접 소유하지 않습니다.

## 독립 실습

두 provider와 concurrent tester를 추가합니다. route, session, P2/P2*, provider deadline, response buffer limit을 static config로 생성하고, component restart 중 in-flight request 처리 정책을 시험합니다.

## 전이 과제

late transport completion, wrong route, provider timeout, ECU-originated NRC를 같은 client 증상으로 위장한 corpus를 풉니다. 책임 경계별 event로 원인을 좁힙니다.

## 판정 기준

- CanTp/PduR/DCM/provider의 buffer·timer·상태 책임자가 명확함
- G6 ISO-TP/UDS 기준 corpus를 adapter 뒤에서도 그대로 통과
- transport, routing, policy, provider, NRC 결과가 audit에서 구별됨
- route/session/service allowlist 밖 요청이 provider에 도달하지 않음
- restart·timeout 뒤 buffer와 request slot이 회수됨
- DCM이 DEM-like store를 직접 수정하는 경로가 없음

## 경계별 오류 장부

transport, route, policy, provider가 낸 오류를 한 행씩 따로 적습니다. 모두 같은 negative response로 바뀌면 adapter 변경을 되돌리고 provider 하나와 route 하나에서 boundary event를 다시 살립니다.

수정 확인에는 기존 timeout fixture를 쓰지 않습니다. 다른 만료 시점으로 재시험해 어느 경계가 응답을 결정했는지 남깁니다.
