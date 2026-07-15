# LocalHub Frontend

대전·충청권 연인 데이트 코스 추천 챗봇("러비" 🍒) + 익명 리뷰 커뮤니티의 프론트엔드입니다.
모든 핵심 경험이 챗봇 대화 안에서 진행됩니다: **설문(칩 선택) → 코스 3종 추천 카드(Kakao 미니 지도) → 사이드 패널(지역/축제 소개 + 리뷰 CRUD)**.

## 기술 스택

- Vue 3 (Composition API, `<script setup>`) + Vite
- axios (백엔드 연동용 서비스 레이어)
- Kakao Maps JavaScript SDK
- 상태 관리: composable 기반 스토어 (`src/stores/`)

## 실행 방법

```bash
npm install
npm run dev
```

### 환경변수 (`.env.local`)

| 변수 | 설명 |
|---|---|
| `VITE_KAKAO_JS_KEY` | [Kakao Developers](https://developers.kakao.com) → 앱 생성 → **JavaScript 키**. 플랫폼에 `http://localhost:5173` 등록 필요. 미설정 시 지도 자리에 플레이스홀더 표시 |
| `VITE_API_BASE_URL` | FastAPI 백엔드 주소 (기본 `http://localhost:8000`) |

## 백엔드(FastAPI) 연동 지점

지금은 백엔드 없이 **목 데이터**로 전체 플로우가 동작합니다. 백엔드가 준비되면 아래 두 파일의 `USE_MOCK`을 `false`로 바꾸면 됩니다.

| 파일 | 담당 기능 | 호출하는 API (프론트가 가정한 형태 — 명세 확정 시 조정) |
|---|---|---|
| `src/services/reviewApi.js` | 리뷰 CRUD | `GET/POST /courses/{id}/reviews`, `PUT/DELETE /reviews/{id}`, `POST /reviews/{id}/verify` (비밀번호 확인, 불일치 시 403) |
| `src/services/chatApi.js` | 자유 채팅(LLM 프록시) | `POST /chat` — body `{ messages: [{role, content}] }`, 응답 `{ reply }` |

- 리뷰 비밀번호 검증은 백엔드 책임입니다. 목 단계에서만 프론트에서 임시 비교합니다.
- 자유 채팅 LLM 호출(API 키 관리 포함)은 백엔드 `POST /chat` 프록시 담당입니다. 준비 전에는 고정 안내 응답을 보여줍니다.

## 폴더 구조

```
src/
├─ data/courses.js        # 설문 문항, 코스 3종(좌표 포함), 시드 리뷰
├─ services/              # http(axios) / reviewApi / chatApi — 백엔드 연동 지점
├─ stores/                # useChatStore(대화 플로우) / usePanelStore(패널 상태) / useReviewStore
├─ composables/useKakaoMap.js
└─ components/
   ├─ ChatHeader / ChatMessageList / ChatInput
   ├─ bubbles/            # Bot·User 말풍선, 타이핑 인디케이터
   ├─ ChipsMessage        # 설문 선택 칩
   ├─ CourseCards / CourseCard / KakaoMiniMap
   └─ panel/              # SidePanel(바텀시트), RegionInfo, ReviewBoard/Detail/Form, PasswordGate
```

## 목 리뷰 테스트용 비밀번호

시드 리뷰의 수정/삭제 비밀번호: `1234`, `0000`, `1111`, `2222` (`src/data/courses.js` 참고)
