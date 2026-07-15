import os
from typing import List, Optional
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# 1. 🌟 절대 경로 기반 DB 설정 (축제 데이터가 들어있는 DB와 안전하게 연동)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "db", "festival.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. 🌟 이전에 설계한 스키마를 SQLAlchemy 모델로 정의
class FestivalModel(Base):
    __tablename__ = "festivals"
    content_id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    addr1 = Column(String, nullable=False)
    addr2 = Column(String, nullable=True)
    tel = Column(String, nullable=True)
    first_image = Column(String, nullable=True)
    first_image2 = Column(String, nullable=True)
    map_x = Column(Float, nullable=False)  # 경도 (mapx)
    map_y = Column(Float, nullable=False)  # 위도 (mapy)

class ReviewModel(Base):
    __tablename__ = "reviews"
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    content_id = Column(String, ForeignKey("festivals.content_id", ondelete="CASCADE"), nullable=False)
    nickname = Column(String, nullable=False)
    password = Column(String, nullable=False)  # 수정/삭제용 비밀번호
    rating = Column(Integer, nullable=False)   # 별점 (1~5)
    content = Column(Text, nullable=False)     # 리뷰 내용

# 테이블 스키마 반영
Base.metadata.create_all(bind=engine)

# DB 세션 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. Pydantic API 스키마 정의
class ChatRequest(BaseModel):
    message: str

class PlaceInfo(BaseModel):
    name: str
    lat: float
    lng: float

class ChatResponse(BaseModel):
    message: str
    places: List[PlaceInfo]

# 리뷰 작성을 위한 입력 검증용 스키마
class ReviewCreate(BaseModel):
    content_id: str
    nickname: str
    password: str = Field(..., min_length=1, description="수정/삭제용 비밀번호")
    rating: int = Field(..., ge=1, le=5, description="별점 (1점 ~ 5점)")
    content: str

# 리뷰 조회를 위한 출력용 스키마
class ReviewResponse(BaseModel):
    review_id: int
    content_id: str
    nickname: str
    rating: int
    content: str

    class Config:
        from_attributes = True


# 비밀번호 검증용 스키마
class PasswordCheck(BaseModel):
    password: str = Field(..., min_length=1)


# 리뷰 수정 입력 스키마 (부분 업데이트 허용)
class ReviewUpdate(BaseModel):
    nickname: Optional[str] = None
    password: str = Field(..., min_length=1, description="현재 비밀번호 (수정/삭제 권한 확인용)")
    rating: Optional[int] = Field(None, ge=1, le=5)
    content: Optional[str] = None
    # 프론트에서 'text'라는 필드를 보낼 가능성 대비
    text: Optional[str] = None


app = FastAPI(title="LocalHub Step 1 Server")

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

# AI 팀원 및 프론트엔드 테스트를 위한 Mock 챗봇 API
@app.post("/api/chat", response_model=ChatResponse)
def mock_chat_with_ai(chat_req: ChatRequest):
    print(f"받은 메시지: {chat_req.message}")
    return ChatResponse(
        message="[Mock] 대전의 필수 데이트 코스를 추천합니다! 먼저 성심당에서 맛있는 빵을 구매한 뒤, 한밭수목원으로 이동하여 산책을 즐겨보세요.",
        places=[
            PlaceInfo(name="성심당 본점", lat=36.3278, lng=127.4273),
            PlaceInfo(name="한밭수목원", lat=36.3688, lng=127.3892)
        ]
    )

# 4. 🌟 데이터베이스에서 실제 축제 데이터 목록을 조회하는 API
@app.get("/api/festivals")
def get_festivals(db: Session = Depends(get_db)):
    festivals = db.query(FestivalModel).all()
    return {
        "status": "success",
        "count": len(festivals),
        "data": festivals
    }

# 5. 🌟 특정 축제에 익명 리뷰를 작성하는 API (C)
@app.post("/api/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    # 대상 축제가 존재하는지 먼저 확인
    festival = db.query(FestivalModel).filter(FestivalModel.content_id == review.content_id).first()
    if not festival:
        raise HTTPException(status_code=404, detail="존재하지 않는 축제 ID입니다.")
    
    db_review = ReviewModel(
        content_id=review.content_id,
        nickname=review.nickname,
        password=review.password,  # 실서비스 시에는 단방향 해시 암호화를 권장합니다.
        rating=review.rating,
        content=review.content
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# 6. 🌟 특정 축제의 리뷰 목록을 가져오는 API (R)
@app.get("/api/festivals/{content_id}/reviews", response_model=List[ReviewResponse])
def get_festival_reviews(content_id: str, db: Session = Depends(get_db)):
    reviews = db.query(ReviewModel).filter(ReviewModel.content_id == content_id).all()
    return reviews


# 비밀번호 검증 엔드포인트 — 수정/삭제 전 비밀번호 확인용
@app.post("/api/reviews/{review_id}/verify")
def verify_review_password(review_id: int, payload: PasswordCheck, db: Session = Depends(get_db)):
    review = db.query(ReviewModel).filter(ReviewModel.review_id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="존재하지 않는 리뷰입니다.")
    if review.password != payload.password:
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다.")
    return {"status": "success"}


# 리뷰 수정 (비밀번호 확인 필요)
@app.put("/api/reviews/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, payload: ReviewUpdate, db: Session = Depends(get_db)):
    review = db.query(ReviewModel).filter(ReviewModel.review_id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="존재하지 않는 리뷰입니다.")
    # 비밀번호 검증
    if review.password != payload.password:
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다.")

    if payload.nickname is not None:
        review.nickname = payload.nickname
    if payload.rating is not None:
        review.rating = payload.rating
    # 프론트에서 'text'를 보낼 수 있으므로 우선순위를 둠
    if payload.content is not None:
        review.content = payload.content
    elif payload.text is not None:
        review.content = payload.text

    db.add(review)
    db.commit()
    db.refresh(review)
    return review


# 리뷰 삭제 (비밀번호 필요)
@app.delete("/api/reviews/{review_id}")
def delete_review(review_id: int, payload: PasswordCheck, db: Session = Depends(get_db)):
    review = db.query(ReviewModel).filter(ReviewModel.review_id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="존재하지 않는 리뷰입니다.")
    if review.password != payload.password:
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다.")

    db.delete(review)
    db.commit()
    return {"status": "deleted"}


if __name__ == "__main__":
    import uvicorn
    # ⚠️ [수정] 파일명이 app.py로 바뀌었으므로 "main:app"에서 "app:app"으로 변경해 줍니다!
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)