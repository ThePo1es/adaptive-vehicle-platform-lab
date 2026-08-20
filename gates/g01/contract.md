# G1 공통 계약: Safe C Components v1

이 문서는 “안전한 C로 데이터와 메모리 다루기(G1)”의 다섯 실습이 공유하는 실행 전제, API 경계, 고정 입력, 치명적 실패와 산출물 계보를 고정합니다.

## 지원 범위

### 호스트 기준 환경

- C17 hosted implementation
- `CHAR_BIT == 8`, `UINT8_MAX == 255`, `UINT16_MAX == 65535`
- `uint8_t`, `uint16_t`, `uint32_t`가 존재
- Clang 18 이상, `-Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Wshadow -Werror`
- AddressSanitizer와 UndefinedBehaviorSanitizer를 켠 공개 검사

위 조건은 컴파일 시 `_Static_assert`로 확인합니다. 조건을 만족하지 않는 구현은 잘못된 결과를 내는 대신 지원하지 않는 대상으로 분류합니다.

### Cortex-M 전이 환경

호스트 검사는 C 언어 계약과 결정적 로직을 확인합니다. 다음 성질은 NUCLEO-G474RE/STM32G474RE, Arm GNU Toolchain 또는 선택한 동등 환경에서 별도로 확인합니다.

- 실제 레지스터 폭·정렬·접근 부작용
- `UNALIGN_TRP` 설정과 메모리 영역별 비정렬 접근 결과
- ISR 호출 규약과 interrupt masking
- ISR에서 사용하는 원자 연산의 lock-free 명령열
- Device memory ordering, Arm barrier, DMA cache 일관성

호스트 가짜 장치 통과를 실제 MCU 동작이나 AUTOSAR 적합성으로 표현하지 않습니다.

## 다섯 실습의 계보

| 실습 | 입력 | 공개 API 결과 | 다음 실습에서 쓰는 것 |
| --- | --- | --- | --- |
| 1-1 | 8바이트 신호 벡터 | raw 신호 decode/encode | 1-4의 payload 의미 확인 |
| 1-2 | offset·길이·바이트 패턴 | 접근법별 C17 분류와 안전한 읽기 | 모든 wire access |
| 1-3 | 동결된 연산열·seed | queue·pool 상태와 counter | 1-5의 ISR→task 전달 |
| 1-4 | frame corpus·CRC 정답 | status·consumed·output | 1-5 task parser |
| 1-5 | register event sequence | access log·queue·timeout·counter | G4 target driver 전이 |

최종 공개 API는 `labs/g01_safe_c/include/g01_lab.h`에 고정합니다. 학습자 구현은 API를 바꾸지 않고 `study/g01/src`에 둡니다.

## 실습 1-1: wire 정수 계약

8바이트 payload의 한 byte는 8비트 octet입니다.

| 위치 | 의미 | 유효 범위 |
| --- | --- | --- |
| 0–1 | little-endian unsigned speed, 단위 0.01 km/h | raw 0–65535 |
| 2–3 | little-endian signed two's-complement temperature, 단위 0.1 °C | raw -400–2150 |
| 4 low nibble | rolling counter | 0–15 |
| 4 high nibble, 5–7 | reserved | 모두 0 |

signed 값은 signed shift나 범위 밖 signed cast로 만들지 않습니다. 먼저 unsigned raw를 만든 뒤 `raw >= 0x8000`이면 수학적으로 `raw - 0x10000`을 계산합니다. round trip은 부동소수점 표시값이 아니라 raw 정수에 적용합니다. 표시값을 비교할 때만 절대 오차 `0.005 km/h`, `0.05 °C`를 사용합니다.

## 실습 1-2: 세 접근법의 정답 분류

| 접근법 | C17 의미 | endian 결과 |
| --- | --- | --- |
| `uint16_t *` cast 뒤 역참조 | 정렬·effective type 위반 가능 | native endian 의존 |
| `memcpy`로 local `uint16_t`에 복사 | 길이가 맞으면 정렬·별칭에는 안전 | native endian 의존 |
| unsigned byte shift와 OR | 8비트 byte 전제에서 정의됨 | wire endian을 명시 가능 |

`memcpy`는 wire endian을 자동으로 해결하지 않습니다. packed structure는 compiler extension과 target 접근 정책을 별도로 기록합니다. padding을 포함한 structure 전체 `memcmp`를 값의 동일성 판정으로 사용하지 않습니다.

## 실습 1-3: 제한된 저장소 계약

Core queue의 논리 용량은 1 이상입니다. 용량 0은 `_Static_assert`가 거부해야 하는 compile-fail 입력입니다. `reject-new` 정책은 실패 뒤 상태를 보존하고, `overwrite-oldest` 정책은 가장 오래된 원소 하나만 버리며 counter를 증가시킵니다.

Pool은 raw foreign pointer의 범위 비교나 뺄셈으로 소유권을 판정하지 않습니다. 공개 구현은 `index + generation` handle을 사용합니다. 해제는 유효한 live handle에만 성공하고, double free·오래된 generation·범위 밖 index는 pool 상태를 바꾸지 않습니다.

## 실습 1-4: 프레임 파서 계약

```text
[0xA5 magic][0x01 version][length 0..16][payload][CRC-8/ATM]
```

- CRC 범위: magic부터 payload 마지막 byte까지
- CRC-8/ATM: polynomial `0x07`, init `0x00`, refin/refout false, xorout `0x00`
- 표준 확인 벡터: ASCII `123456789` → `0xF4`
- 반환값: `complete`, `need-more`, `rejected`와 `consumed` 길이
- full-buffer parser는 정확히 한 frame만 받고 trailing byte를 거부
- byte parser는 오류 byte까지 소비하고, 그 byte가 magic이면 새 frame의 시작으로 재사용
- `need-more`와 `rejected`는 application output을 바꾸지 않음
- 거부 뒤 첫 정상 frame은 이전 payload와 무관하게 정상 해석

공개 corpus는 길이 0–20의 모든 truncation, 잘못된 길이·CRC·version, 반복 magic, trailing byte를 포함합니다. 결정적 fuzz는 고정 seed와 최대 입력 64바이트, 100,000회로 실행하며 실행 사이에 parser 상태를 초기화합니다. 시간 기반 fuzz 기록은 별도 보강 근거로 남깁니다.

## 실습 1-5: MMIO·ISR·동시성 계약

### 가짜 레지스터

| 이름 | offset | 폭 | 접근 | reset | reserved mask | 부작용 |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| STATUS | 0x00 | 32비트 | RO | 0 | `~0x3` | 없음 |
| CONTROL | 0x04 | 32비트 | RW | 0 | `~0x3` | 단일 task writer |
| RX_DATA | 0x08 | 32비트 | RO | 0 | `~0xFF` | 읽으면 값 유지 |
| IRQ_ACK | 0x0C | 32비트 | W1C | 0 | `~0x1` | bit 0 literal write로 STATUS.RX_READY 해제 |

W1C에는 read-modify-write를 사용하지 않습니다. host oracle은 접근 순서·폭·값·횟수를 검사합니다. timeout은 32비트 단조 증가 tick의 modulo subtraction으로 계산하며 무한 polling을 금지합니다.

### 네 실행 모델을 분리함

| 모델 | 공개 실습에서 확인 | 추가 근거 |
| --- | --- | --- |
| 단일 core ISR→task | ISR producer, task consumer, release publish/acquire consume | target assembly, lock-free 확인 |
| C thread↔thread | C17 atomic과 happens-before | ThreadSanitizer 보강 |
| multi-core | 공개 host 실습 범위 밖 | cache coherence·architecture 문서 |
| DMA↔CPU | 공개 host 실습 범위 밖 | device barrier·cache maintenance·descriptor ownership |

payload는 producer가 먼저 쓰고 release로 index를 공개합니다. consumer는 acquire로 index를 읽은 뒤 payload를 읽습니다. queue index에 쓰는 atomic이 target에서 항상 lock-free인지 `ATOMIC_*_LOCK_FREE == 2` 또는 assembly로 증명하지 못하면 ISR 경로에 사용할 수 없습니다. `volatile`은 접근을 관찰 가능하게 만드는 구현 수단일 뿐 원자성, happens-before, Device ordering을 보장하지 않습니다.

## 고정 입력과 독립 판정

| 실습 | 공개 입력 | 독립 판정 |
| --- | --- | --- |
| 1-1 | `fixtures/g01/sprint-1.1-v1.h` | raw 수학식과 known-answer vectors |
| 1-2 | `fixtures/g01/sprint-1.2-v1.h` | C17 분류표와 native-endian probe |
| 1-3 | `fixtures/g01/sprint-1.3-v1.h` | 작은 reference model과 고정 PRNG seed |
| 1-4 | `fixtures/g01/sprint-1.4-v1.h` | 독립 CRC·full-parser oracle |
| 1-5 | `fixtures/g01/sprint-1.5-v1.h` | register event log와 상태 모델 |

공개 입력 A는 학습과 회귀 검사에 사용합니다. 재시험 입력 B는 같은 schema와 다른 seed·layout·정책을 사용합니다. 종합 평가는 저장소 밖에서 봉인한 manifest의 SHA-256만 기록합니다.

## 치명적 실패

다음 중 하나라도 있으면 합계와 관계없이 통과하지 못합니다.

- 범위 밖 접근, use-after-free, data race 또는 다른 undefined behavior
- 거부된 입력이나 실패한 operation이 application output·저장소 상태를 변경
- foreign pointer 비교처럼 판정 코드 자체가 undefined behavior에 의존
- `memcpy`가 wire endian까지 해결한다고 설명
- full/empty 정책 또는 parser consumed 규칙이 문서와 다름
- W1C register에 read-modify-write 사용
- `volatile`만으로 원자성·thread synchronization·device ordering을 주장
- host 결과를 Cortex-M·DMA·AUTOSAR 적합성 근거로 과장

## 시간 기록

각 실습은 `읽기 / 안내 실습 / 독립 구현 / 자동 시험 / 전이 과제 / 기록` 시간을 따로 남깁니다. 검사기 CPU 시간과 전체 경과 시간도 별도 기록합니다. 첫 사람 실행 전의 시간은 추정치이며, 두 명 이상의 실제 수행값이 생기면 중앙값과 범위를 갱신합니다.
