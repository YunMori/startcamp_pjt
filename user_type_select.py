import time

# ==========================================
# [백엔드] 1. 질문을 던지고 입력을 받는 헬퍼 함수
# ==========================================
def ask_question(question, options, valid_keys=['1', '2', '3']):
    """반복되는 질문과 예외 처리를 깔끔하게 해주는 헬퍼 함수입니다."""
    while True:
        print(f"\n🍒 챗봇: {question}")
        ans = input(f"({options}) : ")
        if ans in valid_keys:
            return ans
        print("⚠️ 올바른 번호를 입력해주세요!")

# ==========================================
# [백엔드] 2. 데이트 코스 분류 알고리즘 엔진
# ==========================================
def mobility_preference(user_answers):
    ans = ask_question("두 분의 이동 수단은 어떻게 되나요?", "1: 뚜벅이 🚶, 2: 자동차 🚗", ['1', '2'])
    user_answers["mobility"] = "walk" if ans == '1' else "car"

def festival_preference(user_answers):
    ans = ask_question("현재 대전/충청 지역에 핫한 축제들이 열리고 있어요! 관심 있으신가요?", "1: 네, 가보고 싶어요 🎉, 2: 아니요, 조용히 보낼래요 ☕", ['1', '2'])
    user_answers["festival"] = True if ans == '1' else False

def user_preference(user_answers, scores):
    print("\n" + "-"*50)
    print("🍒 챗봇: 두 분의 완벽한 데이트를 위해 5가지 성향을 알아볼게요!")
    print("-" * 50)

    # [질문 1] 분위기 성향
    ans1 = ask_question("가장 선호하는 데이트 분위기는 무엇인가요?", "1: 세련되고 트렌디한 도심 🏙️, 2: 고즈넉하고 감성적인 골목길 📸, 3: 탁 트인 자연과 여유 🍃")
    if ans1 == '1': scores["course_B"] += 3; scores["course_D"] += 2
    elif ans1 == '2': scores["course_C"] += 3
    elif ans1 == '3': scores["course_A"] += 3; scores["course_E"] += 2

    # [질문 2] 활동성 성향
    ans2 = ask_question("데이트 중 선호하는 활동은 무엇인가요?", "1: 몸을 움직이는 액티비티나 체험 💦, 2: 예쁜 풍경이나 전시를 보며 걷기 📷, 3: 한 곳에 오래 머물며 딥톡하기 ☕")
    if ans2 == '1': scores["course_B"] += 3; scores["course_D"] += 1
    elif ans2 == '2': scores["course_C"] += 2; scores["course_E"] += 2
    elif ans2 == '3': scores["course_A"] += 3; scores["course_C"] += 1

    # [질문 3] 식사/음주 성향
    ans3 = ask_question("오늘의 식사 및 음주 스타일은?", "1: 분위기 좋은 식당과 예쁜 카페 🍽️, 2: 왁자지껄한 분위기에서 시원한 맥주 한 잔 🍻, 3: 가성비 좋고 맛있는 로컬 노포 🍜")
    if ans3 == '1': scores["course_A"] += 2; scores["course_B"] += 2; scores["course_C"] += 1
    elif ans3 == '2': scores["course_D"] += 3; scores["course_E"] += 3
    elif ans3 == '3': scores["course_C"] += 3; scores["course_D"] += 1

    # [질문 4] 시간대 성향
    ans4 = ask_question("오늘 데이트의 하이라이트 시간대는 언제인가요?", "1: 햇살 좋은 낮 시간대 ☀️, 2: 노을이 지는 저녁부터 화려한 야경까지 🌙, 3: 시간 상관없이 하루 종일 ⏰")
    if ans4 == '1': scores["course_A"] += 2; scores["course_B"] += 2
    elif ans4 == '2': scores["course_D"] += 2; scores["course_E"] += 3; scores["course_A"] += 1
    elif ans4 == '3': scores["course_C"] += 2; scores["course_B"] += 1

    # [질문 5] 스트레스 해소 성향
    ans5 = ask_question("데이트를 통해 어떤 방법으로 스트레스를 푸시나요?", "1: 시끌벅적한 축제나 핫플의 에너지 🎉, 2: 연인과 둘만의 프라이빗한 휴식 🤫, 3: 꿀잼 스포츠나 오락으로 승부욕 불태우기 🔥")
    if ans5 == '1': scores["course_D"] += 3; scores["course_E"] += 3
    elif ans5 == '2': scores["course_A"] += 3; scores["course_C"] += 2
    elif ans5 == '3': scores["course_B"] += 3

    # ==========================================
    # 🎯 [핵심] 하드 필터링 적용 (불가능한 코스 배제)
    # ==========================================
    # 뚜벅이는 외곽 코스(A: 대청호, E: 공주) 절대 불가
    if user_answers["mobility"] == "walk":
        scores["course_A"] -= 9999
        scores["course_E"] -= 9999

    # 축제 참여 희망 여부에 따른 필터링
    if user_answers["festival"] == True:
        scores["course_D"] += 100 # 유성 축제 가산점
        scores["course_E"] += 100 # 공주 축제 가산점
    else:
        scores["course_D"] -= 9999 # 축제 미희망시 축제 코스 배제
        scores["course_E"] -= 9999

def user_type_select(user_answers, scores):
    # 딕셔너리에서 최종 점수가 가장 높은 코스(key)를 찾아냅니다.
    best_course = max(scores, key=scores.get)
    user_answers["preference"] = best_course

def get_course_data(selected_course_id):
    # DB에 저장된 마스터 코스 데이터 풀 (실제로는 DB에서 Fetch 해옵니다)
    course_pool = {
        "course_A": {
            "name": "대청호 물길 힐링 코스", 
            "places": [
                {"title": "대청호자연수변공원", "addr1": "대전광역시 동구 추동 328", "tel": "", "firstimage": "http://...image1.jpg"},
                {"title": "카페 팡시온", "addr1": "대전광역시 동구 회남로275번길 227", "tel": "", "firstimage": "http://...image2.jpg"},
                {"title": "더리스", "addr1": "대전광역시 동구 냉천로 34-8", "tel": "042-123-4567", "firstimage": "http://...image3.jpg"}
            ]
        },
        "course_B": {
            "name": "도룡동 실내 액티비티 코스", 
            "places": [
                {"title": "스몹 대전", "addr1": "대전광역시 유성구 엑스포로 1 신세계백화점 6층", "tel": "042-000-0000", "firstimage": "http://...image1.png"},
                {"title": "더 빛나", "addr1": "대전광역시 유성구 엑스포로 131", "tel": "042-111-1111", "firstimage": "http://...image2.jpg"},
                {"title": "엑스포다리 야경", "addr1": "대전광역시 유성구 도룡동", "tel": "", "firstimage": "http://...image3.jpg"}
            ]
        },
        "course_C": {
            "name": "소제동 레트로 감성 코스", 
            "places": [
                {"title": "테미오래", "addr1": "대전광역시 중구 보문로205번길 13", "tel": "", "firstimage": "http://...image1.jpg"},
                {"title": "치앙마이방콕", "addr1": "대전광역시 동구 철갑3길 8", "tel": "", "firstimage": "http://...image2.jpg"},
                {"title": "볕 (수플레 카페)", "addr1": "대전광역시 동구 수향2길 7", "tel": "", "firstimage": "http://...image3.jpg"}
            ]
        },
        "course_D": {
            "name": "유성 도심 재즈&맥주 페스타 코스", 
            "places": [
                {"title": "유성재즈&맥주페스타", "addr1": "대전광역시 유성구 어은로 27 유림공원 일원", "tel": "042-611-2080", "firstimage": "http://...image1.jpg"},
                {"title": "1984그수육집칼국수", "addr1": "대전광역시 유성구 원신흥남로42번길 5-22", "tel": "", "firstimage": "http://...image2.jpg"},
                {"title": "유성온천 족욕체험장", "addr1": "대전광역시 유성구 봉명동 574", "tel": "", "firstimage": "http://...image3.jpg"}
            ]
        },
        "course_E": {
            "name": "공주 야밤 맥주축제 드라이브 코스", 
            "places": [
                {"title": "공주야밤 맥주축제", "addr1": "충청남도 공주시 금벽로 368 공주 금강신관공원 일원", "tel": "041-840-8404", "firstimage": "http://...image1.jpg"},
                {"title": "공주 공산성", "addr1": "충청남도 공주시 웅진로 280", "tel": "", "firstimage": "http://...image2.jpg"},
                {"title": "베이커리 밤마을", "addr1": "충청남도 공주시 백미고을길 5-13", "tel": "", "firstimage": "http://...image3.jpg"}
            ]
        }
    }
    return course_pool[selected_course_id]

# ==========================================
# [프론트엔드] 3. 터미널 기반 대화형 UI 시뮬레이터
# ==========================================
def run_terminal_frontend():
    print("="*60)
    print(" 🌸 로맨틱 대전/충청 데이트 코스 AI 플래너 🌸 ")
    print("="*60)
    
    user_answers = {}
    # 코스별 초기 점수
    scores = {
        "course_A": 0, # 대청호 힐링 (차량 필수)
        "course_B": 0, # 도룡동 액티비티
        "course_C": 0, # 소제동 레트로
        "course_D": 0, # 도심 맥주 축제
        "course_E": 0  # 공주 드라이브 축제 (차량 필수)
    }

    mobility_preference(user_answers)
    festival_preference(user_answers)
    user_preference(user_answers, scores) 
    
    # 성향 점수 종합 후 코스 확정
    user_type_select(user_answers, scores)

    print("\n" + "="*60)
    print("🍒 챗봇: 모든 정보를 수집했습니다! 맞춤형 코스를 생성합니다...")
    print("="*60)
    
    return user_answers

# ==========================================
# [백엔드] 4. 최종 LLM 프롬프트 조립
# ==========================================
def generate_llm_prompt(course_data):
    # DB에서 꺼내온 각 장소 정보를 문자열로 결합합니다.
    places_info = ""
    for i, place in enumerate(course_data["places"], 1):
        places_info += f"{i}. 장소명: {place['title']} / 주소: {place['addr1']} / 전화번호: {place.get('tel', '정보없음')} / 이미지URL: {place['firstimage']}\n"
        
    llm_prompt = f"""
너는 대전/충청 데이트 코스를 친절하게 안내해 주는 로맨틱 가이드 챗봇이야.
백엔드 알고리즘이 사용자 성향을 분석하여 아래의 데이트 코스 및 세부 장소 정보를 가져왔어.

[추천 코스명]: {course_data['name']}

[상세 장소 정보]
{places_info}

[지시사항]
1. 사용자의 성향과 이 코스가 왜 잘 어울리는지 공감하며 부드러운 톤으로 설명을 시작해라.
2. 텍스트 형태는 반드시 다음과 같은 포맷을 유지해라.
   "사용자님에게 [{course_data['name']}]를 추천해 드립니다! 이 코스는 [장소1]->[장소2]->[장소3] 순서로 정해져 있습니다. 각각의 장소 정보를 안내해 드릴게요."
3. 그 다음, 제공된 [상세 장소 정보]의 장소명, 주소, 전화번호, 이미지 URL을 활용해서 각 장소의 매력과 동선을 대화하듯 매끄럽게 설명해라.
4. 설명 마지막에는 이 코스가 사용자님의 성향과 얼마나 잘 어울리는지 대략적인 총평을 덧붙여라.
"""
    return llm_prompt

# ==========================================
# 🚀 전체 파이프라인 실행
# ==========================================
if __name__ == "__main__":
    # 1. 프론트엔드에서 사용자 응답 수집
    answers = run_terminal_frontend()
    
    # 2. 백엔드에서 알고리즘 돌리기 (최고 점수 코스 ID 반환)
    selected_course_id = answers["preference"]
    print(f"[서버 로그] 선택된 코스 ID: {selected_course_id}")
    
    # 3. DB 조회 (가상의 데이터 반환)
    course_data = get_course_data(selected_course_id)
    
    # 4. LLM 프롬프트 조립
    final_prompt = generate_llm_prompt(course_data)
    
    print("\n✨ [최종 LLM API로 전송될 프롬프트] ✨\n")
    print(final_prompt)