# Sprint 1.2 — 객체 표현, 정렬, aliasing

## 시간과 자료

24–30시간. N1570 6.2.6.1, 6.2.8, 6.5, 6.5.2.3, 6.7.2.1, 6.7.3, 7.24.2.1을 읽습니다.

## Fixture

다음 세 구현을 같은 corpus로 비교합니다.

1. `uint16_t *` cast 뒤 dereference
2. `memcpy`로 local integer에 복사
3. byte shift와 OR

입력 주소 offset은 0–7, payload length는 0–8, compiler는 GCC/Clang, profile은 `-O0/-O2`입니다.

## 안내 실습

`sizeof`, `_Alignof`, `offsetof`로 세 structure의 padding map을 출력합니다. Packed structure의 codegen과 target fault risk를 기록합니다.

## 독립 실습

host에서 통과하지만 Cortex-M target에서 정렬 fault 가능성이 있는 parser를 찾고 portable implementation으로 고칩니다.

## 전이 과제

Network byte order의 32-bit field와 3-byte field를 읽는 API를 설계합니다. Input lifetime과 output representation을 문서화합니다.

## 판정 기준

- implementation별 defined/undefined/implementation-defined 분류
- sanitizer가 잡는 경우와 놓치는 경우 기록
- compiler assembly와 target instruction alignment 요구 연결
- public API에 alignment와 lifetime 계약 표시

## 힌트

1. Character type access와 effective type 규칙을 분리해서 읽습니다.
2. `memcpy`가 최적화 뒤 실제 call로 남는지 assembly에서 확인합니다.
3. Packed는 layout 문제를 해결해도 access 문제를 남길 수 있습니다.

## 치명적 실패와 보충

x86 host 성공만으로 portable 판정을 내리면 실패입니다. 보충 과제는 unaligned offset matrix를 UBSan과 Cortex-M cross assembly로 다시 분석하는 것입니다.

