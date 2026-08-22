# Sprint 12.7 — DoIP에서 UDS provider까지

P05의 DoIP 경로와 P00-C의 read-only UDS endpoint를 P06에 연결합니다. 결과 분류는 [P06 통합 계약](contract.md)의 diagnostic 불변 조건을 따릅니다.

## 시간과 자료

24–30시간. routing activation·alive check 복습 4–6시간, gateway route 구현 6–8시간, 고장 입력 8시간, tester 교차 확인과 정리 6–8시간입니다. ISO 13400·ISO 14229는 합법적으로 접근한 판과 절을 장부에 기록하고, 공개 도구는 version과 commit을 고정합니다.

## 결과 모델

각 요청에 connection ID, DoIP source·target address, UDS service·DID, backend route, deadline을 붙입니다. 결과는 `TransportRejected`, `GatewayFailure`, `EcuNegativeResponse`, `PositiveResponse`로 나눠 wire response와 audit event를 정의합니다.

## 안내 실습

정상 routing activation 뒤 ReadDataByIdentifier 한 건을 MCU endpoint까지 전달합니다. request, gateway route, ISO-TP/CAN traffic, provider 호출, response를 trace ID로 묶습니다. 연결 종료와 alive timeout 때 남는 route와 pending request가 없는지 확인합니다.

잘못된 target address, backend timeout, ECU NRC 0x31, 정상 DID 네 사례를 실행해 결과 code family와 tester 표시가 유지되는지 봅니다.

## 독립 실습

두 번째 DID를 추가하고 권한이 다른 client profile을 만듭니다. malformed DoIP length, 중복 routing activation, 늦은 CAN response, service version mismatch, flood 입력을 주며 bounded queue와 audit rate limit을 측정합니다.

## 전이 과제

tester에는 timeout만 보이지만 gateway log에는 ECU NRC가 기록된 사례를 받습니다. 60분 안에 최초로 계약이 달라진 경계, 보존해야 할 원본 packet, 수정할 oracle을 찾아 재현합니다.

## 판정 기준

- transport 거부와 backend 실패가 wire, gateway API, audit에서 구분됨
- ECU NRC와 application provider 실패가 별도 결과로 유지됨
- trace ID로 tester request부터 MCU provider 결과까지 따라갈 수 있음
- alive timeout 뒤 route와 pending request가 제한 시간 안에 정리됨
- 권한 실패 시 backend provider 호출 횟수가 0임
- malformed·중복·late·version·flood 입력이 자동 회귀에 포함됨
- queue와 audit rate가 동결된 한계를 넘지 않음
- 독립 tester가 정상 응답과 ECU NRC를 같은 packet 자료로 확인함

## 경계를 다시 찾는 법

같은 timeout으로 뭉친 결과는 최초 변환 지점을 결함 위치로 잡습니다. packet capture, route log, provider counter의 상관 ID를 보완해 경계별 결과를 다시 대조합니다.
