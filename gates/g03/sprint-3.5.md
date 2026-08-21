# 실습 3-5 — 컴파일러 의심 동작을 줄이고 보고 여부 결정하기

> 상태: `Runnable` · [장 안내](README.md) · [실행 계약](contract.md)

## 시간과 기준 자료

24–30시간. [LLVM bug life cycle](https://llvm.org/docs/BugLifeCycle.html), [LLVM bug reporting guide](https://llvm.org/docs/HowToSubmitABug.html), 대상 프로젝트의 contribution guide와 code of conduct를 읽습니다. 이미 공개된 issue를 재현할 때는 issue URL과 확인한 commit을 기록합니다.

## 시작 조건

다음 후보 중 하나를 고릅니다.

- 고정된 compiler version에서 재현되는 공개 issue
- vehicle corpus에서 발견한 의심스러운 진단·최적화·backend 동작
- 최근 수정된 upstream regression을 이전 commit에서 재현

source UB, 잘못된 flags, target mismatch를 먼저 배제합니다. 실제 upstream 보고는 peer review를 받은 뒤 진행합니다.

## 안내 실습

공개된 known issue 하나를 지정된 version에서 재현하고 input을 줄입니다. 한 단계씩 code를 없애며 증상이 유지되는지 자동 script로 확인합니다.

## 독립 실습

새 후보를 triage합니다. expected behavior의 근거, 최초 재현 version, 최소 reproducer, exact command, actual output, target 정보를 한 묶음으로 만듭니다. 수정할 수 있으면 failing test를 먼저 작성합니다.

## 전이 과제

검토자가 reproducer의 type, optimization level, target 중 하나를 바꿉니다. 90분 안에 문제 범위가 frontend, optimizer, backend, assembler/linker, source contract 중 어디에 있는지 다시 좁힙니다.

## 판정 기준

- 새 환경에서 한 명이 명령 하나로 증상을 재현
- 최소 reproducer와 reduction log가 있음
- expected behavior가 언어·IR·ABI 문서 절에 연결됨
- issue를 제출하지 않아도 test-first 분석과 peer review가 완료됨
- upstream 의견을 받았다면 반영 여부와 이유를 기록

## 보고 전 확인

1. `creduce`, `llvm-reduce`를 쓰기 전에 증상을 판정하는 script를 만듭니다.
2. compiler crash, wrong code, missed optimization, poor diagnostic을 구분합니다.
3. 이미 보고된 문제인지 issue tracker를 검색합니다.

## 보고를 멈추는 조건

UB를 컴파일러 버그로 보고했거나 재현을 확인하기 전에 upstream issue를 열었다면 보고 절차를 멈춥니다. 알려진 regression 하나를 지정 commit에서 재현하고 기존 테스트가 판정하는 조건부터 읽습니다.
