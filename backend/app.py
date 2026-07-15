import os
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text, Column, Integer, String, Text, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from recommend import (
    score_courses,
    get_course_data,
    generate_course_story,
    generate_free_reply,
)

# 1. 🌟 절대 경로 기반 DB 설정 (축제 데이터가 들어있는 DB와 안전하게 연동)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "db", "festival.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. 🌟 SQLAlchemy 모델 정의
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
    # 추천 코스 ID(course_A~E) 등 임의 대상에 리뷰를 달 수 있도록 축제 FK 없이 문자열 키만 유지
    content_id = Column(String, nullable=False, index=True)
    nickname = Column(String, nullable=False)
    password = Column(String, nullable=False)  # 수정/삭제용 비밀번호
    rating = Column(Integer, nullable=False)   # 별점 (1~5)
    content = Column(Text, nullable=False)     # 리뷰 내용
    created_at = Column(String, nullable=True) # 작성일 (YYYY.MM.DD)

# 테이블 스키마 반영
Base.metadata.create_all(bind=engine)

# 기존 DB에 created_at 컬럼이 없으면 추가 (팀원이 만든 축제 데이터 보존을 위해 DB 재생성 대신 마이그레이션)
with engine.connect() as conn:
    review_columns = [row[1] for row in conn.execute(text("PRAGMA table_info(reviews)"))]
    if review_columns and "created_at" not in review_columns:
        conn.execute(text("ALTER TABLE reviews ADD COLUMN created_at VARCHAR"))
        conn.commit()

# DB 세션 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. Pydantic API 스키마 정의

# ---- 추천/챗봇 ----
class RecommendRequest(BaseModel):
    mobility: str = Field(..., description="이동수단 (walk 또는 car)")
    festival: bool = Field(False, description="축제 참여 희망 여부")
    q1: str = Field(..., description="분위기 성향 (1~3)")
    q2: str = Field(..., description="활동성 성향 (1~3)")
    q3: str = Field(..., description="식사/음주 성향 (1~3)")
    q4: str = Field(..., description="시간대 성향 (1~3)")
    q5: str = Field(..., description="스트레스 해소 성향 (1~3)")

class PlaceInfo(BaseModel):
    name: str
    lat: float
    lng: float
    image_url: str = ""
    address: str = ""

class RecommendedCourse(BaseModel):
    id: str
    name: str
    spots: List[PlaceInfo]

class RecommendResponse(BaseModel):
    courses: List[RecommendedCourse]

class CourseChatRequest(BaseModel):
    course_id: str = Field(..., description="추천 코스 ID (예: course_A)")

class ChatResponse(BaseModel):
    message: str
    places: List[PlaceInfo]

class FreeChatMessage(BaseModel):
    role: str  # 'user' | 'assistant'
    content: str

class FreeChatRequest(BaseModel):
    messages: List[FreeChatMessage]

class FreeChatResponse(BaseModel):
    reply: str

# ---- 리뷰 (프론트 계약: id / text / date 필드) ----
class ReviewCreate(BaseModel):
    nickname: str
    password: str = Field(..., min_length=1, description="수정/삭제용 비밀번호")
    rating: int = Field(..., ge=1, le=5, description="별점 (1점 ~ 5점)")
    text: str

class ReviewResponse(BaseModel):
    id: int
    nickname: str
    rating: int
    text: str
    date: str

class PasswordCheck(BaseModel):
    password: str = Field(..., min_length=1)

class ReviewUpdate(BaseModel):
    nickname: Optional[str] = None
    password: str = Field(..., min_length=1, description="현재 비밀번호 (수정 권한 확인용)")
    new_password: Optional[str] = Field(None, description="변경할 새 비밀번호 (미입력 시 유지)")
    rating: Optional[int] = Field(None, ge=1, le=5)
    text: Optional[str] = None


def to_review_response(review: ReviewModel) -> ReviewResponse:
    return ReviewResponse(
        id=review.review_id,
        nickname=review.nickname,
        rating=review.rating,
        text=review.content,
        date=review.created_at or "",
    )


app = FastAPI(title="LocalHub API Server")

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


# ==========================================
# 추천 / 챗봇 API
# ==========================================

# 설문 답변 → 점수 알고리즘 → 상위 3개 코스 추천
@app.post("/api/recommend", response_model=RecommendResponse)
def recommend_courses(req: RecommendRequest):
    ranked_ids = score_courses(req.model_dump())
    courses = []
    for course_id in ranked_ids:
        course_data = get_course_data(course_id)
        courses.append(RecommendedCourse(
            id=course_id,
            name=course_data["name"],
            spots=[
                PlaceInfo(
                    name=p["title"], lat=p["lat"], lng=p["lng"],
                    image_url=p["firstimage"], address=p["addr1"],
                )
                for p in course_data["places"]
            ],
        ))
    return RecommendResponse(courses=courses)


# 선택한 코스에 대한 Gemini 스토리텔링 + 지도 핀 좌표
@app.post("/api/chat", response_model=ChatResponse)
def course_chat(req: CourseChatRequest):
    course_data = get_course_data(req.course_id)
    if not course_data["places"]:
        raise HTTPException(status_code=404, detail="존재하지 않는 코스 ID입니다.")
    message = generate_course_story(course_data)
    return ChatResponse(
        message=message,
        places=[
            PlaceInfo(
                name=p["title"], lat=p["lat"], lng=p["lng"],
                image_url=p["firstimage"], address=p["addr1"],
            )
            for p in course_data["places"]
        ],
    )


# 자유 채팅 (프론트 chatApi.js 계약: {messages} → {reply})
@app.post("/chat", response_model=FreeChatResponse)
def free_chat(req: FreeChatRequest):
    reply = generate_free_reply([m.model_dump() for m in req.messages])
    if reply is None:
        reply = "지금은 자유 대화가 잠시 어려워요 🥲 위의 선택지 버튼으로 코스를 추천받아 보세요!"
    return FreeChatResponse(reply=reply)


# ==========================================
# 축제 데이터 API
# ==========================================
@app.get("/api/festivals")
def get_festivals(db: Session = Depends(get_db)):
    festivals = db.query(FestivalModel).all()
    return {
        "status": "success",
        "count": len(festivals),
        "data": festivals,
    }


# ==========================================
# 리뷰 CRUD API (코스 ID 기준, 프론트 reviewApi.js 계약)
# ==========================================

# 특정 코스의 리뷰 목록 (R)
@app.get("/courses/{course_id}/reviews", response_model=List[ReviewResponse])
def get_course_reviews(course_id: str, db: Session = Depends(get_db)):
    reviews = (
        db.query(ReviewModel)
        .filter(ReviewModel.content_id == course_id)
        .order_by(ReviewModel.review_id.desc())
        .all()
    )
    return [to_review_response(r) for r in reviews]


# 특정 코스에 익명 리뷰 작성 (C)
@app.post("/courses/{course_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(course_id: str, review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = ReviewModel(
        content_id=course_id,
        nickname=review.nickname,
        password=review.password,  # 실서비스 시에는 단방향 해시 암호화를 권장합니다.
        rating=review.rating,
        content=review.text,
        created_at=datetime.now().strftime("%Y.%m.%d"),
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return to_review_response(db_review)


# 비밀번호 검증 — 수정/삭제 전 비밀번호 확인용
@app.post("/reviews/{review_id}/verify")
def verify_review_password(review_id: int, payload: PasswordCheck, db: Session = Depends(get_db)):
    review = db.query(ReviewModel).filter(ReviewModel.review_id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="존재하지 않는 리뷰입니다.")
    if review.password != payload.password:
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다.")
    return {"status": "success"}


# 리뷰 수정 (U) — password로 권한 확인, new_password가 있으면 비밀번호 변경
@app.put("/reviews/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, payload: ReviewUpdate, db: Session = Depends(get_db)):
    review = db.query(ReviewModel).filter(ReviewModel.review_id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="존재하지 않는 리뷰입니다.")
    if review.password != payload.password:
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다.")

    if payload.nickname is not None:
        review.nickname = payload.nickname
    if payload.rating is not None:
        review.rating = payload.rating
    if payload.text is not None:
        review.content = payload.text
    if payload.new_password:
        review.password = payload.new_password

    db.commit()
    db.refresh(review)
    return to_review_response(review)


# 리뷰 삭제 (D) — 비밀번호 필요
@app.delete("/reviews/{review_id}")
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
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
