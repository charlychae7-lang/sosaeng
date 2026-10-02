# 마음온도 서버 연동 설계 (다음 단계)

## 목표
1. 참여자 기기와 진행자 기기가 다른 경우에도 요약·위험신호를 볼 수 있게 한다.
2. AI 대화를 서버에서 중계해 API 키를 브라우저에 두지 않는다.

## 원칙
- 대화 원문은 서버로 보내지 않는다. 서버에는 요약 지표만 저장한다 (현재 앱의 개인정보 안내와 동일).
- 위험신호 대응 시한(고위험 수 시간 / 중위험 24시간 / 저위험 48시간)은 서버에서 계산해 진행자에게 알린다.

## API (초안)
| 메서드 | 경로 | 용도 |
|---|---|---|
| POST | `/chat` | `{system, messages}` → `{text}` (AI 중계, 앱의 `MAEUM_CHAT_ENDPOINT`) |
| PUT | `/participants/:id/summary` | 마음 온도, 현재 강, 위험 수준·시각, 대화 횟수 |
| GET | `/participants` | 진행자용 전체 요약 (인증 필요) |
| POST | `/participants/:id/risk-log` | 진행자의 대응 기록 |
| PUT | `/participants/:id/legacy-notice` | 5축 활용 소식 |

## 저장 모델
`participants(id, name, joined_at)`, `summaries(participant_id, mood, mood_date, week, risk_level, risk_note, risk_at, chat_turns)`, `risk_logs(participant_id, date, summary, action, agency, plan)`, `legacy_notices(participant_id, message, read)`

## 인증
- 참여자: 진행자가 발급한 초대 코드(6자리) → 기기별 토큰. 이름만으로 구분하던 현재 방식 대체.
- 진행자: 계정 로그인. 참여자 요약 조회는 진행자 권한에서만 허용.

## 앱 쪽 변경 범위
`safeSet('summary:...')` 직후 `PUT /participants/:id/summary`를 비동기 호출(실패 시 로컬 유지 후 재시도), 진행자 화면은 `GET /participants`로 교체. 나머지 화면은 그대로.

## 구현 후보
Supabase(Postgres + Row Level Security + Edge Function으로 `/chat`) 또는 Cloudflare Workers + D1. 둘 다 무료 구간으로 시범 운영 가능.
