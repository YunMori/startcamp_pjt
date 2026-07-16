import os
import json
from dotenv import load_dotenv

# 새로운 공식 구글 패키지 임포트
from google import genai
from google.genai import types

from prepro import preprocess_poi_data
from user_type_select import generate_llm_prompt, get_course_data, run_terminal_frontend

# ==========================================
# 1. API 키 로드 및 Gemini 설정
# ==========================================
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("🚨 에러: .env 파일에 GEMINI_API_KEY가 없습니다!")
    exit()

client = genai.Client(api_key=GEMINI_API_KEY)

# ==========================================
# 2. JSON 데이터 전처리 파이프라인
# ==========================================
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

os.makedirs('pre_result', exist_ok=True)

print("🔄 JSON 데이터 전처리를 시작합니다...")
for source_file in file_paths:
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
            
        lightweight_data = preprocess_poi_data(raw_data)
        file_name = os.path.basename(source_file)
        save_path = os.path.join('pre_result', f'pre_{file_name}')
        
        with open(save_path, 'w', encoding='utf-8') as out_f:
            json.dump(lightweight_data, out_f, ensure_ascii=False)
            
    except FileNotFoundError:
        print(f"⚠️ {source_file} 파일을 찾을 수 없습니다. 건너뛰고 다음 파일을 진행합니다.")
        
print("✅ 전처리 완료!\n")


# ==========================================
# 3. 챗봇 성향 분석 및 프롬프트 조립
# ==========================================
if __name__ == "__main__":
    # 사용자 성향 분석 설문 실행 (로컬 콘솔용)
    answers = run_terminal_frontend()
    
    selected_course_id = answers["preference"]
    print(f"\n[서버 로그] 선택된 코스 ID: {selected_course_id}")
    
    # 공통 모듈에서 데이터 및 기본 프롬프트 가져오기
    course_data = get_course_data(selected_course_id)
    final_prompt = generate_llm_prompt(course_data)
    
    print("\n✨ [최종 조립된 프롬프트 내용] ✨\n")
    print(final_prompt)
    
    # ==========================================
    # 4. Gemini 3.5 Flash 호출 및 응답 출력
    # ==========================================
    print("\n🚀 Gemini API로 데이터를 전송하고 맞춤형 스토리를 생성 중입니다...\n")
    
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=final_prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                response_mime_type="application/json",
            )
        )
        print("\n🚀 Gemini API 응답 수신 완료! 🚀\n")
        # 1. LLM의 감성 멘트 파싱
        llm_result = json.loads(response.text)
        
        # 2. 신뢰할 수 있는 백엔드 DB 데이터와 안전하게 결합
        final_json_data = {
        "message": llm_result["message"],
        "places": []
        }
        
        for db_place in course_data["places"]:
            final_json_data["places"].append({
                "contentid": db_place.get("contentid"),
                "title": db_place.get("title"),
                "addr1": db_place.get("addr1", "주소 정보 없음"),
                "addr2": db_place.get("addr2", "상세주소 정보 없음"),
                "tel": db_place.get("tel", "번호 정보 없음"), # 기존 데이터에 tel 필드 보존 확인 필요
                "firstimage": db_place.get("firstimage", ""),
                "firstimage2": db_place.get("firstimage2", ""),
                "mapx": db_place.get("mapx", 0.3),
                "mapy": db_place.get("mapy", 0.3)
                })

        # 3. 최종 출력 확인
        print("🎉 [서버 내부에서 최종 완성된 JSON 데이터] 🎉\n")
        print(json.dumps(final_json_data, indent=4, ensure_ascii=False))
        
    except json.JSONDecodeError:
        print("🚨 에러: Gemini가 반환한 텍스트가 올바른 JSON 형식이 아닙니다.")
        print("원시 데이터:", response.text)
    except Exception as e:
        print(f"🚨 Gemini API 호출 중 에러 발생: {e}")