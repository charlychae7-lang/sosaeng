# 마음온도

신노년층 자각·역할 회복 프로그램 웹앱 (단일 HTML, 서버 불필요).

- 주소(Pages 배포 후): `https://<계정>.github.io/sosaeng/maeumondo/`
- 음성 입력은 https(또는 localhost)에서 Chrome·Edge·Safari로 열어야 동작합니다.
- 외부 AI 연결: `index.html`에서 `window.MAEUM_CHAT_ENDPOINT = "https://.../chat"` 지정.
  서버는 `POST {system, messages}`를 받아 `{text}`를 돌려주면 됩니다. 미지정 시 기기 내 거울 모드 응답을 씁니다.
- 기록은 각자 브라우저(localStorage)에만 저장됩니다. 진행자 화면이 다른 기기의 참여자를 보려면
  서버(참여자 요약·위험신호 저장 API)가 필요합니다 — 다음 단계 과제.
