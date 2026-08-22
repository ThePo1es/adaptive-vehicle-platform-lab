# G7 실행 계약

공통 입력은 [Classic 합성 설정](../../fixtures/g07/classic-config-v1.yml), P00-B 릴리스, [R25-11 자료 장부](source-ledger.md)입니다. 생성기는 로컬 교육 도구이며 결과 명칭은 `Classic concept-aligned prototype`으로 유지합니다.

## 시간 배분

| Sprint | Core | Gate 근거 | Stretch | Active 합계 | 별도 wall time |
| --- | ---: | ---: | ---: | ---: | --- |
| 7.1 | 15–18h | 7–8h | 0–2h | 22–28h | 문서 접근·review 대기 제외 |
| 7.2 | 18–21h | 8–9h | 0–2h | 26–32h | packet replay 별도 |
| 7.3 | 16–20h | 8h | 0–2h | 24–30h | tester run 별도 |
| 7.4 | 16–20h | 8h | 0–2h | 24–30h | reset campaign 별도 |
| 7.5 | 18–21h | 8–9h | 0–2h | 26–32h | model sweep 별도 |
| 7.6 | 15–18h | 7–8h | 0–2h | 22–28h | 시험 195분·review 제외 |

## 입력, oracle, 산출물

| Sprint | 시작점 | 기대 결과·허용 범위 | 산출물 진화 |
| --- | --- | --- | --- |
| 7.1 | P00-A task model, 설정 v1의 task/runnable/port | `CanRxTask`가 `UpdateVehicleSpeed`를 1회 activate; ISR/task/runnable 책임 중복 0; 예상 파일 3개를 매번 같은 bytes로 생성 | P00-A task에 RTE-like port/설정 추가 |
| 7.2 | P00-B frame contract, 설정 v1 frame 0x123 | payload `39 30 00 00 00 00 00 00`이 123.45 km/h로 한 번 update; short/unknown/stale input은 last-valid 유지 | CAN path → generated COM/RTE slice |
| 7.3 | G6 UDS 입력 모음, 설정 v1 diagnostic route | `22 12 34`이 지정 provider 한 번 호출; transport/routing/policy/provider/NRC 다섯 결과가 서로 다른 event code | G6 상태기를 유지하고 CanTp/PduR/DCM-like adapter 추가 |
| 7.4 | [DTC journal reset 입력](../../fixtures/g07/dtc-journal-reset-v1.json) | 실행 model과 DTC response 일치; commit 전 candidate 채택 0; 마지막 commit 또는 default 외 reboot 상태 0 | G6 memory-backed DTC 책임 → persistent DEM/NvM-like slice |
| 7.5 | [mode·security 순열](../../fixtures/g07/mode-security-permutations-v1.json) | event 순서가 달라도 우선순위가 같으면 최종 상태·이유 일치; 책임 없는 transition 0; stale freshness에서 애플리케이션 update 0 | G4 watchdog + G6 bus 상태 + 생성된 mode/security policy |
| 7.6 | canonical 설정, 세 slice, 봉인 책임 경계 고장 | 같은 input의 생성 결과가 byte 단위로 일치; 세 slice와 G4–G6 regression 통과; mapping review가 없으면 상태는 `Provisional` | `P00-C/P00-v1`; 수동 route table은 폐기 |

## Release dossier

canonical config와 hash, 생성 결과 hash, packet/call/상태 추적 기록, R25-11 page·requirement 장부, E2E/SecOC 보장 표, 새 host 실행 기록, 시험 manifest를 보관합니다. schema나 공식 mapping이 바뀌면 generator 결과와 기존 검토를 덮어쓰지 않고 pack version을 올립니다.
