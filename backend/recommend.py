# ai_chat/user_type_select.py의 추천 엔진을 API에서 쓸 수 있게 이식한 모듈.
# - input() 기반 설문 → 답변 dict를 받는 순수 함수(score_courses)
# - get_course_data: pre_result 경로를 절대경로로, lat/lng 보존 (지도 핀 좌표)
# - Gemini 호출(스토리텔링/자유채팅)과 키 없는 환경용 폴백 포함
import os
import json
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(BASE_DIR)
PRE_RESULT_DIR = os.path.join(REPO_ROOT, "pre_result")

load_dotenv(os.path.join(REPO_ROOT, ".env"))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

_client = genai.Client(api_key=GEMINI_API_KEY) if (genai and GEMINI_API_KEY) else None
GEMINI_MODEL = "gemini-3.5-flash"

COURSE_NAMES = {
    "course_A": "대청호 물길 힐링 코스",
    "course_B": "도룡동 실내 액티비티 코스",
    "course_C": "소제동 레트로 감성 코스",
    "course_D": "유성 도심 축제 데이트 코스",
    "course_E": "공주 역사 & 야밤 축제 코스",
}

COURSE_MAP = {
    "course_A": ["대청댐", "장태산자연휴양림", "대청호자연수변공원"],
    "course_B": ["스몹 대전", "대전아쿠아리움", "대전엑스포시민광장스케이트장"],
    "course_C": ["테미오래", "소제동", "대동하늘공원"],
    "course_D": ["유성온천문화축제", "유성온천공원", "촌놈들연탄구이 본점"],
    "course_E": ["공주 공산성 [유네스코 세계유산]", "공주야밤 맥주축제", "베이커리 밤마을"],
}

# 성향 5문항(q1~q5)의 답변('1'|'2'|'3')별 코스 가중치 — user_type_select.user_preference와 동일
QUESTION_WEIGHTS = {
    "q1": {  # 분위기
        "1": {"course_B": 3, "course_D": 2},
        "2": {"course_C": 3},
        "3": {"course_A": 3, "course_E": 2},
    },
    "q2": {  # 활동성
        "1": {"course_B": 3, "course_D": 1},
        "2": {"course_C": 2, "course_E": 2},
        "3": {"course_A": 3, "course_C": 1},
    },
    "q3": {  # 식사/음주
        "1": {"course_A": 2, "course_B": 2, "course_C": 1},
        "2": {"course_D": 3, "course_E": 3},
        "3": {"course_C": 3, "course_D": 1},
    },
    "q4": {  # 시간대
        "1": {"course_A": 2, "course_B": 2},
        "2": {"course_D": 2, "course_E": 3, "course_A": 1},
        "3": {"course_C": 2, "course_B": 1},
    },
    "q5": {  # 스트레스 해소
        "1": {"course_D": 3, "course_E": 3},
        "2": {"course_A": 3, "course_C": 2},
        "3": {"course_B": 3},
    },
}


def score_courses(answers: Dict[str, Any], top_n: int = 3) -> List[str]:
    """설문 답변으로 코스 점수를 계산해 상위 top_n개의 코스 ID를 반환한다.

    answers: {mobility: 'walk'|'car', festival: bool, q1~q5: '1'|'2'|'3'}
    하드 필터(뚜벅이 → 외곽 코스 제외, 축제 미희망 → 축제 코스 제외)로
    제외된 코스는 순위에서 아예 빠지므로 결과가 top_n보다 적을 수 있다.
    """
    scores = {course_id: 0 for course_id in COURSE_NAMES}
    for question, weights in QUESTION_WEIGHTS.items():
        for course_id, weight in weights.get(str(answers.get(question, "")), {}).items():
            scores[course_id] += weight

    excluded = set()
    if answers.get("mobility") == "walk":
        excluded |= {"course_A", "course_E"}
    if answers.get("festival"):
        scores["course_D"] += 100
        scores["course_E"] += 100
    else:
        excluded |= {"course_D", "course_E"}

    ranked = sorted(
        (c for c in scores if c not in excluded),
        key=lambda c: scores[c],
        reverse=True,
    )
    return ranked[:top_n]


def get_course_data(course_id: str) -> Dict[str, Any]:
    """pre_result 데이터에서 코스 소속 장소들을 좌표 포함으로 조회한다."""
    target_titles = COURSE_MAP.get(course_id, [])
    found: Dict[str, Dict[str, Any]] = {}

    for filename in sorted(os.listdir(PRE_RESULT_DIR)):
        file_path = os.path.join(PRE_RESULT_DIR, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        for item in data:
            title = item.get("title")
            if title in target_titles and title not in found:
                found[title] = {
                    "title": title,
                    "addr1": item.get("address", "주소 정보 없음"),
                    "tel": "정보없음",
                    "firstimage": item.get("image", ""),
                    "lat": float(item.get("lat", 0.0)),
                    "lng": float(item.get("lng", 0.0)),
                }

    # 코스 정의 순서(동선 순서)를 유지
    places = [found[t] for t in target_titles if t in found]
    return {
        "id": course_id,
        "name": COURSE_NAMES.get(course_id, "추천 데이트 코스"),
        "places": places,
    }


def generate_llm_prompt(course_data: Dict[str, Any]) -> str:
    places_info = ""
    for i, place in enumerate(course_data["places"], 1):
        places_info += (
            f"{i}. 장소명: {place['title']} / 주소: {place['addr1']} / "
            f"전화번호: {place.get('tel', '정보없음')} / 이미지URL: {place['firstimage']}\n"
        )

    return f"""
    너는 데이트 코스 가이드야. 아래 장소들을 방문하는 데이트 코스를 추천해 줘.
    [코스명]: {course_data['name']}
    [장소들]: {places_info}

    [지시사항]
    - 사용자에게 {course_data['name']}를 추천하는 다정한 메시지를 작성해.
    - 장소들의 특징을 엮어서 자연스러운 스토리텔링을 해줘.
    - 다른 설명은 절대 하지 말고, 아래 형식의 JSON 데이터만 출력해.

    {{
        "message": "작성한 스토리 메시지"
    }}
    """


def _fallback_story(course_data: Dict[str, Any]) -> str:
    names = " → ".join(p["title"] for p in course_data["places"])
    return (
        f"'{course_data['name']}'를 추천해요! 💕 "
        f"{names} 순서로 둘러보시면 하루가 알차게 채워질 거예요. "
        f"각 장소는 아래 지도에서 확인해 보세요!"
    )


def generate_course_story(course_data: Dict[str, Any]) -> str:
    """Gemini로 코스 스토리텔링 메시지를 생성한다. 키가 없거나 실패하면 폴백 문구."""
    if _client is None:
        return _fallback_story(course_data)

    prompt = generate_llm_prompt(course_data)
    prompt += """

    [출력 지시사항]
    반드시 아래 JSON 형식으로만 출력해. 백틱(```json)이나 다른 설명은 절대 포함하지 마.
    {
        "message": "사용자님에게 추천 코스를 안내해 드립니다! ... (각 장소의 매력을 연결하여 로맨틱한 스토리텔링 작성)"
    }
    """
    try:
        response = _client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                response_mime_type="application/json",
            ),
        )
        return json.loads(response.text).get("message", _fallback_story(course_data))
    except Exception as e:
        print(f"[recommend] Gemini 스토리 생성 실패: {e}")
        return _fallback_story(course_data)


FREE_CHAT_SYSTEM = (
    "너는 대전·충청권 연인 데이트 큐레이터 챗봇 '러비'야. "
    "다정하고 친근한 말투로 짧게(3문장 이내) 답해. "
    "데이트 코스가 필요하면 설문 선택지를 이용하라고 자연스럽게 안내해."
)


def generate_free_reply(messages: List[Dict[str, str]]) -> Optional[str]:
    """자유 채팅 응답. messages: [{role: 'user'|'assistant', content: str}]"""
    if _client is None:
        return None
    conversation = "\n".join(
        f"{'사용자' if m.get('role') == 'user' else '챗봇'}: {m.get('content', '')}"
        for m in messages
    )
    prompt = f"{FREE_CHAT_SYSTEM}\n\n[대화]\n{conversation}\n챗봇:"
    try:
        response = _client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.8),
        )
        return (response.text or "").strip() or None
    except Exception as e:
        print(f"[recommend] Gemini 자유채팅 실패: {e}")
        return None
