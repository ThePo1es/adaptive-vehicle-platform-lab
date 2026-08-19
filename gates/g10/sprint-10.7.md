# Sprint 10.7 — Adaptive Diagnostics 책임과 읽기 경로

## 시간과 기준 자료

26–36시간을 예상합니다. R25-11 `Diagnostics`, `Execution Management`, `Persistency` 문서와 Sprint 9.8의 DoIP 읽기 경로를 사용합니다. `standards-ledger.md`에는 문서 ID, revision, Diagnostic Manager·application·transport 책임을 확인한 section title을 기록합니다.

## 먼저 그릴 경계

DoIP 전송, 진단 요청 라우터, UDS 서비스 의미, 애플리케이션 데이터·DTC 제공자를 네 책임으로 나눕니다. DoIP 헤더 거부, 라우팅 권한 실패, backend timeout, ECU가 반환한 UDS NRC는 서로 다른 결과 형식으로 정의합니다. 하나의 `NRC translation` 필드에 합치지 않습니다.

## 안내 실습

로컬 Diagnostic Manager가 DID registry와 read-only 서비스 policy를 읽어 요청을 알맞은 provider로 보냅니다. provider가 unavailable이면 lifecycle 상태와 함께 명시적인 backend 결과를 반환합니다. `DiagnosticSessionControl` 기본 session과 두 개의 `ReadDataByIdentifier`만 연결하고, write·routine·download·reset은 router에서 차단합니다.

## 독립 실습

request ID, authenticated principal placeholder, 대상, 서비스, 프로세스 instance, policy version, UDS result를 한 audit chain에 넣습니다. concurrent tester 수, in-flight request, payload, provider timeout에 상한을 둡니다. provider 재시작과 Function Group State 변경 중 들어온 요청을 queue, reject, cancel 중 어떤 규칙으로 처리할지 고정합니다.

## 전이 과제

봉인 fixture에서는 DoIP NACK, gateway timeout, provider crash, ECU NRC 중 하나가 같은 tester 증상으로 보입니다. packet, router audit, provider log를 사용해 최초 실패 위치를 찾고 회귀 시험을 추가합니다. 새 DID 하나도 등록해 application 변경 범위를 확인합니다.

## 판정 기준

- transport, authorization, routing, UDS semantics, application data 책임이 코드와 trace에서 구분됨
- read-only allowlist 밖 요청이 provider나 CAN backend에 도달하지 않음
- DoIP 거부·backend 실패·UDS NRC가 다른 type과 metric으로 남음
- provider restart와 상태 변경 중에도 in-flight request 수가 상한을 지킴
- request부터 response까지 principal·policy·프로세스 instance를 포함한 audit chain을 재구성
- 로컬 구현과 R25-11 Diagnostics 사이의 `Mapped/Partial/Missing` 상태를 section 근거와 기록
- 비공개 경계 고장의 최초 실패 위치를 90분 안에 찾아 자동 시험으로 고정

## 힌트

1. tester가 본 timeout만으로 gateway와 ECU 중 어느 쪽이 실패했는지 알 수 없습니다.
2. UDS NRC는 ECU 또는 UDS endpoint의 protocol response입니다. 로컬 parser error는 별도 결과로 기록합니다.

## 진단 오류 분리 재확인

logical address를 인증된 사용자처럼 취급했거나, 허용되지 않은 요청이 backend에 전달됐거나, 서로 다른 실패를 한 숫자로 기록했다면 해당 경로를 다시 만듭니다. 보강 과제는 tester 한 명, DID 하나, provider 하나로 줄여 네 책임의 로그를 맞추는 것입니다.
