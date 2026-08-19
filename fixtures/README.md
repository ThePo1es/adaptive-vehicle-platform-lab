# 공개 학습 fixture

이 디렉터리의 입력은 실제 차량에서 추출하지 않은 합성 자료입니다. 각 파일은 생성 목적, 단위, 우선순위 규칙과 기대 결과를 파일 안에 적습니다. Lab Pack을 `Runnable`로 올릴 때는 파일 SHA-256과 생성·검토 commit을 release manifest에 기록합니다.

현재 fixture는 문서 검토용 v1입니다. 아직 구현체와 대조 실행하지 않았으므로 `Specified` 근거이며 `Verified` 근거로 사용할 수 없습니다.

| 파일 | 고정한 내용 |
| --- | --- |
| `g05/task-set-v1.yml` | release model, priority, jitter, blocking 자원, stack 예산, RTA 기대값 |
| `g06/can-fd-dlc-v1.csv` | CAN FD DLC 0–15와 payload length |
| `g06/can-rta-three-message-v1.json` | Classical CAN 세 message의 frame-time·fixed-priority RTA 손 계산 |
| `g06/isotp-rx-v1.yml` | ISO-TP 수신 정상·오류 입력 |
| `g06/uds-read-v1.yml` | read-only UDS 응답·거부 입력 |
| `g07/classic-config-v1.yml` | OS/RTE·통신·진단 생성 설정 |
| `g07/dtc-journal-reset-v1.json` | two-slot journal의 모든 write 경계 reset 결과 |
| `g07/mode-security-permutations-v1.json` | 동시 mode event 우선순위와 합성 freshness 입력 |
| `g10/release-map-cases-v1.json` | 책임 지도 검사기의 양성 1개와 단일 결함 음성 5개 |

`scripts/check_fixture_semantics.py`는 계산 가능한 기대값과 필수 필드를 독립 계산합니다. 이 검사는 구현 시험을 대신하지 않습니다.
