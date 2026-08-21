# 학습 단계별 실습 안내서

각 실습 파일은 시작 전에 동결합니다. 풀이를 시작한 뒤에는 입력, 독립 판정 기준, 허용 오차, 재시험 조건을 바꾸지 않습니다.

## 준비 상태

| 관리 코드 | 챕터 | 실습 안내서 | 상태 |
| --- | --- | --- | --- |
| G0 | 개발 환경과 검증 기준 준비하기 | [2개 실습](g00/) | Specified |
| G1 | 안전한 C로 데이터와 메모리 다루기 | [챕터 안내와 5개 실습](g01/README.md) | 5 Runnable (v7) |
| G2 | [임베디드 C++로 안전한 실행 기반 만들기](g02/README.md) | [4개 실습](g02/) | 4 Runnable (v3) |
| G3 | ARM 실행 구조와 컴파일 결과 읽기 | [5개 실습](g03/) | Specified |
| G4 | Cortex-M 보드 부팅과 인터럽트 구현하기 | [6개 실습](g04/) | Specified |
| G5 | RTOS 태스크와 실시간성 검증하기 | [7개 실습](g05/) | Specified |
| G6 | CAN 통신과 차량 진단 구현하기 | [8개 실습](g06/) | Specified |
| G7 | AUTOSAR Classic 구조로 ECU 기능 묶기 | [6개 실습](g07/) | Specified |
| G8 | 임베디드 Linux 이미지와 프로세스 운영하기 | [9개 실습](g08/) | Specified |
| G9 | 서비스 인터페이스와 SOME/IP 통신 구현하기 | [10개 실습](g09/) | Specified |
| G10 | AUTOSAR Adaptive 실행·상태·진단·권한 이해하기 | [10개 실습](g10/) | 9 Specified; [10.1](g10/sprint-10.1.md) Runnable |
| G11A | 안전한 업데이트와 UCM 구현하기 | [4개 실습](g11/) | Specified |
| G11B | MCU–Linux 안전·보안 근거 검토하기 | [3개 실습](g11/) | Specified |
| G12 | MCU–Linux 차량 플랫폼 최종 통합하기 | [12개 실습](g12/) | Specified |

현재 91개 중 81개가 `Specified`, G1의 5개 실습과 G2의 4개 실습, G10.1이 `Runnable`입니다. 상태 기준은 아래 표를 따르고, 실제 학습 진도는 [PROGRESS.md](../PROGRESS.md)에 기록합니다. G1과 G2의 시작점과 실행 기록은 각 챕터 안내에, G10.1의 실행 기록은 [실행 명세 v12](../evidence/runnable/g10.1/run-manifest-v12.json)에 있습니다.

| 상태 | 필요한 근거 |
| --- | --- |
| Outline | 주제, 선수 관계, 종료 결과가 학습 단계 실행 안내에 있음 |
| Specified | 기준 자료, 과제, 독립 판정 방식, 전이 과제, 재시험 조건이 문서화됨 |
| Runnable | 시작 커밋, 시험 입력·입력 모음 해시, 실행 명령, 기준 출력, CPU·경과 시간이 검증됨 |
| Assessment-ready | 봉인 과제와 독립 판정기를 검토자가 실행했고 평가 명세 해시가 있음 |

파일을 `Runnable`로 올릴 때는 시작 파일과 시험 입력이 들어 있는 커밋 SHA를 이 문서에 연결합니다. 빈 SHA나 아직 실행하지 않은 문서 내 입력은 `Specified` 상태로 둡니다. 학습 단계 공통 수치와 산출물 계보는 각 실습이 연결한 `contract.md`에 둘 수 있습니다.

학습 단계 코드는 기술 묶음을 찾기 위한 표기입니다. G3 다음에는 `G8 → G9 → G10 → G11A`로 Linux/Adaptive 축을 완성하고, 이어서 `G4–G7`의 MCU/Classic 축을 진행합니다. 두 축의 결과는 `G11B → G12`에서 보증과 종단 통합으로 합칩니다.

각 학습 단계에 들어가기 전에는 [입구 진단](../docs/gate-entry-diagnostics.md)을 먼저 수행합니다. 필수 항목에서 막힌 경우 전체 선행 과정을 반복하지 않고 해당 8–16시간 보강 모듈만 마친 뒤 다른 입력으로 재시험합니다.

## 파일에 필요한 항목

- 기준 자료의 판본·문서 ID·절 제목 또는 요구사항 ID
- 시작 파일과 시험 입력 모음
- 안내 실습, 독립 실습, 전이 과제
- 기대 출력, 불변 조건, 허용 오차
- 필요한 경우에만 단계별 힌트
- 재시험 조건과 채점 기준
- 핵심·단계 통과 증거·확장별 활동 시간과 빌드·지속 시험 경과 시간

학습 단계 공통 계약: [G4](g04/contract.md), [G5](g05/contract.md), [G6](g06/contract.md)·[실물 벤치](g06/bench-contract.md), [G7](g07/contract.md)·[R25-11 근거 대장](g07/source-ledger.md), [G11B](g11/assurance-contract.md), [G12](g12/contract.md).

평가용 비공개 고장은 이 디렉터리에 저장하지 않습니다. 시험 때 사용하는 실행 명세의 해시와 검증 날짜만 [숙련도 검토 기록](../docs/templates/mastery-review.md)에 적습니다.
