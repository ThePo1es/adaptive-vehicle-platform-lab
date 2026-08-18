# 20주 학습·구현 로드맵

기준 학습량은 주 8–12시간입니다. 일정이 밀리면 주차를 억지로 맞추지 말고, 각 주의 **통과 기준**을 충족한 뒤 다음 단계로 넘어갑니다.

## 운영 규칙

- 매주 시작: GitHub 이슈 1개 생성
- 매주 종료: 학습 노트 1개, 재현 가능한 실험 1개, 회고 1개
- 프로젝트 변경: 기능별 브랜치와 PR 사용
- 완료 판정: 설명이 아니라 코드·테스트·패킷·측정 로그로 증명
- 사양 기준: Adaptive Platform R25-11을 학습 기준선으로 사용하되, 적합 구현이라고 주장하지 않음

## Phase 1 — 기반: 구조와 프로세스 수명주기

| 주 | 핵심 질문 | 구현·기록 | 통과 기준 |
| ---: | --- | --- | --- |
| 1 | Classic과 Adaptive의 실행·통신 모델은 왜 다른가? | 구조 요약, FC 책임표, Process Supervisor 설계 | EM·SM·PHM·COM·PER·UCM의 경계를 자기 말로 설명 |
| 2 | POSIX 프로세스를 어떻게 안전하게 생성·종료하는가? | `posix_spawn`, signal, exit status 실험 | SIGTERM graceful shutdown과 timeout 후 강제 종료 재현 |
| 3 | 장애 복구 정책은 어떤 상태를 가져야 하는가? | restart limit, exponential backoff, structured log | crash loop를 제한하고 원인을 로그로 식별 |
| 4 | 테스트 가능한 Supervisor란 무엇인가? | Process Supervisor v1, GTest/CTest, ASan/UBSan | 정상·비정상 종료·timeout·재시작 테스트 자동 통과 |

### Phase 1 산출물

- `projects/01-process-supervisor/`
- 프로세스 상태 머신과 시퀀스 다이어그램
- sanitizer 실행 로그
- “Execution Management와 유사한 부분 / 생략한 부분” 매핑

## Phase 2 — 통신: SOME/IP와 서비스 발견

| 주 | 핵심 질문 | 구현·기록 | 통과 기준 |
| ---: | --- | --- | --- |
| 5 | TCP, UDP, multicast의 실패 특성은 무엇인가? | 2노드 echo/event 실험, Wireshark 캡처 | 손실·재연결·multicast interface 차이를 패킷으로 설명 |
| 6 | SOME/IP의 Service, Instance, Method, Event, Field는 어떻게 연결되는가? | 메시지 헤더 파서 또는 작은 request/response | 헤더와 request/response를 캡처에서 식별 |
| 7 | SD와 재발견은 장애 후 어떻게 동작하는가? | vsomeip 기반 Vehicle State Service v1 | 늦은 서버 시작, 종료·재시작, 재구독 자동 테스트 |

### Phase 2 산출물

- `projects/02-vehicle-state-service/`
- Service/Instance/Method/Event ID 표
- SOME/IP-SD 및 SOME/IP 패킷 증거
- discovery time, event latency, CPU 사용량 초벌 측정

## Phase 3 — 플랫폼: 실행·상태·헬스·영속성

| 주 | 핵심 질문 | 구현·기록 | 통과 기준 |
| ---: | --- | --- | --- |
| 8 | State Management와 Execution Management의 책임은 어떻게 나뉘는가? | 상태 모델, Function Group 단순화 설계 | 상태 결정과 프로세스 실행 책임이 코드 구조에서 분리됨 |
| 9 | Manifest로 실행 순서와 정책을 표현할 수 있는가? | YAML schema, DAG dependency resolution | 순환 의존성 거부, 위상 정렬, 상태별 실행 자동 테스트 |
| 10 | 프로세스의 건강 상태를 어떻게 판단하고 복구하는가? | heartbeat/deadline supervision, persistency | heartbeat 중단 → degraded/restart 및 재부팅 후 상태 복원 |

### Phase 3 산출물

- `projects/03-execution-manager/`
- Manifest schema와 예제
- Alive/Deadline/Logical supervision 중 구현 범위
- 상태 전환 및 복구 시퀀스

## Phase 4 — 차량 통합: CAN·UDS·DoIP

| 주 | 핵심 질문 | 구현·기록 | 통과 기준 |
| ---: | --- | --- | --- |
| 11 | CAN 프레임을 서비스 데이터로 안전하게 변환하는가? | vcan, replay, signal decoder | 입력 검증, queue 상한, drop counter 테스트 |
| 12 | ISO-TP·UDS·DoIP 계층은 어디서 분리해야 하는가? | UDS read-only 경로와 DoIP adapter | positive response, NRC, multi-frame를 캡처로 식별 |
| 13 | 게이트웨이가 정책과 장애를 어떻게 처리하는가? | CAN–SOME/IP/DoIP gateway v1 | timeout, flood, 허용되지 않은 SID를 격리·기록 |

### Phase 4 산출물

- CAN 신호/서비스 인터페이스 매핑
- UDS/DoIP 정상·오류 시퀀스
- 가상 ECU 또는 소유·허가된 벤치 ECU 재현 절차
- 캡처에서 민감 정보 제거한 증거

## Phase 5 — 보안 업데이트: 검증·활성화·복구

| 주 | 핵심 질문 | 구현·기록 | 통과 기준 |
| ---: | --- | --- | --- |
| 14 | 무엇을 어떤 순서로 검증해야 하는가? | manifest, payload hash, Ed25519/ECDSA 검증 | 변조된 manifest/payload/signature를 설치 전에 거부 |
| 15 | 새 버전 실패 시 원자적으로 되돌릴 수 있는가? | A/B slots, activation, health check | 새 서비스 시작 실패 → 이전 슬롯 자동 rollback |
| 16 | 전원 차단·구버전·재전송 공격을 견디는가? | transaction journal, version policy, audit | 상태별 강제 종료 후 복구 및 downgrade 거부 테스트 |

### Phase 5 산출물

- `projects/04-secure-update-manager/`
- 업데이트 상태 머신
- 정상·변조·구버전·부팅 실패·전원 차단 테스트
- 키 저장·버전 정책의 trust boundary 설명

## Phase 6 — 통합 포트폴리오

| 주 | 핵심 질문 | 구현·기록 | 통과 기준 |
| ---: | --- | --- | --- |
| 17 | 각 서비스가 하나의 운영 모델로 결합되는가? | 통합 빌드·설정·부팅 시퀀스 | 깨끗한 환경에서 문서만으로 재현 |
| 18 | 정상 경로 밖에서 살아남는가? | crash, network loss, CAN flood, log storm, update failure | 장애 주입 테스트가 기대 상태와 복구 시간을 검증 |
| 19 | 성능·보안·추적성을 수치로 보여주는가? | p50/p95/p99, CPU/RAM, threat model, traceability | 모든 핵심 요구사항이 코드와 테스트에 연결됨 |
| 20 | 채용 담당자가 5분 안에 가치를 이해하는가? | README 정리, 데모 영상, v1.0 release | 부팅 → 통신 → 장애 → 복구 → rollback 데모 완료 |

## 최종 완료 기준

- [ ] GCC와 Clang 빌드가 모두 통과한다.
- [ ] unit/integration/fault-injection 테스트가 CI에서 재현된다.
- [ ] ASan/UBSan 결과가 남아 있다. 동시성 코드가 있으면 TSan 범위도 명시한다.
- [ ] 요구사항, 구현 파일, 테스트 ID가 추적성 표로 연결된다.
- [ ] SOME/IP-SD, SOME/IP, DoIP/CAN 증거를 민감 정보 없이 제공한다.
- [ ] p50/p95/p99 latency, CPU, RSS, discovery/recovery time을 동일 환경에서 측정한다.
- [ ] 위협 모델에 자산, 공격자, trust boundary, abuse case, mitigation, residual risk가 있다.
- [ ] 미구현 범위와 AUTOSAR 적합성을 주장하지 않는 이유가 명확하다.
- [ ] 새 사용자가 README만 보고 데모를 재현할 수 있다.

