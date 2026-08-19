# Sprint 6.6 — UDS session과 read service

추적 대상: `OUT-XCUT-G6`, `REQ-ECU-DIAG-001`–`REQ-ECU-DIAG-003`. `FATAL-G6.6-UDS`는 차단한 상태 변경 service가 실행되거나 오류 원인을 같은 결과로 숨긴 경우입니다.

## 시간과 기준 자료

22–28시간. 접근 가능한 ISO 14229-1 edition에서 message format, DiagnosticSessionControl, ReadDataByIdentifier, TesterPresent, P2/P2*, S3, NRC 절을 읽습니다. 사용한 tester와 second stack의 version도 고정합니다.

[UDS read 입력 모음](../../fixtures/g06/uds-read-v1.yml)의 네 byte sequence와 [G6 실행 계약](contract.md) 6.6을 oracle로 씁니다.

## 허용 범위

격리된 P00-B endpoint만 대상으로 합니다. `0x22` read DID와 필요한 session/tester-present 경로를 allowlist합니다. session change도 ECU state를 바꾸므로 완전 무상태 read라고 부르지 않습니다. reset, write, routine, download 서비스는 차단합니다.

## 안내 실습

DCM-like dispatcher가 request SID, length, session, security precondition, DID range를 순서대로 검사합니다. unsupported SID/DID, bad length, wrong session에 versioned NRC를 반환합니다. P2와 P2* 관찰 지점을 정하고 delayed provider에는 `0x78` 정책을 적용합니다.

S3 expiry와 TesterPresent가 session state를 어떻게 바꾸는지 virtual clock으로 시험합니다. provider의 timeout, transport failure, ECU가 만든 NRC를 서로 다른 result로 남깁니다.

## 독립 실습

새 read DID 하나를 typed provider interface로 추가합니다. unit, scaling, valid range, stale/unavailable 표현을 기준 응답과 연결합니다. provider가 느리거나 재시작해도 request table과 queue가 상한을 넘지 않습니다.

## 전이 과제

wrong session, delayed response, duplicate tester, unsupported subfunction을 각자 독립된 대화로 재생합니다. packet, session 상태, audit counter를 한 timeline에서 설명합니다.

## 판정 기준

- allowlist 밖의 상태 변경 service가 dispatcher를 통과하지 않음
- P2, P2*, S3의 시작·만료 지점이 timer test와 일치
- bad length·unsupported·wrong session이 정한 NRC로 구별됨
- provider failure, transport failure, ECU NRC를 합치지 않음
- DID encoding의 unit·range·endianness가 기준 벡터와 일치
- concurrent request와 provider wait에 hard limit이 있음
- 두 tester implementation으로 허용 서비스 상호 운용 확인

## dispatcher를 고치는 순서

1. default session과 read DID 하나만 남긴다.
2. session timer와 request timer의 시작·만료 event를 분리한다.
3. bad length, unsupported, wrong session이 서로 다른 NRC를 내는지 확인한다.
4. extended session을 새 fixture로 다시 붙인다.

provider failure와 transport failure는 마지막까지 별도 결과로 유지합니다.
