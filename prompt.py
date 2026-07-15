import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from dotenv import load_dotenv

# Gemini API 라이브러리 임포트
import google.generativeai as genai

# 환경변수 로드 (.env 파일에서 API 키를 읽어옵니다)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini 설정
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인해주세요.")
genai.configure(api_key=GEMINI_API_KEY)

# Gemini 1.5 Flash 모델 초기화 (정확한 모델명으로 수정 & JSON 출력 강제 옵션 추가)
generation_config = {
    "temperature": 0.7,
    "response_mime_type": "application/json", # 프론트엔드 연동을 위해 JSON 형식으로만 응답하게 강제
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", 
    generation_config=generation_config
)

app = FastAPI(title="LocalHub 데이트 코스 챗봇 API")

# ==========================================
# 1. Pydantic 스키마 정의 (프론트엔드와 주고받을 데이터 규격)
# ==========================================
class UserAnswers(BaseModel):
    mobility: str = Field(..., description="이동수단 (walk 또는 car)")
    preference: str = Field(..., description="알고리즘에서 도출된 최고 점수 코스 ID (예: course_A)")
    festival: bool = Field(False, description="축제 참여 여부")

class Place(BaseModel):
    name: str = Field(..., description="장소명")
    lat: float = Field(..., description="위도")
    lng: float = Field(..., description="경도")
    image_url: str = Field("", description="이미지 URL")
    address: str = Field("", description="주소")

class ChatResponse(BaseModel):
    message: str = Field(..., description="Gemini가 생성한 맞춤형 스토리텔링 텍스트")
    places: List[Place] = Field(..., description="지도 핀 마커용 좌표 배열")

# ==========================================
# 2. 내부 데이터 및 헬퍼 함수 (앞서 만든 알고리즘 활용)
# ==========================================
def get_course_data(selected_course_id: str) -> Dict[str, Any]:
    # 5개의 마스터 코스 데이터를 모두 채워 넣었습니다.
    course_pool = {
        "course_A": {
            "name": "대청호 물길 힐링 코스", 
            "places": [
                {"title": "대청호자연수변공원", "addr1": "대전광역시 동구 추동 328", "mapy": "36.372645", "mapx": "127.474717", "firstimage": "http://tong.visitkorea.or.kr/cms/resource/55/3542255_image2_1.jpg"},
                {"title": "카페 팡시온", "addr1": "대전광역시 동구 회남로275번길 227", "mapy": "36.377814", "mapx": "127.504067", "firstimage": "http://tong.visitkorea.or.kr/cms/resource/64/2767064_image2_1.jpg"},
                {"title": "더리스", "addr1": "대전광역시 동구 냉천로 34-8", "mapy": "36.386122", "mapx": "127.484101", "firstimage": "http://tong.visitkorea.or.kr/cms/resource/16/2735316_image2_1.jpg"}
            ]
        },
        "course_B": {
            "name": "도룡동 실내 액티비티 코스", 
            "places": [
                {"title": "스몹 대전", "addr1": "대전광역시 유성구 엑스포로 1 신세계백화점 6층", "mapy": "36.375101", "mapx": "127.382065", "firstimage": "http://tong.visitkorea.or.kr/cms/resource/95/3535595_image2_1.png"},
                {"title": "더 빛나", "addr1": "대전광역시 유성구 엑스포로 131", "mapy": "36.375349", "mapx": "127.394130", "firstimage": "http://tong.visitkorea.or.kr/cms/resource/14/2767214_image2_1.jpg"},
                {"title": "대전신세계 Art&Science점", "addr1": "대전광역시 유성구 엑스포로 1", "mapy": "36.375181", "mapx": "127.381765", "firstimage": "http://tong.visitkorea.or.kr/cms/resource/92/4023492_image2_1.jpg"}
            ]
        },
        "course_C": {
            "name": "소제동 레트로 감성 코스", 
            "places": [
                {"title": "테미오래", "addr1": "대전광역시 중구 보문로205번길 13", "mapy": "36.320666", "mapx": "127.423268", "firstimage": "http://tong.visitkorea.or.kr/cms/resource/27/3505827_image2_1.jpg"},
                {"title": "치앙마이방콕", "addr1": "대전광역시 동구 철갑3길 8", "mapy": "36.334229", "mapx": "127.437747", "firstimage": "http://tong.visitkorea.or.kr/cms/resource/18/2865818_image2_1.jpg"},
                {"title": "볕 (수플레 카페)", "addr1": "대전광역시 동구 수향2길 7", "mapy": "36.335524", "mapx": "127.437061", "firstimage": ""}
            ]
        },
        "course_D": {
            "name": "도심 속 재즈&맥주 페스타 코스", 
            "places": [
                {"title": "유성재즈&맥주페스타", "addr1": "대전광역시 유성구 어은로 27 유림공원 일원", "mapy": "36.360730", "mapx": "127.357706", "firstimage": "http://tong.visitkorea.or.kr/cms/resource/23/3338823_image2_1.jpg"},
                {"title": "1984그수육집칼국수", "addr1": "대전광역시 유성구 원신흥남로42번길 5-22", "mapy": "36.337211", "mapx": "127.338686", "firstimage": "http://tong.visitkorea.or.kr/cms/resource/21/4057021_image2_1.jpg"},
                {"title": "유성온천 족욕체험장", "addr1": "대전광역시 유성구 봉명동 574", "mapy": "36.355044", "mapx": "127.345432", "firstimage": "http://tong.visitkorea.or.kr/cms/resource/22/3350822_image2_1.jpg"}
            ]
        },
        "course_E": {
            "name": "공주 야밤 맥주축제 드라이브 코스", 
            "places": [
                {"title": "공주야밤 맥주축제", "addr1": "충청남도 공주시 금벽로 368 공주 금강신관공원 일원", "mapy": "36.470245", "mapx": "127.127538", "firstimage": "http://tong.visitkorea.or.kr/cms/resource/09/3520309_image2_1.jpg"},
                {"title": "공주 공산성", "addr1": "충청남도 공주시 웅진로 280", "mapy": "36.462949", "mapx": "127.126790", "firstimage": "http://tong.visitkorea.or.kr/cms/resource/41/3404541_image2_1.jpg"},
                {"title": "베이커리 밤마을", "addr1": "충청남도 공주시 백미고을길 5-13", "mapy": "36.464625", "mapx": "127.122924", "firstimage": "http://tong.visitkorea.or.kr/cms/resource/75/2834375_image2_1.jpg"}
            ]
        }
    }
    return course_pool.get(selected_course_id, course_pool["course_A"])

# ==========================================
# 3. FastAPI 엔드포인트
# ==========================================
@app.post("/api/chat", response_model=ChatResponse)
async def generate_dating_course(user_answers: UserAnswers):
    try:
        # 1. 프론트엔드에서 전달받은 성향(preference)으로 DB 조회
        course_data = get_course_data(user_answers.preference)
        
        # 2. LLM에게 던져줄 프롬프트 조립
        places_info = ""
        for i, place in enumerate(course_data["places"], 1):
            places_info += f"{i}. 장소명: {place['title']} / 주소: {place['addr1']}\n"
        
        prompt = f"""
        너는 대전/충청 데이트 코스를 안내해 주는 친절하고 로맨틱한 가이드 챗봇이야.
        아래의 데이트 코스와 장소 정보를 바탕으로 사용자에게 데이트 동선을 제안해줘.
        
        [추천 코스명]: {course_data['name']}
        [상세 장소 정보]
        {places_info}
        
        [출력 지시사항 - 매우 중요]
        반드시 아래 JSON 형식으로만 출력해라. 백틱(```json)이나 다른 설명은 절대 포함하지 마라.
        {{
            "message": "사용자님에게 {course_data['name']}를 추천해 드립니다! ... (각 장소의 매력을 연결하여 부드러운 톤으로 설명)",
            "places": [
                {{
                    "name": "장소명",
                    "lat": 0.0,
                    "lng": 0.0,
                    "image_url": "이미지 주소",
                    "address": "주소"
                }}
            ]
        }}
        """

        # 3. Gemini API 호출
        response = model.generate_content(prompt)
        
        # 4. JSON 파싱
        # response_mime_type을 application/json으로 설정했으므로 바로 파싱 가능
        response_data = json.loads(response.text)
        
        # 5. DB에 있는 정확한 좌표와 이미지 데이터로 덮어씌우기 (환각 방지 안전장치)
        # LLM이 좌표나 이미지를 헷갈릴 수 있으므로, 응답 메시지만 LLM 것을 쓰고 좌표는 DB 원본을 사용
        safe_places = []
        for db_place in course_data["places"]:
            safe_places.append({
                "name": db_place["title"],
                "lat": float(db_place["mapy"]),
                "lng": float(db_place["mapx"]),
                "image_url": db_place["firstimage"],
                "address": db_place["addr1"]
            })
            
        return ChatResponse(
            message=response_data.get("message", "추천 코스를 준비했습니다!"),
            places=safe_places
        )

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="코스 추천 중 오류가 발생했습니다.")

# 서버 실행 (터미널 명령어): uvicorn prompt:app --reload