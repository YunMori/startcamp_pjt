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
