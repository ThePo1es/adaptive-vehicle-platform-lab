# Sprint 9.8 — DoIP 읽기 경로

## 시간과 기준 자료

26–32시간. [ISO 13400-2:2025 공식 페이지](https://www.iso.org/standard/13400-2)를 확인하고 합법적으로 접근 가능한 원문이 있으면 edition과 읽은 절을 기록합니다. 원문 접근이 없으면 protocol conformance 판정은 `Provisional`로 남깁니다. [python-doipclient](https://github.com/jacobschaer/python-doipclient)는 pinned commit의 tester 동작을 읽고 사용합니다.

## 시작 조건과 안전 범위

격리된 namespace 또는 lab ECU에서 vehicle identification, routing activation, alive check, diagnostic message의 최소 경로를 구성합니다. UDS는 `DiagnosticSessionControl`의 안전한 기본 session과 `ReadDataByIdentifier` 두 DID만 허용합니다. write, routine control, download, reset은 gateway allowlist에서 거부합니다. 이 Sprint의 network endpoint는 인증되지 않은 것으로 표시하며 logical address를 principal로 사용하지 않습니다.

## 안내 실습

tester와 gateway 사이의 discovery, TCP 연결, routing activation, UDS read, alive check를 capture합니다. DoIP generic header의 version, inverse version, payload type, payload length를 bounds-checking parser로 확인하고 logical address route를 표로 만듭니다.

## 독립 실습

잘린 header, 잘못된 inverse version, 과대 length, unknown logical address, activation timeout, backend UDS timeout을 corpus로 만듭니다. gateway는 connection과 route 상태를 분리해 기록하고 동시에 허용할 tester 수와 payload 상한을 적용합니다.

## 전이 과제

봉인 묶음에는 잘못된 route, timeout, malformed message 가운데 하나가 있습니다. tester 결과, gateway audit, packet capture를 시간순으로 맞춰 첫 거부 지점을 찾습니다. python-doipclient와의 성공만으로 ISO 적합성을 주장하지 않습니다.

## 판정 기준

- 정상 activation부터 DID response까지 packet과 상태 timeline이 일치
- malformed length 전체 corpus에서 crash·과대 allocation 0건
- 허용되지 않은 write/reset/download 요청이 backend에 전달되지 않음
- logical address, route, activation 상태, timeout 이유가 audit에 남음
- DoIP rejection, backend timeout, ECU UDS NRC가 다른 결과로 기록됨
- tester 구현의 대상 edition과 ISO 13400-2:2025 차이 가능성을 기록
- 원문 검토 범위에 따라 `Validated`와 `Provisional` 근거를 구분

## 안전 범위 확인

1. TCP connection 성립과 diagnostic routing 허가는 별도 단계입니다.
2. payload length를 확인한 뒤 buffer를 할당합니다.
3. packet에는 식별 정보가 들어갈 수 있으므로 공개 전 fixture 주소와 payload만 사용합니다.

## 즉시 중단할 조건

허가받지 않은 실차 네트워크에서 시험하거나 읽기 전용 범위를 넘는 요청을 전달하면 즉시 중단합니다. 공개 tester 결과만으로 규격 적합성을 판정한 경우에도 결과를 인정하지 않습니다. namespace 안에서 activation과 DID 읽기 하나만 다시 구현합니다.
