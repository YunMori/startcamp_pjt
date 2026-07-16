#!/bin/sh
set -e
cd /app/backend
mkdir -p db

# 이미지 재빌드 시 갱신된 시드 파일이 볼륨에 반영되도록 복사
cp -f /app/seed/festivals.json /app/seed/import.py db/

# 테이블 생성 + created_at 인라인 마이그레이션 (app.py 모듈 임포트 시 실행됨)
python -c "import app"

# import.py는 테이블을 만들지 않고 INSERT만 하므로 행 수로 시드 여부 판단
COUNT=$(python -c "import sqlite3; print(sqlite3.connect('db/festival.db').execute('SELECT COUNT(*) FROM festivals').fetchone()[0])")
if [ "$COUNT" -eq 0 ]; then
  echo "festivals 테이블 시딩 시작..."
  python db/import.py
fi

# SQLite 단일 파일이므로 workers는 1로 유지
exec uvicorn app:app --host 0.0.0.0 --port 8000
