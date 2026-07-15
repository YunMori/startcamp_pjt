import json
import os # 파일 경로와 폴더 생성을 다루기 위해 추가

def preprocess_poi_data(json_data):
    """
    TourAPI 4.0 원본 JSON 데이터를 LLM 및 프론트엔드 렌더링에 적합하게 경량화합니다.
    """
    processed_data = []

    # items 배열 순회
    for item in json_data.get("items", []):
        mapx = item.get("mapx", "")
        mapy = item.get("mapy", "")
        
        # 1. 예외 처리: 좌표값이 없거나 "0"인 경우(비정상 데이터) 제외
        if not mapx or not mapy or mapx == "0" or mapy == "0":
            continue

        try:
            # 2. 필수 필드 추출 및 타입 변환
            cleaned_item = {
                "id": item.get("contentid", ""),
                "title": item.get("title", ""),
                "address": item.get("addr1", ""),      # 주소가 없을 경우 "" 유지
                "image": item.get("firstimage", ""),   # 이미지가 없을 경우 "" 유지
                "lat": float(mapy),                    # 위도 (문자열 -> 실수 변환)
                "lng": float(mapx)                     # 경도 (문자열 -> 실수 변환)
            }
            processed_data.append(cleaned_item)
            
        except ValueError:
            # float 변환 실패 시 해당 항목 건너뜀
            continue

    return processed_data


# ==========================================
# 🚀 사용 예시 (테스트 로직)
# ==========================================
if __name__ == "__main__":
    # 백엔드 서버에 저장된 원본 JSON 파일 경로 목록
    file_paths = [
        'data/대전_충청권_관광지.json', 
        'data/대전_충청권_레포츠.json', 
        'data/대전_충청권_문화시설.json', 
        'data/대전_충청권_쇼핑.json', 
        'data/대전_충청권_숙박.json', 
        'data/대전_충청권_여행코스.json', 
        'data/대전_충청권_음식점.json', 
        'data/대전_충청권_축제공연행사.json'
    ]
    
    # 결과를 저장할 폴더가 없다면 자동으로 생성 (에러 방지)
    os.makedirs('pre_result', exist_ok=True)
    
    # for문 안쪽으로 try-except를 이동시켜, 특정 파일이 없어도 다음 파일은 계속 처리되도록 함
    for source_file in file_paths:
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                
            # 전처리 함수 실행
            lightweight_data = preprocess_poi_data(raw_data)
            
            # 파일명만 추출 (예: 'data/대전_충청권_관광지.json' -> '대전_충청권_관광지.json')
            file_name = os.path.basename(source_file)
            
            # 결과 확인
            print(f"✅ [{file_name}] 추출된 유효 장소 개수: {len(lightweight_data)}개")
            
            # 안전하게 경로 결합 (pre_result/result_대전_충청권_관광지.json)
            save_path = os.path.join('pre_result', f'pre_{file_name}')
            
            # 전처리된 데이터를 새로운 JSON으로 저장하여 LLM Context로 활용
            with open(save_path, 'w', encoding='utf-8') as out_f:
                json.dump(lightweight_data, out_f, ensure_ascii=False)
                
        except FileNotFoundError:
            # 배열 전체가 아닌 에러가 난 파일명만 정확히 출력
            print(f"⚠️ {source_file} 파일을 찾을 수 없습니다. 건너뛰고 다음 파일을 진행합니다.")