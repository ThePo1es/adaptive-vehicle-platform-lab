# G7 R25-11 자료 장부

AUTOSAR Classic release는 R25-11 하나만 사용합니다. 아래 document ID와 section title을 내려받은 PDF의 revision·page·requirement ID와 대조해 Sprint issue에 적습니다. 원문 접근이 없으면 해당 mapping 상태는 `Provisional`입니다.

| Sprint | R25-11 document ID | 확인할 section title |
| --- | --- | --- |
| 7.1 | `AUTOSAR_CP_SWS_OS`, `AUTOSAR_CP_SWS_RTE` | Task Management, Event Control, Resource Management; Runnable Entity, RTE Event, Sender-Receiver Communication |
| 7.2 | `AUTOSAR_CP_SWS_CANDriver`, `CANInterface`, `PDURouter`, `COM`, `E2ELibrary` | Controller/Transmit/Receive; PDU indication/trigger; routing path; signal packing/update/timeout; protect/check와 receiver 상태 |
| 7.3 | `AUTOSAR_CP_SWS_CANTransportLayer`, `PDURouter`, `DiagnosticCommunicationManager` | segmentation/reassembly·timer; routing; session·service processing·NRC |
| 7.4 | `AUTOSAR_CP_SWS_DiagnosticEventManager`, `NVRAMManager` | event/DTC status·debounce·event memory; block read/write·integrity·recovery |
| 7.5 | `AUTOSAR_CP_SWS_ECUStateManager`, `BSWModeManager`, `WatchdogDriver`, `WatchdogInterface`, `WatchdogManager`, `CommunicationManager`, `CANStateManager`, `CANNetworkManagement`, `SecureOnboardCommunication`, `CryptoServiceManager`, `CryptoInterface` | startup/shutdown/wakeup; mode rule arbitration; supervision; communication/controller/network 상태; freshness/authenticator; crypto job와 driver routing |
| 7.6 | 위 문서 전체와 R25-11 methodology/configuration 문서 | configuration input, generated artifact, responsibility mapping, variation point |

문서 이름만 보고 책임을 추정하지 않습니다. issue를 동결할 때 실제 PDF의 document revision, 읽은 page, 관련 `SWS_` requirement ID를 최소 하나씩 연결합니다.
