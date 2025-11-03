from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.models import Review
from app.db.schemas import ReviewSchema
from app.db.database import SessionLocal

review_router = APIRouter(prefix="/review", tags=["Review"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@review_router.post("/", response_model=ReviewSchema)
async def create_review(review_data: ReviewSchema, db: Session = Depends(get_db)):
    new_review = Review(**review_data.dict())

    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@review_router.get("/", response_model=List[ReviewSchema])
async def list_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()


@review_router.get("/{review_id}/", response_model=ReviewSchema)
async def detail_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=404, detail="Review not found")
    return review_db


@review_router.put("/{review_id}/", response_model=ReviewSchema)
async def update_review(review_data: ReviewSchema, review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=404, detail="Review not found")
    review_db.stars = review_data.stars
    review_db.comment = review_data.comment
    db.commit()
    db.refresh(review_db)
    return review_db


@review_router.delete("/{review_id}/")
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review_db)
    db.commit()
    return {"message": f"Review {review_id} deleted successfully"}
