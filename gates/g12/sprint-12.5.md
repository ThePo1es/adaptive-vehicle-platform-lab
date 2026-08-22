# Sprint 12.5 — 두 노드 최소 통합 골격

목표는 동결한 P00–P05 구성요소가 한 번에 시작되어 VehicleState 한 값을 전달하는 최소 통합 경로입니다. [P06 통합 계약](contract.md)의 lifecycle과 증거 등급을 적용합니다.

## 시간과 준비물

24–30시간. image 조립 6–8시간, startup wiring 6시간, smoke suite 6–8시간, 새 배포와 정리 6–8시간입니다. `release-lock.yml`, 두 node의 clean image, CAN·Ethernet 연결도, 전원·serial 접근을 준비합니다.

## 안내 실습

Linux manager ready, gateway ready, MCU session observed, version accepted, VehicleState offered 순서를 하나의 run ID로 모읍니다. 각 단계는 readiness event와 timeout을 갖고 lifecycle coordinator가 다음 결정을 내립니다. 실패 시 마지막으로 확인된 단계와 owner를 출력합니다.

정상 시작, Linux 먼저 시작, MCU 먼저 시작, gateway 지연, 잘못된 version 다섯 smoke case를 만듭니다. 종료는 service withdraw, queue drain, process stop, 저장 상태 flush의 순서를 확인합니다.

## 독립 실습

빈 저장소와 새 image에서 두 node를 배포합니다. 한 개의 CAN signal이 VehicleState client까지 도착하도록 wiring하고 source session·counter·quality를 출력합니다. 같은 artifact를 세 번 재부팅해 startup event와 결과 hash의 안정성을 확인합니다.

## 전이 과제

hostname, network interface 이름, CAN bitrate가 다른 격리 환경을 받습니다. 코드 수정 없이 deployment configuration과 manifest만 바꿔 120분 안에 smoke suite를 실행합니다.

## 판정 기준

- release lock의 artifact·image·firmware hash와 실행 명령·원본 log·smoke 결과가 한 manifest에 묶임
- 다섯 startup case가 최초 실패 단계와 책임 주체를 정확히 냄
- 기준 시작 순서가 `Driving-ready`에 도달하고 종료 중 queue가 제한 시간 안에 비워짐
- 세 재부팅에서 새 MCU session을 관찰하고 이전 값을 폐기함
- 환경 차이가 configuration에만 반영되고 code commit은 유지됨

## 골격부터 다시 세울 조건

수동 순서와 sleep 의존은 setup 결함으로 등록합니다. readiness 이벤트, timeout, process 두 개의 최소 시작 절차를 고친 뒤 순서 교환 네 건을 다시 붙입니다.
