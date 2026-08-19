# Sprint 9.1 — 차량 서비스용 Ethernet 기초

## 시간과 기준 자료

24–30시간. IETF의 [UDP RFC 768](https://www.rfc-editor.org/rfc/rfc768), [TCP RFC 9293](https://www.rfc-editor.org/rfc/rfc9293), [IPv4 multicast host extensions RFC 1112](https://www.rfc-editor.org/rfc/rfc1112), iproute2의 [`ip-link(8)`](https://man7.org/linux/man-pages/man8/ip-link.8.html), [`network_namespaces(7)`](https://man7.org/linux/man-pages/man7/network_namespaces.7.html)을 읽습니다.

## 시작 조건과 topology

Linux network namespace 세 개를 `ecu-a`, `ecu-b`, `observer`로 구성합니다. bridge 하나, VLAN 두 개, multicast group 하나를 사용합니다. namespace, interface, MAC, IP, VLAN ID, route를 표로 고정하고 setup/teardown script가 반복 실행되어도 같은 상태가 되게 만듭니다.

## 안내 실습

UDP unicast, UDP multicast, TCP stream을 차례로 주고받습니다. `tcpdump -i any -nn -e`로 Ethernet/VLAN/IP/transport header를 읽고 application message와 packet을 대응시킵니다. TCP에서는 application framing을 직접 넣고 partial read를 재현합니다.

## 독립 실습

sender 10/100/1,000Hz, payload 32/512/1,400 byte 조합을 실행합니다. socket buffer와 consumer pause를 바꾸며 delivered, application drop, kernel drop, reconnect time을 raw CSV로 남깁니다. MTU를 넘는 payload는 fragmentation 또는 송신 실패가 어떻게 나타나는지 확인합니다.

## 전이 과제

검토자가 route, VLAN membership, multicast join interface, MTU 중 하나를 깨뜨립니다. packet이 사라진 첫 경계를 namespace별 capture와 `ip -details` 출력으로 찾고 복구 test를 추가합니다.

## 판정 기준

- topology를 빈 host/VM에서 한 명령으로 생성하고 완전히 정리
- VLAN tag, multicast destination, TCP sequence/ack를 capture에서 설명
- route fault와 application fault를 서로 다른 관찰 근거로 구분
- 송신, wire 관찰, 수신, application 처리 count의 차이를 계산
- overload에서도 queue와 memory가 정한 상한을 지킴
- capture filter와 해석 절차를 README에 기록

## 힌트

1. `ping` 성공만으로 multicast membership과 application port를 확인할 수 없습니다.
2. loopback, bridge, veth 중 어디서 capture했는지 항상 표시합니다.
3. TCP 한 번의 `send`와 상대의 한 번의 `recv`는 대응되지 않을 수 있습니다.

## 치명적 실패와 보충

host의 실제 network 설정을 깨뜨리거나, packet capture 없이 원인을 추측하거나, TCP를 message transport처럼 parsing하면 실패입니다. 보충 과제는 namespace 두 개와 UDP/TCP 한 경로만 다시 만들고 packet-to-message 표를 작성하는 것입니다.
