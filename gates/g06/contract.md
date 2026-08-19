# G6 실행 계약

packet 입력은 모두 합성 자료입니다. ISO 원문을 읽지 못한 실행은 Linux·Zephyr 비교 결과까지만 판정하고 규격 적합성 상태는 `Provisional`로 둡니다.

## Active time과 별도 대기

| Sprint | Core | Gate 근거 | Stretch | Active 합계 | 별도 wall time |
| --- | ---: | ---: | ---: | ---: | --- |
| 6.1 | 15–18h | 7–8h | 0–2h | 22–28h | 입력 모음 재생 3회 |
| 6.2 | 20–22h | 8–10h | 0–2h | 28–34h | bench 준비·계측 대기 제외 |
| 6.3 | 16–20h | 8h | 0–2h | 24–30h | analyzer capture 별도 |
| 6.4 | 15–18h | 7–8h | 0–2h | 22–28h | fuzz wall time 별도 |
| 6.5 | 16–20h | 8h | 0–2h | 24–30h | timer matrix replay |
| 6.6 | 15–18h | 7–8h | 0–2h | 22–28h | tester 대기 제외 |
| 6.7 | 15–18h | 7–8h | 0–2h | 22–28h | flood run 1h 이하 |
| 6.8 | 20–22h | 8–10h | 0–2h | 28–34h | 시험 120분·review 제외 |

## 입력과 판정

| Sprint | 동결 입력 | 기대 결과·허용 범위 | 산출물 계보 |
| --- | --- | --- | --- |
| 6.1 | [DLC 16-vector](../../fixtures/g06/can-fd-dlc-v1.csv), Classic/FD/error object 입력 모음 | 16개 mapping 오차 0; Classic payload >8 B와 FD >64 B 거부; malformed input 뒤 애플리케이션 값 불변 | G1 serializer + G4 driver → CAN frame contract |
| 6.2 | [bench contract](bench-contract.md) CAN-BENCH-01–05 | 각 scenario의 controller/packet 판정 충족; analog 결과는 scope가 있을 때만 `Validated` | simulator와 독립된 physical 근거 묶음 |
| 6.3 | bench timing, [세 message RTA 입력](../../fixtures/g06/can-rta-three-message-v1.json) | frame bit 상한 75/95/135, 응답 상한 420/660/710 µs와 독립 계산 일치; clock·packet loss가 있는 실행은 무효 | G5 RTA 도구에 non-preemptive CAN model 추가 |
| 6.4 | [ISO-TP RX 입력 모음](../../fixtures/g06/isotp-rx-v1.yml), Linux ISO-TP 비교 run | 다섯 case 결과 일치; copy-before-check·allocation-before-capacity-check 0 | CAN frame → 크기가 정해진 transport PDU |
| 6.5 | BS `{0,1,8}`, STmin `{0x00,0x7F,0xF1,0xF9,0x80}`, timeout±1 tick, two-channel seed | 유효 구간에서는 설정 STmin보다 빠른 전송 0; reserved value는 고정 오류; stale generation write 0 | full-duplex transport와 virtual-time timer oracle |
| 6.6 | [UDS read 입력 모음](../../fixtures/g06/uds-read-v1.yml), tester 두 종류 | 네 response byte sequence 일치; blocked service의 provider call 0; P2/P2*/S3 경계 ±1 virtual tick | transport PDU → DCM-like dispatcher |
| 6.7 | DTC executable model, 1/10/100/1,000 req/s flood seed, 두 tester | unauthorized 상태 change 0; counter 보존식 성립; health deadline miss가 생기면 설정한 거부 정책 실행 | G7 DEM/DCM slice의 protocol oracle |
| 6.8 | P00-A tag, 모든 G6 시험 입력, 봉인 network fault | vcan·실장비 디렉터리 분리, P00-A regression 100% 통과, reviewer가 packet count 재계산 | `P00-B` tag → G7 adapter가 재사용 |

## 고정 파일

릴리스에는 시험 입력 SHA-256, controller/transceiver 표시, bit timing, packet log, controller 원시 counter, 분석 worksheet와 실행 기록을 넣습니다. 입력이나 timer edition이 바뀌면 pack version을 올리고 이전 결과를 그대로 보존합니다.
