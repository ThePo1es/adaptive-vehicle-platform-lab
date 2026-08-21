# 실습 2-1 — 원본이 파괴되어도 안전한 데이터 뷰 만들기

> - 준비 상태: `Runnable`
> - 시작 커밋: `af3b810a55b4a5444337472f15bd9fb1f5809c32`
> - 공개 입력 SHA-256: `66752ae713e02cb8b7427caad01e0e7be387015b55a69ffd86b9e99374a21b50`
> - 재시험 입력 SHA-256: `595e4c01846dd3f4a66c8ff50e90b510b95d9f8be1dfedcba09e3b5d34a61182`
> - 실행 기록: [G2.1 실행 명세 v2](../../evidence/runnable/g2.1/run-manifest-v2.json)

> 소속 챕터: [임베디드 C++로 안전한 런타임 만들기](README.md) · 관리 코드: G2.1

## 시간과 기준 자료

24–32시간을 기준으로 잡습니다. C++ draft의 [`[basic.life]`](https://eel.is/c++draft/basic.life), [`[class.temporary]`](https://eel.is/c++draft/class.temporary), [`[util.smartptr.shared]`](https://eel.is/c++draft/util.smartptr.shared)와 [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html)를 읽습니다.

| 활동 | 예상 시간 |
| --- | ---: |
| 객체 수명·이동·소유권 관리 방식 읽기 | 6–8시간 |
| 소유 관계도와 실패 재현 | 8–10시간 |
| 독립 구현과 A·B 검사 | 6–8시간 |
| 전이 과제와 기록 | 4–6시간 |

## 시작 파일과 결과물

- 시작 구현: `labs/g02_embedded_cpp/starter/lifetime.cpp`
- 공개 입력: `fixtures/g02/sprint-2.1-v1.hpp`
- 재시험 입력: `fixtures/g02/retest-2.1-v1.hpp`
- 공개 API: `labs/g02_embedded_cpp/include/g02_lifetime.hpp`

결과물은 1–256바이트를 직접 소유하는 `MessageOwner`와 원본 저장 공간의 수명을 함께 보장하는 `PayloadLease`입니다. 원본을 소유하지 않는 `span`만 큐에 저장하는 구현은 통과할 수 없습니다.

## 안내 실습

1. 임시 객체, 이동된 객체, `vector` 재배치, 큐에서 값을 꺼낸 뒤의 소유 관계를 그립니다.
2. 각 단계에서 원본을 소유하지 않는 `span`의 수명이 언제 끝나는지 ASan으로 재현합니다.
3. `shared_ptr`의 소유권 관리 정보와 `span`이 가리키는 저장 공간의 관계를 표로 정리합니다.
4. `MessageOwner`를 이동한 뒤에는 `MovedFrom`, `PayloadLease`를 이동한 뒤에는 두 객체 모두 유효하다는 정책을 검사 이름으로 남깁니다.
5. 공개 입력 A를 O0·O2에서 통과시킵니다.

## 독립 실습

기준 구현을 보지 않고 `lifetime.cpp`를 완성합니다. 빈 입력, 최대 길이, `MessageOwner` 이동, `vector` 재배치, 큐에서 꺼내기, `PayloadLease` 이동을 모두 확인합니다. 메모리 할당에 실패해도 예외를 API 밖으로 던지지 않고 `OwnerError::AllocationFailed`로 바꿔 반환합니다.

```bash
G02_TRUSTED_LOCAL_EXECUTION=1 G02_SUBMISSION_ROOT=study/g02/src G02_LAB_ID=G2.1 \
uv run --offline --python 3.12.13 \
  --with ziglang==0.15.2 --with pyelftools==0.32 \
  python -m labs.g02_embedded_cpp.run_harness
```

## 전이 과제

소켓 수신 버퍼나 메모리 맵 파일 중 하나를 골라 같은 수명 관리 방식을 적용해 봅니다. 여러 객체가 저장 공간을 함께 소유하면 해제가 늦어질 수 있고, 값을 복사하면 복사 비용이 생깁니다. 두 비용을 함께 적고, 기존 클래스 이름과 필드는 그대로 베끼지 않습니다.

## 판정 기준

- `MessageOwner`를 파괴한 뒤에도 `PayloadLease`가 원본 저장 공간의 수명을 유지
- 빈 입력과 257바이트 이상을 서로 다른 오류로 처리
- 이동된 `MessageOwner`와 `PayloadLease`의 정책이 검사와 문서에서 일치
- O0·O2, 입력 A·B, 결함 101·102 판정 통과
- 이 실습에서 힙을 허용한 이유와 2-2에서 힙 사용을 금지하는 구간을 구분

## 다시 시작할 지점

메모리·정의되지 않은 동작 검사기(sanitizer)가 오류를 내지 않았다는 이유로 원본을 소유하지 않는 `span`을 그대로 두면 안 됩니다. `MessageOwner`를 파괴하자마자 관찰용 `weak_ptr`이 만료되는 경우에도 수명 관리가 잘못된 것입니다. 먼저 바이트 한 개만 값으로 복사하는 가장 단순한 구현으로 돌아간 뒤, 소유권 관리 정보와 원본 저장 공간의 수명을 확인하고 최대 길이와 컨테이너 이동을 차례로 추가합니다.
