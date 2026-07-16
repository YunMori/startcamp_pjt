# LocalHub 🍒

대전·충청권 연인 데이트 코스를 추천해주는 챗봇("러비")과 익명 리뷰 커뮤니티를 결합한 웹 서비스입니다.
설문(칩 선택) → 성향 기반 코스 3종 추천 → Kakao 지도로 동선 확인 → 지역/축제 정보 열람 및 익명 리뷰 작성까지, 모든 경험이 하나의 챗봇 대화 흐름 안에서 이루어집니다.

## 주요 기능

- **성향 설문 기반 코스 추천**: 이동수단(도보/차량), 축제 참여 여부, 5개 성향 문항(q1~q5)에 가중치 점수를 매겨 5종 코스(A~E) 중 상위 3개를 추천
- **AI 스토리텔링**: 추천된 코스에 대해 Gemini가 장소들을 엮은 다정한 소개 메시지를 생성 (API 키 미설정/할당량 초과 시 폴백 문구로 자동 대체)
- **자유 대화**: 코스 추천 외에도 챗봇과 자유롭게 대화 가능
- **코스 동선 시각화**: Kakao 지도 미니맵 + 코스별 방문 장소 목록(동선) 표시
- **지역/축제 정보 패널**: 사이드 패널에서 지역 소개, 축제 정보 열람
- **익명 리뷰 CRUD**: 코스별 리뷰 작성/조회/수정/삭제, 비밀번호 기반 권한 검증

## 기술 스택

**Frontend**
- Vue 3 (Composition API, `<script setup>`) + Vite
- axios, Kakao Maps JavaScript SDK
- composable 기반 상태 관리 (`stores/`)

**Backend**
- FastAPI + Uvicorn
- SQLAlchemy + SQLite (`festival.db`)
- Google Gemini API (`google-genai`) — 코스 스토리텔링 / 자유 채팅

**Infra**
- Docker Compose (nginx + FastAPI 2-container 구성)
- nginx: 정적 파일 서빙 + `/api`, `/chat`, `/courses`, `/reviews` 리버스 프록시, 외부 노출은 80 포트만
- AWS EC2 배포 (Elastic IP + Kakao 웹 플랫폼 도메인 등록)

## 아키텍처

[Browser]
   │  (80)
[nginx] ── 정적 파일 서빙 (front/dist)
   │  reverse proxy: /api, /chat, /courses, /reviews
   ▼
[FastAPI:8000] ── SQLAlchemy ── [SQLite: festival.db]
   │
   └── Gemini API (스토리텔링 / 자유 채팅)

## 폴더 구조

├─ backend/
│  ├─ app.py           # FastAPI 라우터 (추천/챗봇/축제/리뷰 CRUD)
│  ├─ recommend.py      # 성향 기반 코스 스코어링 + Gemini 연동
│  └─ db/               # festival.db, 데이터 import 스크립트
├─ front/
│  └─ src/
│     ├─ components/    # ChatHeader, CourseCards, KakaoMiniMap, panel/(SidePanel, ReviewBoard 등)
│     ├─ stores/         # useChatStore, usePanelStore, useReviewStore
│     ├─ services/       # chatApi, reviewApi (axios)
│     └─ data/courses.js
├─ data/, pre_result/   # 대전·충청권 관광지/축제/맛집 등 원본·전처리 데이터(JSON)
├─ docker/               # nginx.conf, backend-entrypoint.sh
└─ docker-compose.yml

## 실행 방법

### 로컬 개발
```bash
# Backend
pip install -r requirements.txt
uvicorn backend.app:app --reload --port 8000

# Frontend
cd front
npm install
npm run dev

환경변수 (.env)

┌───────────────────┬────────────────────────────────────────────────┐
│       변수        │                      설명                      │
├───────────────────┼────────────────────────────────────────────────┤
│ GEMINI_API_KEY    │ Gemini API 키 (미설정 시 폴백 응답으로 동작)   │
├───────────────────┼────────────────────────────────────────────────┤
│ VITE_KAKAO_JS_KEY │ Kakao Developers JavaScript 키 (지도 렌더링용) │
└───────────────────┴────────────────────────────────────────────────┘

Docker 배포

cp .env.example .env
# .env에 GEMINI_API_KEY, VITE_KAKAO_JS_KEY 입력
docker compose up -d --build
자세한 배포 절차는 DEPLOY.md 참고.

API 개요

┌────────────┬───────────────────────┬───────────────────────────────────────────────┐
│   Method   │         Path          │                     설명                      │
├────────────┼───────────────────────┼───────────────────────────────────────────────┤
│ POST       │ /api/recommend        │ 설문 답변 → 상위 3개 코스 추천                │
├────────────┼───────────────────────┼───────────────────────────────────────────────┤
│ POST       │ /api/chat             │ 코스 ID → AI 스토리텔링 메시지 + 지도 핀 좌표 │
├────────────┼───────────────────────┼───────────────────────────────────────────────┤
│ POST       │ /chat                 │ 자유 채팅                                     │
├────────────┼───────────────────────┼───────────────────────────────────────────────┤
│ GET        │ /api/festivals        │ 축제 목록 조회                                │
├────────────┼───────────────────────┼───────────────────────────────────────────────┤
│ GET/POST   │ /courses/{id}/reviews │ 코스 리뷰 조회/작성                           │
├────────────┼───────────────────────┼───────────────────────────────────────────────┤
│ PUT/DELETE │ /reviews/{id}         │ 리뷰 수정/삭제 (비밀번호 검증)                │
├────────────┼───────────────────────┼───────────────────────────────────────────────┤
│ POST       │ /reviews/{id}/verify  │ 리뷰 비밀번호 검증                            │
└────────────┴───────────────────────┴───────────────────────────────────────────────┘

팀 구성 및 담당

- Frontend / Backend-AI 연동 / 배포: Vue3 UI 전체, 백엔드-챗봇 API 연동, Docker 배포 구성
- AI 추천 로직: 성향 기반 코스 스코어링 알고리즘, Gemini 연동
- Backend: FastAPI 서버 골조, DB 스키마, 리뷰 CRUD API


```
## 나의 기여 (YunMori)

### Frontend 초기 구축
Vue 3(Composition API) + Vite 기반으로 프론트엔드 전체를 처음부터 설계·구현했습니다. 챗봇 UI(ChatHeader/ChatMessageList/ChatInput), 설문 칩 선택(ChipsMessage), 코스 추천 카드(CourseCard/CourseCards), Kakao 지도 미니맵(KakaoMiniMap), 사이드 패널(지역정보/리뷰 CRUD/비밀번호 검증) 등 30여 개 컴포넌트와 composable 기반 상태관리(useChatStore/usePanelStore/useReviewStore), axios 서비스 레이어(chatApi/reviewApi)를 구성했습니다. 백엔드가 없는 단계에서도 목(mock) 데이터로 전체 사용자 플로우가 동작하도록 설계해 프론트-백엔드 개발을 병렬로 진행할 수 있게 했습니다.

### Git 브랜치 전략 및 병합 관리
`master`/`dev`/`BE`/`front`/`lcy` 5개로 나뉜 팀 작업 브랜치를 통합하는 역할을 맡아, 수많은 브랜치 병합을 직접 수행했습니다. 백엔드 라우터, `requirements.txt`, `.gitignore`가 브랜치마다 다르게 바뀌면서 발생한 3-way merge 충돌을 여러 차례 해결했고, 병합이 꼬였을 때는 "폭탄해체중"이라는 커밋 메시지를 남길 정도로 얽힌 상태를 하나씩 풀어가며 정리했습니다.

다만 병합을 반복하는 과정에서 각 브랜치의 `.gitignore`가 서로 어긋나 있었고, 그 사이로 `front/node_modules`, 빌드 산출물(`dist`), `.env`(API 키 포함), `festival.db` 같은 파일들이 여러 커밋에 걸쳐 히스토리에 섞여 들어갔습니다. 뒤늦게 이를 추적 해제(`git rm --cached`)했지만, 이미 과거 커밋에 남아있는 비밀 키는 그것만으로 지워지지 않았습니다. 결국 원본 저장소는 시크릿이 포함된 상태로 남겨두고, 커밋 히스토리를 재작성해 시크릿을 제거한 별도 GitHub 미러 저장소를 새로 만드는 것으로 수습해야 했습니다. 여러 브랜치가 얽힌 협업에서는 `.gitignore`를 초반부터 브랜치 간에 통일해두지 않으면, 병합이 누적될수록 되돌리기 어려운 상태가 된다는 것을 직접 겪으며 배웠습니다.

### 리뷰 기능 프론트-백엔드 통합
프론트가 기대하는 응답 형태(`id/nickname/r`) 엔드 리뷰 CRUD와 프론트 리뷰컴포넌트(`ReviewBoard/ReviewForm/PasswordGate`)를 연결하고, 기존 DB에 `created_at` 컬럼이 없을 경우 자동
마이그레이션하는 로직을 추가해 팀원이 쌓아 스키마를 확장했습니다.

### 배포 환경 구성
nginx + FastAPI 2-container Docker Compose 구성을 설계했습니다. nginx가 정적 파일을 서빙하면서 `/api`,
`/chat`, `/courses`, `/reviews`만 백엔드로  외부에는 80 포트만 노출되게 했고, 리뷰데이터는 Docker volume으로 영속화했습니다. AWS EC2 배포 절차(Elastic IP, 보안그룹, 스왑 설정, Kakao 도메인
등록)를 `DEPLOY.md`로 문서화해 팀원 누구나 했습니다.

### 기타
- Kakao 지도 미니맵 렌더링 버그 수정
- 추천 코스 패널에 코스 동선(방문 장소 목록) 표시 기능 추가
- 지역 정보 패널에 이미지 연결
