import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# 개발자님이 만드신 모듈 임포트
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

# Gemini 모델 설정
genai.configure(api_key=GEMINI_API_KEY)
generation_config = {
    "temperature": 0.7,
    "response_mime_type": "application/json", # 프론트엔드가 쓰기 편하게 JSON으로 응답 강제
}
# model = genai.GenerativeModel(
#     model_name="gemini-1.5-flash",
#     generation_config=generation_config
# )
model = genai.GenerativeModel('gemini-1.5-flash')
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

# 결과를 저장할 폴더가 없다면 자동으로 생성
os.makedirs('pre_result', exist_ok=True)

print("🔄 JSON 데이터 전처리를 시작합니다...")
for source_file in file_paths:
    # try-except를 for문 안으로 이동시켜야 파일이 없어도 반복문이 끊기지 않습니다.
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
    # 사용자 성향 분석 설문 실행
    answers = run_terminal_frontend()
    
    selected_course_id = answers["preference"]
    print(f"\n[서버 로그] 선택된 코스 ID: {selected_course_id}")
    
    # DB에서 코스 정보 가져오기
    course_data = get_course_data(selected_course_id)
    
    # LLM 프롬프트 생성
    final_prompt = generate_llm_prompt(course_data)
    
    # 추가: 시스템 프롬프트에 JSON 출력 포맷 지시를 한 번 더 명확히 합침
    final_prompt += """
    
    [출력 지시사항]
    반드시 아래 JSON 형식으로만 출력해. 백틱(```json)이나 다른 설명은 절대 포함하지 마.
    {
        "message": "사용자님에게 추천 코스를 안내해 드립니다! ... (여기에 스토리를 작성해)",
        "places": [
            {
                "name": "장소명",
                "lat": 0.0,
                "lng": 0.0,
                "image_url": "이미지 주소",
                "address": "주소"
            }
        ]
    }
    """
    
    print("\n✨ [최종 조립된 프롬프트 내용] ✨\n")
    print(final_prompt)
    
    # ==========================================
    # 4. Gemini 3.5 Flash 호출 및 응답 출력
    # ==========================================
    print("\n🚀 Gemini API로 데이터를 전송하고 맞춤형 스토리를 생성 중입니다...\n")
    
    try:
        response = model.generate_content(final_prompt)
        print("🎉 [Gemini의 최종 응답 (완벽한 JSON 형태)] 🎉\n")
        
        # 반환된 텍스트가 유효한 JSON인지 파싱해서 깔끔하게 출력
        response_json = json.loads(response.text)
        print(json.dumps(response_json, indent=4, ensure_ascii=False))
        
    except json.JSONDecodeError:
        print("🚨 에러: Gemini가 반환한 텍스트가 올바른 JSON 형식이 아닙니다.")
        print("원시 데이터:", response.text)
    except Exception as e:
        print(f"🚨 Gemini API 호출 중 에러 발생: {e}")