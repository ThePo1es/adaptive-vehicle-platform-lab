# 공개 학습 fixture

이 디렉터리의 입력은 실제 차량에서 추출하지 않은 합성 자료입니다. 각 파일은 생성 목적, 단위, 우선순위 규칙과 기대 결과를 파일 안에 적습니다. Lab Pack을 `Runnable`로 올릴 때는 파일 SHA-256과 생성·검토 commit을 release manifest에 기록합니다.

G5–G7 입력은 개별 실습의 계산 기준이고, G10 책임 지도 입력은 공개 검사기와 대조 실행해 `Runnable` 근거로 묶었습니다. G11·G12 입력은 변경 영향과 통합 결정을 고정합니다. 학습 결과를 `Verified`로 올릴 때는 별도 실행 기록을 붙입니다.

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
| `g10/release-map-cases-v1.json` | 책임 지도 검사기의 양성 1개와 구조·주장·review 결함 음성 17개 |
| `g10/review-manifest-v1.json` | reviewer·node·citation·근거 hash 결속을 확인하는 합성 review |
| `g11/assurance-change-v1.json` | 운행 조건·공통 시계·trust root 변경의 보증 영향 |
| `g12/integration-contract-v1.json` | 20 ms 예산, version·lifecycle 결정, F01–F12 고장 목록 |

`scripts/check_fixture_semantics.py`는 G5–G7의 계산값, G11 변경 영향, G12 예산·version·lifecycle oracle을 독립 계산합니다. G10 입력은 `labs/g10_1_release_map/run_harness.py`가 결함별 오류 코드를 확인합니다.
