# Curriculum Audit — 2026-08-19

## 현재 판정

- G8–G12의 Adaptive·MCU·보증·통합 경로 명세: **통과**
- 91개 Sprint 전체를 바로 실행할 수 있는 완성 과정: **통과 전**

90개 Lab Pack은 `Specified`, G10.1은 `Runnable` 상태입니다. G10.1에는 시작 커밋, 공개 입력과 코드의 SHA-256, 실행 명령, 기준 출력, CPU 사용 시간과 실제 경과 시간이 붙었습니다. 첫 학습 실행에서 원문 검토, 독립 과제, 실제 학습 시간을 기록합니다. G11B·G12도 시간·입력·실습·전이 과제·판정 기준까지 작성됐습니다.

## 이전 감사 항목 대조

| 항목 | 현재 상태 | 확인 위치 |
| --- | --- | --- |
| 차량 보안을 G10 뒤로 앞당김 | 해결 | G10.8 IAM, G11A UCM·패키지 보안 |
| Service Interface → Proxy/Skeleton → SOME/IP 순서 | 해결 | G9.2 → G9.3 → G9.4–9.6 |
| Proxy/Skeleton 실제 생성 실습 | 해결 | 로컬 IDL 생성기와 CommonAPI 비교를 G9.3에 명시 |
| G8 실시간 Linux·PREEMPT_RT 공백 | 해결 | G8.8–8.9 |
| PID 재사용·이탈 자식 정리 | 해결 | pidfd, cgroup v2, subreaper, double-fork 시험 |
| systemd·P01·P03·PHM 재시작 경합 | 해결 | [생명주기 소유권 표](lifecycle-ownership.md) |
| 저장된 운행 상태의 부팅 적용 | 해결 | 부팅은 `Startup`, 조건·버전·목록 재검증 |
| DoIP·UDS 결과 혼합 | 해결 | transport 거부, backend 실패, ECU NRC 분리 |
| G9 vCAN이 실제 bus-off를 증명하는 문제 | 해결 | P05-SIM과 P05-HW 요구사항 분리 |
| CAN source gap 판정 근거 | 해결 | rolling counter와 source boot/session ID 필수 |
| VM PTP 성능 주장 | 해결 | VM은 프로토콜 확인, drift 주장은 물리 노드나 합성 시계만 허용 |
| Manifest TOCTOU | 해결 | immutable rootfs 또는 descriptor 기반 경로와 교체 입력 모음 |
| 합성 pcap 정책과 CI 충돌 | 해결 | 공개 fixture 경로와 metadata 조건 추가 |
| Diagnostics·IAM 구현 공백 | 해결 | G10.7–10.8과 P03 구성요소 추가 |
| UCM이 단순 A/B updater로 끝나는 문제 | 해결 | G11.1–11.4에 package·cluster·전송·활성화·롤백 계약 추가 |
| CAN FD 판정 공백 | 해결 | DLC code 0–15와 payload length를 분리하고 BRS, ESI, 두 bit-rate 구간을 요구사항·16-vector oracle로 고정 |
| G4–G7 개별 과제·MCU 기준선 공백 | 해결 | 27개 Lab Pack, NUCLEO-G474RE/Zephyr 4.4.0 ADR, G4/Classic 요구사항 추가 |
| G4–G7 수치·시험 입력·계보 공백 | 해결 | Gate별 실행 계약, 8개 합성 입력, 31개 baselined 요구사항, 계산 oracle 독립 검사 추가 |
| Classic module 책임 합침 | 해결 | Can Driver/CanIf, Wdg/WdgIf/WdgM, ComM/CanSM/CanNm을 분리하고 E2E/SecOC 과제 배정 |
| CAN analog 계측 과장 | 해결 | controller·logic·analog lane 분리, scope·differential probe가 없으면 analog 판정을 `Unverified`로 제한 |
| Gate 입구 진단·보강 경로 | 해결 | [입구 진단과 8–16시간 보강 모듈](gate-entry-diagnostics.md) |
| 모든 Sprint가 같은 시간·종결문을 쓰는 문제 | 해결 | G8–G11 시간 범위 분화, 반복 종결 공식 제거 |
| 실제 Adaptive stack 경험 | 일부 해결 | CommonAPI 필수 비교와 Industrial Bridge 경로 추가; 실제 SDK/CAPI 과제는 접근성에 따라 미작성 |
| 외부 검토자 병목 | 일부 해결 | 자동 oracle·upstream 결함을 일반 Sprint에 사용하고 재현·도메인 검토 역할 분리 |
| 전체 91 Sprint 과제 명세 | 해결 | 90개 Specified, G10.1 한 개 Runnable |
| 시간 추정의 실측 보정 | 미해결 | G10.1 기계 재현은 기록됨; 학습 시간과 G8.6·G9.6·G11.4 pilot 기록 없음 |

## 공개 전에 반드시 남은 일

1. G8.6, G9.6, G11.4를 실제로 실행하고 G10.1의 학습 시간을 재서 시간 추정을 보정한다.
2. 실행이 검증된 과제를 `Runnable`로 올리고, 봉인 문제까지 검토한 과제를 `Assessment-ready`로 올린다.
3. G10 뒤 Industrial Bridge를 실행 가능한 과제로 만들고 CommonAPI·Yocto·DLT 결과를 남긴다. 공식 SDK나 CAPI에 접근하면 같은 계약 시험을 이식한다.
4. G0–G2 실제 시간과 네 pilot 결과로 전체 예상 시간을 다시 계산한다.

## 자동 검사 범위

`scripts/check_repo.sh`는 내부 링크, 요구사항 추적, Lab Pack 필수 절, 합성 입력의 계산 가능한 oracle, 민감 파일, 공개 합성 캡처 metadata를 검사합니다. 기술 정확성, 교육 효과, 표준 적합성은 이 스크립트 통과만으로 판정하지 않습니다.

현재 검사 결과:

- 내부 Markdown 링크 정상
- 요구사항 98개와 traceability 98개 일치; 설계·검증 계획을 연결한 92개 `Baselined`
- Specified Lab Pack 90개와 Runnable Lab Pack 1개 확인
- G5–G7·G11·G12 합성 입력 10개의 RTA·DLC·journal·mode/security·변경 영향·통합 oracle 재계산 통과
- G10.1 공개 입력의 양성 1개·음성 20개 재실행과 시작 파일·시험 입력·출력 해시 확인
- 자동 검사에서 잡히는 동일 문장 반복 0건
- `bash -n`과 `git diff --check` 통과
