# Sprint 2.1 — 수명과 소유권

## 시간과 기준 자료

24–30시간. C++ working draft의 [`[basic.life]`](https://eel.is/c++draft/basic.life), [`[class.temporary]`](https://eel.is/c++draft/class.temporary), [`[class.copy.ctor]`](https://eel.is/c++draft/class.copy.ctor)와 [Clang AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html)를 읽습니다. 사용한 draft 날짜와 compiler version을 source manifest에 적습니다.

## 시작 fixture

`MessageOwner`는 최대 256바이트를 소유하고 `MessageView`는 byte span과 sequence를 빌립니다. 제공된 결함은 다음 세 가지입니다.

- 임시 owner에서 꺼낸 view를 queue에 보관
- move 뒤 원래 객체의 view를 계속 사용
- container 재배치 뒤 이전 element 주소를 사용

## 안내 실습

owner, view, borrow 기간을 표로 적고 세 결함을 ASan으로 재현합니다. `MessageOwner`의 copy/move 정책과 moved-from 상태를 문서화한 뒤 test를 먼저 고칩니다.

## 독립 실습

다음 API를 직접 설계합니다.

```cpp
Result<MessageView, ViewError> view_payload(const MessageOwner& owner);
```

성공 값이 owner보다 오래 살지 않게 호출 구조를 바꾸고, 빈 payload·최대 payload·move·queue pop 경계를 시험합니다.

## 전이 과제

파일 mapping 또는 socket receive buffer를 감싼 새로운 RAII owner/view pair를 90분 안에 설계합니다. 자원 해제와 view 무효화 시점을 sequence diagram에 표시합니다.

## 판정 기준

- ASan에서 제공된 세 결함이 모두 재현되고 수정 뒤 사라짐
- copy, move, destruction, reallocation 뒤의 유효성을 test 이름으로 확인 가능
- public API에 owner, borrower, lifetime, thread 사용 조건이 적혀 있음
- 전이 과제에서 원래 class 이름이나 구조를 그대로 복사하지 않음

## 수명 점검

1. 주소가 같아 보인다는 관찰은 lifetime을 연장하지 않습니다.
2. view를 반환하기 전에 호출자가 owner를 어디에 보관하는지 그립니다.
3. move 뒤 허용할 연산을 작게 정하면 test가 쉬워집니다.

## 다시 시작할 지점

sanitizer를 꺼서 증상을 숨겼거나 성공 경로에 dangling view가 남았다면 값 복사 구현으로 돌아갑니다. 안전한 기준 구현을 먼저 통과시킨 뒤 owner/view 버전의 비용과 수명 조건을 비교합니다.
