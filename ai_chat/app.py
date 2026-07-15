import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from dotenv import load_dotenv

# 최신 구글 공식 패키지 임포트
from google import genai
from google.genai import types

# 💡 공통 비즈니스 로직 및 프롬프트 템플릿 모듈 재사용
from ai_chat.user_type_select import get_course_data, generate_llm_prompt

# 환경변수 로드
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인해주세요.")

# 새로운 클라이언트 초기화
client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI(title="LocalHub 데이트 코스 챗봇 API")

# ==========================================
# 1. Pydantic 스키마 정의
# ==========================================
class UserAnswers(BaseModel):
    mobility: str = Field(..., description="이동수단 (walk 또는 car)")
    preference: str = Field(..., description="코스 ID (예: course_A)")
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
# 2. FastAPI 엔드포인트
# ==========================================
@app.post("/api/chat", response_model=ChatResponse)
async def generate_dating_course(user_answers: UserAnswers):
    try:
        # 1. 공통 모듈 함수로 DB(혹은 메모리 풀) 데이터 조회
        course_data = get_course_data(user_answers.preference)
        
        # 2. 공통 프롬프트 생성기 호출 및 간결한 지시사항 주입
        prompt = generate_llm_prompt(course_data)
        prompt += """
        
        [출력 지시사항]
        반드시 아래 JSON 형식으로만 출력해. 백틱(```json)이나 다른 설명은 절대 포함하지 마.
        {
            "message": "사용자님에게 추천 코스를 안내해 드립니다! ... (각 장소의 매력을 연결하여 로맨틱한 스토리텔링 작성)"
        }
        """

        # 3. 최신 Gemini API 호출
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                response_mime_type="application/json",
            )
        )
        
        # 4. 안전한 결과 조립 (백엔드 좌표 맵핑)
        response_data = json.loads(response.text)
        
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

# 서버 실행 (터미널): uvicorn app:app --reload