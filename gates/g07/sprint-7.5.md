# Sprint 7.5 — Mode, network, watchdog, SecOC 배치

추적 대상: `OUT-XCUT-G7`, `REQ-CP-MODE-001`, `REQ-CP-SEC-001`, `REQ-MCU-WDG-001`. `FATAL-G7.5-OWNER`는 mode/network/watchdog 책임 혼합이나 실사용 key 사용입니다.

## 시간과 기준 자료

26–32시간. [R25-11 자료 장부](source-ledger.md)의 EcuM, BswM, ComM, CanSM, CanNm, Wdg/WdgIf/WdgM, SecOC, CSM, CryptoIf 절을 읽습니다. 각 module의 상태 책임과 callback 방향을 책임 표에 적고 [mode·security 순열](../../fixtures/g07/mode-security-permutations-v1.json)을 oracle로 사용합니다.

## 여섯 책임을 나누기

EcuM-like startup/shutdown, BswM-like rule arbitration, ComM-like communication request, CanSM-like controller/bus-off 상태, CanNm-like network participation, WdgM-like supervised entity 판정을 별도 component로 둡니다. hardware Wdg와 WdgIf adapter도 WdgM에서 분리합니다.

## 안내 실습

power-on→startup→full communication→silent/no communication→shutdown 상태 model을 만들고 각 transition의 requester, 판단 주체, actuator를 표시합니다. bus-off, missing supervision checkpoint, diagnostic request가 동시에 들어오는 시험을 deterministic event queue로 실행합니다.

SecOC-like 보호가 필요한 PDU 하나를 threat model에서 고릅니다. freshness 책임 주체, authenticator input, key identifier, 검증 결과, failure policy를 배치하고 CryptoIf/CSM-like boundary를 모형으로 둡니다. 실제 배포 key나 차량 credential은 사용하지 않습니다.

## 독립 실습

startup 중 bus-off와 late network wakeup을 처리합니다. BswM rule conflict resolution과 상태 transition reason을 trace에 남기고 watchdog feed는 G4 health vote contract를 유지합니다. key unavailable·freshness rollback은 communication quality와 mode policy에 전달합니다.

## 전이 과제

simultaneous mode request, stale freshness, WdgM checkpoint loss를 동일한 event ordering으로 replay합니다. 최종 결정을 내린 owner와 actuator를 trace에서 짚습니다.

## 판정 기준

- EcuM/BswM/ComM/CanSM/CanNm state와 판단 책임이 분리됨
- Wdg, WdgIf, WdgM-like supervision 경계가 코드와 trace에서 보임
- bus-off와 mode request 동시성 결과가 deterministic model과 일치
- SecOC-like failure가 last-valid·quality·mode policy에 일관되게 전달됨
- key/freshness storage·restart 가정과 residual risk가 기록됨
- SecOC가 confidentiality를 보장한다는 claim이 없음
- 로컬 모형과 R25-11 mapping의 검증 수준이 분리됨

## mode 경로를 되살리는 순서

full/no communication 두 state만 두고 요청·판단·실행의 책임 주체를 trace에서 다시 확인합니다. 그다음 startup과 shutdown, bus-off, watchdog 경로를 하나씩 되붙입니다.

한 component가 세 책임을 모두 맡거나 watchdog callback이 mode를 직접 바꾸는 순간 그 변경은 되돌립니다. 다음 확인에는 다른 동시 event 순서를 사용합니다.
