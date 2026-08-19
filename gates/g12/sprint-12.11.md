# Sprint 12.11 — 새 환경에서 릴리스 재현

개발에 참여하지 않은 사람이 P06 release candidate를 새 host 또는 새 board에서 실행합니다. EXT 증거의 범위는 [P06 통합 계약](contract.md)에 따릅니다.

## 시간과 역할

20–24시간. 작성자의 release 정리 5–6시간, 재현 담당자의 설치·실행 8–10시간, 질문 기록과 수정 4시간, 두 번째 실행 3–4시간입니다. 작성자는 실행 중 조작을 대신하지 않고 issue와 문서 변경으로 답합니다.

## 전달물

release tag, source·submodule SHA, toolchain container 또는 lock file, firmware·image·SBOM hash, 장비 연결도, flash·boot·test 명령, 예상 출력, cleanup 절차를 하나의 manifest에 묶습니다. 비밀값은 환경 변수 이름과 발급 절차만 기록합니다.

## 안내 실습

먼저 깨끗한 VM에서 SIM smoke suite와 F06 service crash를 재현합니다. 명령마다 expected exit와 핵심 출력 marker를 두고, 문서에 없는 수동 단계를 담당자가 그대로 기록합니다. 작성자는 그 기록을 setup check 또는 README로 바꿉니다.

## 독립 실습

재현 담당자가 HW lane을 설치해 정상 VehicleState, 진단 읽기, dual fault 또는 power interruption 중 장비에 맞는 한 건을 실행합니다. 환경 정보, 걸린 시간, 질문, 실패 지점, 원본 자료 hash를 review manifest에 남깁니다.

## 전이 과제

새 환경의 Linux distribution 또는 board revision이 달라집니다. 두 시간 안에 지원 범위, 필요한 configuration, 막힌 hardware claim을 분류하고 SIM 또는 HW에서 가능한 가장 높은 증거를 다시 냅니다.

## 판정 기준

- 새 환경이 release tag와 hash만으로 같은 source를 가져옴
- setup check가 toolchain·권한·network·장비 연결 오류를 초기에 찾음
- 재현 담당자가 작성자의 키보드 조작 없이 smoke suite를 끝냄
- 문서 밖 단계와 질문이 issue 및 수정 commit에 남음
- 두 번째 실행에서 첫 실행의 문서 결함이 재발하지 않음
- EXT manifest가 SIM·HW 결과를 인용하고 새 근거 범위를 밝힘
- 비밀값·실차 data·개인 경로가 공개 artifact에 없음

## 재현을 이어 가는 기준

작성자의 실시간 설명이 없으면 다음 단계로 갈 수 없는 순간을 실패 지점으로 기록합니다. 그 단계만 최소 fixture로 다시 만들고 문서와 setup check를 고친 뒤 같은 담당자가 처음부터 재시험합니다.
