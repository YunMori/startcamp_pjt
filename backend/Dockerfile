# 빌드 컨텍스트: 저장소 루트 (docker-compose.yml 참고)
FROM python:3.12-slim

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# recommend.py가 REPO_ROOT(/app) 기준으로 pre_result/를 읽으므로 backend/와 형제로 배치
COPY pre_result/ /app/pre_result/
COPY backend/ /app/backend/

# 시드 파일은 볼륨이 /app/backend/db를 가려도 접근 가능하도록 별도 보관
COPY backend/db/festivals.json backend/db/import.py /app/seed/

COPY docker/backend-entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

WORKDIR /app/backend
EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
