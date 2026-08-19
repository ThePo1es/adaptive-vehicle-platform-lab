# Sprint 10.8 — 인증 주체, 권한 정책, 감사 기록

## 시간과 기준 자료

24–34시간입니다. Linux [`unix(7)`](https://man7.org/linux/man-pages/man7/unix.7.html)의 `SO_PEERCRED`, OpenSSL의 [TLS 1.3 documentation](https://docs.openssl.org/3.0/man7/ssl/), R25-11에서 Identity and Access Management와 Cryptography가 맡는 책임을 읽습니다. Core 실습은 로컬 Unix socket credential을 사용하고, mTLS는 두 node 확장 실습으로 둡니다.

## 위협 모델

보호할 action은 diagnostic read, 상태 request, update staging입니다. 공격자는 다른 UID로 실행, logical address 위조, 오래된 credential 재사용, policy file 교체, audit 삭제를 시도할 수 있다고 둡니다. IP 주소, SOME/IP Client ID, DoIP logical address는 인증 주체로 인정하지 않습니다.

## 안내 실습

Policy Decision Point는 `principal, action, resource, context, policy_version`을 받아 allow 또는 deny와 rule ID를 반환합니다. Unix socket 연결에서는 kernel이 제공한 PID/UID/GID를 프로세스 instance와 연결합니다. Policy Enforcement Point는 action 직전에 결정을 확인하고, 업무 component는 UID 해석이나 policy parsing을 직접 하지 않습니다.

## 독립 실습

default-deny 정책, atomic policy reload, schema/version 검사, stale decision 방지를 구현합니다. audit에는 principal, action, resource, decision, rule ID, policy hash, 프로세스 instance, correlation ID를 남기되 secret과 credential 원문은 기록하지 않습니다. policy 파일은 immutable image 또는 descriptor 기반 검증 경로에서 읽습니다.

## 전이 과제

다른 UID의 client, 같은 PID처럼 보이는 stale session, 위조 logical address, rollback된 policy version, reload 중 request를 차례로 넣습니다. 이어서 두 node mTLS 경로를 선택했다면 certificate subject·SAN을 로컬 principal로 바꾸는 규칙과 폐기된 certificate 처리까지 시험합니다.

## 판정 기준

- 모든 보안 결정이 인증된 principal과 고정된 policy version을 가짐
- kernel credential과 application 제공 ID를 구분하고 위조 입력을 거부
- default-deny 상태에서 등록되지 않은 action·resource가 실행되지 않음
- policy reload 전후의 request가 어느 version으로 판정됐는지 재현 가능
- allow/deny 양쪽 audit이 남고 credential·key material은 로그에 없음
- policy parser의 duplicate key, unknown key, overflow, path swap corpus 통과
- G9 DoIP와 G10 Diagnostics가 같은 권한 API를 사용하되 transport ID를 principal로 승격하지 않음
- IAM·Crypto의 공식 책임과 로컬 Unix credential 실습의 한계를 mapping에 표시

## 실마리

- credential을 읽은 시점과 action을 수행한 시점 사이에 connection 또는 프로세스 instance가 바뀔 수 있습니다.
- audit 저장소가 가득 찼을 때 allow를 계속할지 중단할지 action별로 정해야 합니다.
- mTLS 확장을 하지 않았다면 network caller는 계속 `unauthenticated endpoint`로 표시합니다.

## 실패 시 줄일 범위

IP·logical address를 principal로 사용했거나, deny 결정을 기록하지 않았거나, policy reload가 실행 중인 결정을 소급해 바꾸면 재시험합니다. Unix socket client 두 개와 action 하나만 남겨 credential→decision→enforcement→audit 순서를 다시 확인합니다.
