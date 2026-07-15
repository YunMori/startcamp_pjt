import os
from typing import List, Optional
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. 가벼운 로컬 SQLite 연동 세팅
DATABASE_URL = "sqlite:///./localhub_dev.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 임시 Post 테이블 정의
class PostModel(Base):
    __tablename__ = "temp_posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String, default="익명")
    password = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

# 2. API 스키마 정의
class ChatRequest(BaseModel):
    message: str

class PlaceInfo(BaseModel):
    name: str
    lat: float
    lng: float

class ChatResponse(BaseModel):
    message: str
    places: List[PlaceInfo]

app = FastAPI(title="LocalHub Step 1 Mock Server")

# CORS 전체 허용 (FE 개발 편의용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "LocalHub FastAPI Server가 정상 작동 중입니다!"}

# FE 지도 시각화 테스트를 위한 Mock 챗봇 API
@app.post("/api/chat", response_model=ChatResponse)
def mock_chat_with_ai(chat_req: ChatRequest):
    """
    Step 1 단계에서 FE 개발자분들이 지도 API 및 동선 그리기를 
    먼저 연동하고 테스트할 수 있도록 제공하는 Mock API입니다.
    """
    print(f"받은 메시지: {chat_req.message}")
    return ChatResponse(
        message="[Mock] 대전의 필수 데이트 코스를 추천합니다! 먼저 성심당에서 맛있는 빵을 구매한 뒤, 한밭수목원으로 이동하여 산책을 즐겨보세요.",
        places=[
            PlaceInfo(name="성심당 본점", lat=36.3278, lng=127.4273),
            PlaceInfo(name="한밭수목원", lat=36.3688, lng=127.3892)
        ]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)