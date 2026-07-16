# LocalHub EC2 + Docker 배포 가이드

## 구성

- **frontend** 컨테이너: nginx — `front/dist` 정적 서빙 + API 리버스 프록시 (`/api/`, `/chat`, `/courses/`, `/reviews/` → backend:8000). 외부 노출은 80 포트만.
- **backend** 컨테이너: FastAPI + uvicorn (:8000, 내부망 전용). 첫 기동 시 `festival.db` 자동 생성·시딩, 리뷰 데이터는 `dbdata` 볼륨에 영속화.

## EC2 준비

1. **인스턴스**: Ubuntu 24.04, t3.small(2GB) 권장. t2/t3.micro(1GB)라면 스왑 필수:
   ```bash
   sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile
   ```
2. **Elastic IP** 할당·연결 (인스턴스 재시작 시 IP 유지 — Kakao 도메인 등록과 연동됨)
3. **보안 그룹**: 22(내 IP만), 80(0.0.0.0/0). **8000은 열지 않음**
4. **Docker 설치**:
   ```bash
   sudo apt update && sudo apt install -y docker.io docker-compose-v2 git
   sudo usermod -aG docker ubuntu   # 이후 재로그인
   ```

## 배포

```bash
git clone https://lab.ssafy.com/lcho3049/startcamp_pjt.git
cd startcamp_pjt
cp .env.example .env
nano .env        # GEMINI_API_KEY, VITE_KAKAO_JS_KEY 실제 값 입력
docker compose up -d --build
```

**Kakao 개발자 콘솔**에서 JS 키의 웹 플랫폼 사이트 도메인에 `http://<Elastic IP>` 등록 필수 (미등록 시 지도가 로드되지 않음).

## 배포 확인

```bash
docker compose ps                              # 두 컨테이너 모두 Up
curl -sI localhost/ | head -1                  # HTTP 200
curl -s localhost/api/festivals | head -c 100  # count > 0
curl -s localhost/healthz                      # 백엔드 헬스체크
curl -s -X POST localhost/chat -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"안녕"}]}'   # 실제 응답이면 Gemini 키 정상
```

브라우저에서 `http://<Elastic IP>` 접속 → 지도 렌더링, 설문→추천→리뷰 플로우 확인.

## 운영 메모

- **재배포**: `git pull && docker compose up -d --build` (리뷰 데이터는 볼륨에 유지됨)
- **DB 초기화**: `docker compose down -v && docker compose up -d` (리뷰 삭제 + 축제 재시딩)
- **로그**: `docker compose logs -f backend`
- uvicorn `--workers`는 늘리지 말 것 (SQLite 단일 파일 동시 쓰기 락 문제)
- Gemini 무료 키는 할당량 초과(429) 시 폴백 응답으로 강등됨
- 현재 HTTP 평문 + 리뷰 비밀번호 평문 저장 — 데모 용도로만 사용
