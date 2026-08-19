# Gate 입구 진단과 보강 모듈

새 Gate를 시작하기 전에 짧은 실기 시험을 치릅니다. 문서를 찾아보는 것은 허용하지만 완성된 풀이와 생성형 AI는 사용하지 않습니다. 명령 기록, 작성한 코드, 실패한 테스트를 그대로 보관합니다.

합격선은 전체 70%와 필수 항목 전부 통과입니다. 필수 항목에서 막히면 표의 보강 모듈만 수행하고 다른 입력으로 다시 시험합니다. 이 시간은 해당 Gate 예상 시간에 포함하지 않습니다.

| 진입 Gate | 60–90분 실기 | 필수 판정 | 막혔을 때 |
| --- | --- | --- | --- |
| G1 | 12-byte 패킷을 범위 검사하며 해석하고 경계 입력 6개를 만든다. | 잘린 입력에서 범위 밖 접근이 없고 오류 뒤 출력이 바뀌지 않는다. | B-C, 8시간 |
| G2 | 수명 결함이 든 C++ 코드 하나를 sanitizer로 고치고 소유권을 설명한다. | dangling view와 이중 해제가 사라지고 회귀 테스트가 남는다. | B-CPP, 12시간 |
| G3 | 작은 ELF에서 함수 주소, 호출 규약, section·segment 관계를 찾는다. | 대상 ABI와 build 정보를 기록하고 주소 계산을 재현한다. | B-TOOL, 12시간 |
| G4 | 데이터시트에서 reset vector와 주변장치 레지스터를 찾아 최소 초기화 순서를 쓴다. | reserved bit를 보존하고 clock·reset 의존성을 찾는다. | B-MCU, 12시간 |
| G5 | 주기 작업 세 개의 utilization과 최악 응답시간을 계산한다. | blocking과 release jitter를 빠뜨리지 않는다. | B-RT, 12시간 |
| G6 | CAN trace에서 arbitration ID, DLC, rolling counter 오류를 찾는다. | bit rate와 payload timing의 근거를 분리한다. | B-CAN, 12시간 |
| G7 | CAN 수신부터 application까지 책임 경계를 작은 호출 그래프로 그린다. | 통신·진단·저장 책임을 한 구성요소에 몰아넣지 않는다. | B-CLASSIC, 16시간 |
| G8 | 자식 프로세스를 실행·종료하고 core dump에서 고장 위치를 찾는다. | 종료 상태를 구분하고 남은 descendant를 확인한다. | B-LINUX, 16시간 |
| G9 | UDP 패킷 10개를 캡처하고 network byte order의 길이 필드를 해석한다. | 패킷 경계와 애플리케이션 메시지 경계를 구분한다. | B-NET, 12시간 |
| G10 | YAML 입력을 검증해 DAG를 만들고 cycle 하나를 거부한다. | 파싱, 의미 검사, 실행 계획이 분리되어 있다. | B-MODEL, 16시간 |
| G11A | 서명 대상 바이트와 경로 정규화 규칙을 정하고 중단 가능한 쓰기 절차를 그린다. | 서명 유효성과 설치 권한을 구분하고 복구 지점을 적는다. | B-UPDATE, 16시간 |
| G11B | 짧은 운행 시나리오에서 hazard 하나와 attack path 하나를 도출한다. | 원인, 영향, 대응 수단, 남은 가정을 나눠 쓴다. | B-ASSURE, 16시간 |
| G12 | P00–P04 중 두 시스템의 상태·버전 불일치 한 건을 분석한다. | 관찰 지점과 책임 구성요소를 찾고 회귀 시험을 제안한다. | 실패한 선행 Gate 재시험 |

## 보강 모듈

### B-C — 바이트와 C 실행 모델, 8시간

- 정수 폭, 정렬, endian, shift 규칙을 작은 예제로 확인한다.
- `memcpy` 기반 decoder 하나와 경계 입력 20개를 만든다.
- ASan·UBSan 결과와 컴파일러 경고를 읽고 수정 이유를 적는다.

### B-CPP — C++ 수명과 테스트 도구, 12시간

- 값, 참조, 포인터, view의 수명을 호출 그래프로 표시한다.
- RAII 소유자와 비소유 view를 각각 하나 구현한다.
- sanitizer에서 실패하는 회귀 입력을 먼저 고친 뒤 예외·move 경로를 추가한다.

### B-TOOL — ABI·ELF·디버거, 12시간

- 같은 함수를 `-O0/-O2`로 빌드해 호출 지점과 prologue를 비교한다.
- `readelf`, `objdump`, `nm`, `gdb` 결과를 한 주소표로 연결한다.
- build ID가 다른 심벌 파일을 거부하는 절차를 확인한다.

### B-MCU — 레지스터와 부팅, 12시간

- Cortex-M vector table, stack pointer, reset handler를 직접 연결한다.
- clock, reset, GPIO 한 경로를 reference manual에서 추적한다.
- QEMU 또는 보드에서 잘못된 초기화 한 건을 고쳐 부팅 기록을 남긴다.

### B-RT — 실시간 분석, 12시간

- 고정 우선순위 작업 집합의 utilization, blocking, response time을 계산한다.
- priority inversion 사례를 mutex protocol 적용 전후로 비교한다.
- 분석 상한과 측정 최댓값을 같은 단위로 정리한다.

### B-CAN — CAN·ISO-TP 기초, 12시간

- arbitration, stuffing, error state, CAN FD DLC 변환을 손으로 계산한다.
- SocketCAN에서 정상·중복·누락 frame을 재생한다.
- ISO-TP single/first/consecutive/flow-control frame을 trace에서 구분한다.

### B-CLASSIC — Classic 책임 지도, 16시간

- COM, PduR, CanIf, CanTp, DCM, DEM, NvM의 입력과 출력을 표로 만든다.
- 공개 AUTOSAR 문서의 절과 로컬 구성요소를 `Mapped/Partial/Missing`으로 표시한다.
- 수신 신호와 UDS read 한 경로를 작은 코드나 호출 trace로 재현한다.

### B-LINUX — Linux 프로세스와 진단, 16시간

- `fork/exec`, signal, wait status, process group, `/proc` 관계를 실습한다.
- core dump, `strace`, `perf stat`으로 crash·hang·CPU 포화를 구분한다.
- systemd unit 하나에 전용 사용자와 자원 상한을 적용한다.

### B-NET — 소켓과 패킷 분석, 12시간

- network namespace 두 개를 만들고 UDP/TCP·multicast를 각각 캡처한다.
- TCP partial read와 여러 메시지가 합쳐진 read를 처리한다.
- Wireshark 필터와 원본 `pcapng`에서 같은 결론을 다시 확인한다.

### B-MODEL — 검증·그래프·상태 모델, 16시간

- strict YAML parser 설정과 schema 오류 입력 10개를 만든다.
- 위상 정렬과 cycle 검출을 독립 oracle과 비교한다.
- 상태 전이표에서 허용·거부·동시 요청 규칙을 테스트로 옮긴다.

### B-UPDATE — 업데이트 보안과 영속성, 16시간

- canonical manifest와 서명 검증 입력 모음을 만든다.
- descriptor 기반 경로 확인과 staging 경계를 실습한다.
- 임시 파일, `fsync`, 원자적 rename 사이에서 프로세스를 종료해 복구 결과를 기록한다.

### B-ASSURE — Safety·Security 분석, 16시간

- item boundary와 operating scenario를 한 장으로 정리한다.
- hazard, threat scenario, safety/security requirement를 각각 두 개 도출한다.
- FMEA와 attack path가 같은 자원·복구 수단에 의존하는 지점을 찾는다.

## 기록 방법

`PROGRESS.md`에는 진단 날짜, 입력 ID, 점수, 필수 항목 결과, 수행한 보강 모듈, 재시험 commit을 남깁니다. 답안을 저장소에 공개할 때는 다음 진단에 쓸 입력과 분리합니다.
