# Sprint 6.1 — Classic CAN과 CAN FD frame contract

추적 대상: `OUT-XCUT-G6`, `REQ-CAN-002`, `REQ-CAN-005`, `REQ-CAN-006`. `FATAL-G6.1-FRAME`은 DLC code와 payload length 혼동 또는 malformed frame의 애플리케이션 상태 반영입니다.

## 시간과 기준 자료

22–28시간. Linux SocketCAN 문서, Zephyr CAN controller 문서, Bosch CAN FD specification, 선택 controller의 FDCAN 절을 읽습니다. ISO 11898 원문 접근 여부와 edition은 자료 명세에 표시합니다.

[G6 실행 계약](contract.md) 6.1과 [DLC 16-vector](../../fixtures/g06/can-fd-dlc-v1.csv)가 입력·판정·시간을 고정합니다.

## 먼저 바로잡을 숫자

CAN FD의 on-wire DLC는 4-bit code 0–15입니다. code 0–8은 payload 0–8 byte, 9–15는 각각 12, 16, 20, 24, 32, 48, 64 byte에 대응합니다. SocketCAN의 `canfd_frame.len` 0–64와 DLC code를 다른 값으로 취급합니다.

## 안내 실습

Classic base/extended frame, CAN FD frame, RTR, error frame를 읽는 classifier를 만듭니다. 16개 DLC code 기준 벡터와 모든 0–64 length 입력을 시험해 표현 가능한 length와 padding policy를 구분합니다. BRS는 data phase 전환, ESI는 송신 node의 error state와 연결해 해석합니다.

vcan에서 `can-utils`로 synthetic trace를 만들고 MTU, frame type, ID flags, payload length를 raw bytes와 대조합니다. vcan 결과에는 arbitration loss, ACK, error confinement, bus-off, bit timing 근거가 없다고 metadata에 적습니다.

## 독립 실습

P00-A 큐 앞에 capability validator를 둡니다. controller/transceiver가 지원하지 않는 FD, BRS, nominal/data bitrate 조합은 시작 전에 거부합니다. malformed frame은 마지막 유효 애플리케이션 값을 바꾸지 않고 quality counter만 갱신합니다.

## 전이 과제

전이 corpus에는 Classic/FD API object 혼용, DLC/len 불일치, error-passive ESI trace가 들어 있습니다. wire 상호 운용 문제와 userspace object validation 문제를 나눠 설명합니다.

## 판정 기준

- DLC code 16개와 payload length mapping이 기준표와 정확히 일치
- `len` 0–64, DLC, padded wire length가 code와 문서에서 구분됨
- Classic/FD MTU와 flag가 맞지 않는 object를 decode 전에 거부
- BRS와 ESI 의미를 단순 boolean feature처럼 왜곡하지 않음
- malformed input에서 last-valid 값과 counter 보존식이 성립
- vcan claim이 packet/API 범위를 넘지 않음

## 다시 쌓는 순서

DLC와 payload length가 한 변수에 섞였으면 signal decode를 잠시 뺍니다. 다음 순서를 건너뛰지 않습니다.

1. frame classifier와 16개 기준표
2. controller capability 확인
3. signal parser와 padding policy

각 단계는 앞 단계와 다른 fixture로 경계값을 다시 확인합니다.
