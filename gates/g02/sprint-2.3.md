# Sprint 2.3 — 동시성

## 시간과 기준 자료

24–30시간. C++ working draft의 [`[intro.races]`](https://eel.is/c++draft/intro.races), [`[atomics.order]`](https://eel.is/c++draft/atomics.order), [`[thread.mutex]`](https://eel.is/c++draft/thread.mutex), [`[thread.condition]`](https://eel.is/c++draft/thread.condition)를 읽습니다. TSan을 쓸 수 있는 host에서는 [Clang ThreadSanitizer](https://clang.llvm.org/docs/ThreadSanitizer.html) 설정을 고정합니다.

## 시작 fixture

두 producer와 한 consumer가 bounded queue를 공유합니다. Seed patch에는 다음 중 두 결함이 들어 있습니다.

- condition variable predicate 없이 wait
- publish 전에 ready flag 갱신
- shutdown flag의 data race
- queue full에서 lost wakeup

검토자는 seed와 결함 조합을 시험 전까지 공개하지 않습니다.

## 안내 실습

happens-before graph를 그리고 한 결함을 TSan 또는 deterministic scheduler로 재현합니다. lock, atomic, condition variable이 보호하는 상태를 표로 나눕니다.

## 독립 실습

정상, spurious wakeup, queue full, shutdown 중 producer 진입을 반복하는 test를 만듭니다. 고정 seed 100개와 CI에서 재생 가능한 실패 seed를 보관합니다.

## 전이 과제

처음 보는 logger 또는 telemetry pipeline의 race를 90분 안에 진단합니다. 첫 20분에는 코드를 바꾸지 않고 가설, 공유 상태, 관찰 계획을 적습니다.

## 판정 기준

- 주입한 결함의 실행 순서와 root cause를 설명
- TSan finding 0 또는 deterministic schedule 전체 통과
- shutdown이 정해진 시간 안에 끝나고 대기 thread가 남지 않음
- relaxed ordering을 썼다면 필요한 happens-before를 별도 근거로 설명

## 힌트

1. condition variable은 상태를 저장하지 않습니다. predicate가 상태를 가집니다.
2. atomic 변수 하나가 주변의 비원자 상태를 자동으로 보호하지 않습니다.
3. 재현이 드물면 scheduler hook을 wait, publish, pop 직전에 둡니다.

## 치명적 실패와 보충

data race를 “실제로 잘 안 난다”는 이유로 남기거나 sleep을 늘려 test를 통과시키면 실패입니다. 보충 과제는 한 producer와 한 consumer만 남긴 model checker용 상태 전이표를 만드는 것입니다.
