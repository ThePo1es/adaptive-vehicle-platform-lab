# Sprint 6.4 — ISO-TP receiver와 reassembly

추적 대상: `OUT-XCUT-G6`, `REQ-ECU-DIAG-002`, `REQ-CAN-002`. `FATAL-G6.4-ISOTP-RX`는 bounds check 전 copy나 malformed transfer 뒤 애플리케이션 상태 변경입니다.

## 시간과 기준 자료

22–28시간. 접근 가능한 ISO 15765-2 edition의 addressing·SF/FF/CF/FC와 Linux ISO-TP 문서를 읽습니다. Linux stack은 differential implementation으로 사용하며 normative conformance oracle로 표기하지 않습니다.

고정 byte 입력은 [ISO-TP RX 입력 모음](../../fixtures/g06/isotp-rx-v1.yml), 합격 결과와 시간은 [G6 실행 계약](contract.md) 6.4에 있습니다.

## 입력 모음 준비

normal/extended/mixed addressing 중 구현할 범위를 고정합니다. SF, FF, CF, FC 정상 vector와 truncated length, oversized FF, wrong sequence number, interleaved sender, unexpected frame, padding mismatch를 synthetic corpus에 넣습니다.

## 안내 실습

bounds check가 끝난 뒤에만 payload를 copy하는 receiver 상태기를 만듭니다. transfer identity, expected length, next sequence, deadline, received length를 한 owner가 관리합니다. error가 나면 애플리케이션 buffer를 공개하지 않고 이유 counter와 상태 transition을 남깁니다.

virtual clock과 frame adapter로 board 없이 모든 branch를 돌립니다. 같은 corpus를 Linux ISO-TP socket에도 보내 지원 범위 안의 결과를 비교하고 차이는 version·option과 함께 기록합니다.

## 독립 실습

CAN FD single/first frame 또는 두 번째 addressing mode 중 하나를 추가합니다. fixed-capacity buffer limit보다 큰 선언 길이는 할당 전에 거부합니다. simultaneous RX channel 수와 channel selection rule을 config로 제한합니다.

## 전이 과제

sequence wrap, duplicate CF, late CF, 새 sender 충돌을 seed별로 재생합니다. 기존 transfer와 새 request 중 어느 쪽을 보존하는지 policy와 trace로 답합니다.

## 판정 기준

- copy 전 length·addressing·상태 검사가 끝남
- sequence number modulo와 expected length가 기준 corpus와 일치
- malformed/truncated input 뒤 애플리케이션 상태가 이전 유효값을 유지
- transfer·buffer·timer owner가 하나로 정해짐
- channel count와 payload size에 hard limit이 있음
- Linux differential 결과와 ISO 원문 확인 범위를 구분
- fuzz/property run에서 out-of-bounds와 stale-buffer exposure가 없음

## 상태기 복구 메모

normal addressing, channel 하나, SF/FF/CF만으로 기준 corpus를 먼저 통과시킵니다. 그때의 상태 추적 기록을 기준선으로 저장합니다.

다른 addressing mode와 CAN FD는 별도 변경으로 추가합니다. 새 기능을 붙일 때마다 truncated frame과 sequence 오류를 다시 넣어 이전 유효 payload가 보존되는지 확인합니다.
