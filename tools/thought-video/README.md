# 생각은 어떻게 물질이 되는가 — 모션그래픽 영상

「잠깐! 진짜?」 앱의 **책과 함께 · 깊이 읽기**(물질 → 생명 → 신경계 → 해석 → 생각 → 행동 → 제도 → 환경의 순환)를 95초 모션그래픽으로 만든 것입니다.
완성본: `app/media/thought-to-matter.mp4` (가로 1920×1080) · `app/media/thought-to-matter-vertical.mp4` (세로 1080×1920, 9:16) — 30fps, 95초, 배경음악 포함(음성 내레이션 없음)

## 구성 (95초)
| 시간 | 장면 | 책·깊이 읽기 근거 |
|---|---|---|
| 0:00 | 제목 | — |
| 0:05 | ① 물질: 양자장 → 원자 → 분자(H₂O), 창발 | 물질이란 무엇인가 / 부분의 합이 아닌 것 |
| 0:19 | ② 생명과 신경계: 세포 → 신경세포(전기 신호) → 시냅스(화학 신호) → 신경망 → 뇌 | 물질에서 생명으로 / 신경계 / 전기적·화학적 작용 |
| 0:34 | ③ 경험이 생각이 되는 과정: 외부 자극 → 감각 → 기억·감정·욕구 → 해석 → 생각 (같은 비, 네 개의 현실) | 현실은 그대로 주어지는가 / 해석이라는 다리 |
| 0:47 | ④ 생각이 물질이 되는 길: 생각 → 행동 → 습관 → 집단의 행동 → 규범·제도 → 건물과 환경 | 생각이 현실을 만드는 방식 / 개인의 사고와 사회의 순환 |
| 1:09 | ⑤ 순환: 환경이 다시 사람의 경험과 생각을 만든다 | 사회 층위의 순환 |
| 1:18 | 한계와 열린 질문: 생각이 곧바로 물질을 움직이는 것은 아니다 / 주관적 경험은 어떻게 생기는가 | 아는 것과 아직 열린 질문 |
| 1:28 | 마무리: 잠깐! 진짜? — 순환의 어느 지점에서든 생각의 틈을 열 수 있다 | 책 20장 |

## 다시 만들기
```bash
cd tools/thought-video
npm install                       # 글꼴(Noto Sans KR, Gowun Batang) 설치
export NODE_PATH=$(npm root -g)   # 전역 playwright 사용
node render.js stills 10 30 50    # 지정한 초의 화면 미리보기 → frames/
node render.js video ../../app/media/thought-to-matter.mp4
node render.js video /tmp/vertical.mp4 --portrait   # 세로형(index-portrait.html)
python3 make-music.py music.wav   # 배경음악 합성 (numpy, scipy 필요)
ffmpeg -i vertical.mp4 -i music.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out.mp4
```
- 장면·문구는 `index.html` 안에서 수정합니다. 모든 화면은 시간 `t`만으로 그려져서 어느 시점이든 같은 화면이 나옵니다.
- 자막은 `CAPS` 배열(시작초, 끝초, 줄들), 장면 시간은 `SCENES`·각 `S1`~`S7` 함수에서 조절합니다.
- 필요: ffmpeg, Playwright(chromium).
