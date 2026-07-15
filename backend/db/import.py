import json
import sqlite3
import os

# 1. 파일 경로 정의
base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, 'festivals.json')
db_path = os.path.join(base_dir, 'festival.db')

# 2. JSON 데이터 불러오기
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
except FileNotFoundError:
    print("❌ festivals.json 파일을 찾을 수 없습니다.")
    exit()

# 💡 [핵심 수정] 전달받은 JSON 구조에 맞춰 데이터 목록 안전하게 추출하기
festivals = []
if isinstance(raw_data, dict):
    # 구조 1: 현재 전달받은 "items" 키 아래 리스트가 들어있는 구조 🌟 (해결책)
    if 'items' in raw_data and isinstance(raw_data['items'], list):
        festivals = raw_data['items']
    
    # 구조 2: 공공데이터(TourAPI) 원본 트리 구조 (response -> body -> items -> item)
    elif 'response' in raw_data:
        try:
            items = raw_data['response']['body']['items']['item']
            festivals = items if isinstance(items, list) else [items]
        except (KeyError, TypeError):
            festivals = [raw_data]
            
    # 구조 3: 그 외 일반 단일 객체
    else:
        festivals = [raw_data]
        
elif isinstance(raw_data, list):
    # 구조 4: 바로 리스트로 시작하는 구조
    festivals = raw_data

# 3. SQLite 연결 및 설정
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 외래키 제약 활성화
cursor.execute("PRAGMA foreign_keys = ON;")

# INSERT 쿼리 (동일한 ID가 있으면 업데이트)
insert_query = """
INSERT OR REPLACE INTO festivals (
    content_id, title, addr1, addr2, tel, first_image, first_image2, map_x, map_y
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

# 4. 데이터 정제 및 파싱
insert_data = []
for index, item in enumerate(festivals):
    if not isinstance(item, dict):
        continue

    content_id = item.get('contentid')
    title = item.get('title')

    # 필수 값(ID, 장소명) 누락 검사 및 스킵 처리
    if not content_id or not title:
        print(f"⚠️ 경고: {index}번째 데이터에 필수값(contentid 또는 title)이 없어 제외합니다. (데이터: {item})")
        continue

    # 데이터 매핑 및 실수형(REAL) 타입 변환 안전처리
    try:
        map_x = float(item.get('mapx')) if item.get('mapx') else 0.0
        map_y = float(item.get('mapy')) if item.get('mapy') else 0.0
    except ValueError:
        map_x, map_y = 0.0, 0.0

    insert_data.append((
        content_id,
        title,
        item.get('addr1'),
        item.get('addr2'),
        item.get('tel'),
        item.get('firstimage'),
        item.get('firstimage2'),
        map_x,
        map_y
    ))

# 5. 벌크 인서트 실행
if insert_data:
    cursor.executemany(insert_query, insert_data)
    conn.commit()
    print(f"✅ 성공: 총 {len(insert_data)}개의 축제 데이터를 가져왔습니다.")
else:
    print("⚠️ 저장할 수 있는 유효한 데이터가 없습니다.")

conn.close()