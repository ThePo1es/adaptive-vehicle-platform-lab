# AUTOSAR R25-11 로컬 원문

G10.1 학습자가 AUTOSAR 공식 배포 페이지에서 직접 받은 PDF를 두는 경로입니다. PDF는 저장소에 커밋하지 않습니다.

파일명과 공식 URL은 [`r25-11-document-lock.json`](../../labs/g10_1_release_map/r25-11-document-lock.json)에 고정돼 있습니다. 다운로드 뒤 `Adaptive Platform Specification Hashes`의 SHA-512와 PDF를 대조하고, 검토된 digest를 lock에 pin합니다. 제출 지도에는 로컬 파일의 SHA-256도 적습니다. 검사기는 release, URL, 파일명, 공식 SHA-512와 로컬 SHA-256을 함께 확인합니다.

현재 lock의 `official_sha512`는 비어 있습니다. 공식 hash 목록을 직접 확인한 사람이 별도 커밋으로 값을 채우고 검토받으면 제출 검사가 열립니다.
