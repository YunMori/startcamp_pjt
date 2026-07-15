from prepro import preprocess_poi_data
from user_type_select import generate_llm_prompt, get_course_data, run_terminal_frontend, user_preference, user_type_select
import json, os


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
# 결과를 저장할 폴더가 없다면 자동으로 생성 (에러 방지)


try:
    # 전처리 함수 실행
    for source_file in file_paths:
        with open(source_file, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        lightweight_data = preprocess_poi_data(raw_data)
        file_name = os.path.basename(source_file) # 파일명만 추출 (예: 'data/대전_충청권_관광지.json' -> '대전_충청권_관광지.json')
        save_path = os.path.join('pre_result', f'pre_{file_name}') # 안전하게 경로 결합 (pre_result/result_대전_충청권_관광지.json)
        with open(save_path, 'w', encoding='utf-8') as out_f: # 전처리된 데이터를 새로운 JSON으로 저장하여 LLM Context로 활용
            json.dump(lightweight_data, out_f, ensure_ascii=False)
            
    # 사용자 성향 분석 및 코스 추천
    answers = run_terminal_frontend()
    
    selected_course_id = answers["preference"]
    print(f"[서버 로그] 선택된 코스 ID: {selected_course_id}")
    course_data = get_course_data(selected_course_id)
    final_prompt = generate_llm_prompt(course_data)
    
    print("\n✨ [최종 LLM API로 전송될 프롬프트] ✨\n")
    print(final_prompt)
except FileNotFoundError:
    print(f"⚠️ {source_file} 파일을 찾을 수 없습니다. 건너뛰고 다음 파일을 진행합니다.")
