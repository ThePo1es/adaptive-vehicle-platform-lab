# Sprint 9.3 — 코드 생성기와 Proxy/Skeleton 경계

## 시간과 기준 자료

28–40시간입니다. Sprint 9.2의 동결된 계약과 COVESA [CommonAPI Core Tools](https://github.com/COVESA/capicxx-core-tools), [Core Runtime](https://github.com/COVESA/capicxx-core-runtime)을 사용합니다. COVESA 도구는 서로 맞는 tag·commit 조합을 `toolchain-lock.yml`에 고정한 뒤 실행하며, 확인하지 않은 `latest` 조합은 기준선으로 쓰지 않습니다.

## 시작 파일

필수 경로는 작은 로컬 IDL과 결정적인 generator입니다. 입력은 method, 이벤트, field, type, error만 지원하고 transport 정보는 받지 않습니다. 비교 경로에서는 같은 계약을 Franca IDL로 옮겨 CommonAPI가 만든 Proxy·Stub 계열 산출물을 읽습니다. 두 결과를 `ara::com` 생성물로 부르지 않습니다.

## 안내 실습

generator가 `IVehicleStateProxy`, `IVehicleStateSkeleton`, data type, error type, mock transport를 만들게 합니다. Proxy는 호출과 구독 요청을 type-safe message로 바꾸고, Skeleton은 이를 구현 객체에 전달합니다. in-memory transport로 method 호출과 이벤트 구독을 실행해 wire protocol 없이 경계를 먼저 확인합니다.

## 독립 실습

같은 입력은 byte 단위로 같은 산출물을 내야 합니다. 생성 파일에는 원본 IDL hash와 generator version을 넣고 수정을 금지합니다. unknown type, duplicate member, cyclic type, reserved identifier, incompatible change를 입력 단계에서 거부합니다. hand-written adapter와 business logic은 생성 디렉터리 밖에 둡니다.

## 전이 과제

전이 IDL에는 method 하나가 추가되거나 이벤트 payload가 호환되지 않게 바뀌어 있습니다. IDL diff, 생성 diff, compile failure 또는 compatibility 판정, 수정할 application code를 차례로 보여 줍니다. 이어서 CommonAPI 산출물에서 같은 책임을 맡는 class와 callback을 찾아 비교표에 추가합니다.

## 판정 기준

- Proxy와 Skeleton을 실제 생성하고 in-memory 호출·이벤트 시험을 통과
- 생성 디렉터리를 지운 뒤 한 명령으로 동일한 tree hash를 재생성
- 생성 파일을 손으로 고친 흔적이 없고 CI가 dirty generated tree를 거부
- 잘못된 IDL corpus가 code emission 전에 명확한 위치와 이유로 거부됨
- application logic이 generator·transport type에 직접 의존하지 않음
- CommonAPI 생성 결과와 로컬 결과의 책임 차이를 source 위치로 설명
- Service Interface 변경이 생성 코드와 클라이언트·서비스 빌드에 미치는 영향을 시험

## 힌트

1. generator snapshot 테스트만 두면 잘못된 산출물도 그대로 승인될 수 있으므로 compile·behavior 테스트를 함께 둡니다.
2. Proxy는 서비스 구현을 모르고 Skeleton은 client의 업무 흐름을 알 필요가 없습니다.
3. callback 수명과 unsubscribe 경합을 generated API 계약에 포함합니다.
4. transport 주소나 SOME/IP ID가 로컬 IDL에 들어오면 경계가 무너진 것입니다.

## 생성 경계 위반

Proxy/Skeleton을 손으로 작성해 놓고 생성했다고 표시하거나, 생성 파일에 업무 로직을 넣거나, CommonAPI를 AUTOSAR `ara::com` 구현으로 소개하면 통과할 수 없습니다. 보강 범위는 method 하나와 이벤트 하나이며, 생성→compile→loopback 테스트를 깨끗한 디렉터리에서 다시 실행합니다.
