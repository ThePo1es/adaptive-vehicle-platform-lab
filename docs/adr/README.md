# Architecture Decision Records

설계와 도구 기준선을 바꿀 때 `NNNN-short-title.md`를 추가합니다.

```markdown
# ADR NNNN — 제목

- 상태: Proposed / Accepted / Superseded
- 날짜: YYYY-MM-DD
- 관련 Gate·요구사항:

## 배경

결정을 바꿀 만한 제약, 관찰, 표준·도구 버전을 적습니다.

## 검토한 선택지

각 선택지의 장점, 비용, 실패 조건을 비교합니다.

## 결정

선택한 범위와 적용 commit을 적습니다.

## 확인 방법

clean build, 계약 시험, 측정, 되돌리는 조건을 적습니다.
```

연간 표준·도구 갱신 ADR에는 이전 기준선, 현재 릴리스, 바뀐 책임·보안 항목, 기존 테스트 영향, 올릴지 유지할지를 함께 남깁니다.
