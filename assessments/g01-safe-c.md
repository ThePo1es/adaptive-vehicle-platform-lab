# G1 종합 평가 계약

이 평가는 “안전한 C로 데이터와 메모리 다루기(G1)”의 다섯 실습을 세 영역으로 표본화합니다. 공개 실습을 외운 결과가 아니라 새로운 입력에서 계약을 옮길 수 있는지 판정합니다.

## 동결 절차

평가자는 응시 전에 다음 값을 private manifest에 고정하고 SHA-256만 mastery review에 기록합니다.

- 평가 대상 전체 commit SHA
- compiler·version·flags·host와 Cortex-M target
- 세 과제 ID, 입력 schema version, seed, 예상 관찰값
- 제한 시간, 허용 문서, 인터넷·AI 사용 범위
- 독립 oracle commit과 fixture hash
- 필수 mutant와 치명적 실패 목록
- 평가자, 이해관계, 동결 시각과 timezone

공개 입력과 같은 값·seed·register 순서를 재사용하지 않습니다. 시험 뒤 문제나 oracle 결함이 발견되면 원본 결과를 `Invalid assessment`로 보존하고 새 manifest로 다시 시험합니다.

## 과제 A: 직렬화와 파서, 60분

새로운 12비트 signed/unsigned 배치와 최대 payload 12인 frame 형식을 제공합니다. 응시자는 byte order·bit numbering·CRC 범위·consumed 규칙을 먼저 표로 고정한 뒤 codec 또는 parser를 구현하거나 결함을 고칩니다.

통과 조건:

- signed 경계와 byte 경계 벡터 오차 0
- 모든 truncation에서 범위 밖 접근과 application output 변경 0
- 거부 뒤 정상 frame 복구
- length 선검사, CRC 범위, consumed off-by-one, 오류 뒤 write mutant 생존 0

## 과제 B: 제한된 저장소, 60분

공개 실습과 다른 논리 용량, 가득 참 정책, 연산 seed를 제공합니다. Queue 또는 pool의 불변 조건을 먼저 쓰고 구현·수리합니다.

통과 조건:

- 독립 reference model과 모든 결과·counter 일치
- full·empty·stale generation·double free 뒤 상태 일치
- 용량 0 compile-fail 계약 유지
- raw foreign pointer 관계 비교, 범위 밖 접근, 동적 할당 없음

## 과제 C: MMIO·ISR 경계, 60분

접근 등급과 부작용이 다른 register sequence 하나와 target assembly 일부를 제공합니다. 응시자는 잘못된 W1C update, timeout wrap 또는 publish/consume 순서 결함을 진단하고 고칩니다.

통과 조건:

- register 접근 순서·폭·값이 독립 event oracle과 일치
- ISR에 parser, allocation, unbounded wait 없음
- producer payload write와 release publish, acquire consume 순서 설명
- host, single-core ISR, C thread, multi-core, DMA 주장을 정확히 제한
- target atomic이 lock-free가 아니라면 ISR 사용을 거부하거나 다른 동기화 설계를 제시

## 채점

| 관찰 항목 | A | B | C | 합계 |
| --- | ---: | ---: | ---: | ---: |
| Correctness | 20 | 20 | 20 | 60 |
| Diagnosis | 5 | 5 | 5 | 15 |
| Design contract | 5 | 5 | 5 | 15 |
| Independence와 설명 | 3 | 3 | 4 | 10 |

총점 85점 이상, 세 과제 각각 24점 이상, 모든 치명적 실패 0이어야 통과합니다. Correctness와 Independence는 모두 `강한 통과`를 받아야 합니다.

## 치명적 실패

- sanitizer finding, data race 또는 다른 undefined behavior
- 거부된 입력이나 실패 operation 뒤 출력·상태 변경
- 외부 객체 pointer의 관계 비교·뺄셈을 소유권 판정에 사용
- `memcpy`가 wire endian도 해결한다고 주장
- W1C register에 read-modify-write 사용
- `volatile`을 원자성·happens-before·Device ordering 근거로 사용
- host 가짜 장치 결과를 Cortex-M, multi-core 또는 DMA 검증으로 표시

평가 통과는 G1의 전이 능력을 뜻합니다. 실제 target 측정과 외부 검토가 없으면 전체 챕터 상태는 `Provisional`을 넘지 않습니다.
