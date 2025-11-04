from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.models import HotelImage
from app.db.schemas import (HotelImageOutSchema, HotelImageCreateSchema,
                            HotelImageDetailSchema, HotelImageUpdateSchema)
from app.db.database import SessionLocal
from typing import List


hotel_image_router = APIRouter(prefix="/hotel-image", tags=["HotelImage"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@hotel_image_router.post("/", response_model=HotelImageOutSchema)
async def create_hotel_image(hotel_image_data: HotelImageCreateSchema, db: Session = Depends(get_db)):
    new_hotel_image = HotelImage(hotel_image=hotel_image_data.hotel_image, hotel_id=hotel_image_data.hotel_id)
    db.add(new_hotel_image)
    db.commit()
    db.refresh(new_hotel_image)
    return new_hotel_image


@hotel_image_router.get("/", response_model=List[HotelImageOutSchema])
async def list_hotel_images(db: Session = Depends(get_db)):
    return db.query(HotelImage).all()


@hotel_image_router.get("/{hotel_image_id}/", response_model=HotelImageDetailSchema)
async def detail_hotel_image(hotel_image_id: int, db: Session = Depends(get_db)):
    hotel_image_db = db.query(HotelImage).filter(HotelImage.id == hotel_image_id).first()
    if not hotel_image_db:
        raise HTTPException(status_code=404, detail="Hotel Image not found")
    return hotel_image_db


@hotel_image_router.put("/{hotel_image_id}/", response_model=HotelImageOutSchema)
async def update_hotel_image(hotel_image_data: HotelImageUpdateSchema, hotel_image_id: int, db: Session = Depends(get_db)):
    hotel_image_db = db.query(HotelImage).filter(HotelImage.id == hotel_image_id).first()
    if not hotel_image_db:
        raise HTTPException(status_code=404, detail="Hotel Image not found")
    hotel_image_db.hotel_image = hotel_image_data.hotel_image
    hotel_image_db.hotel_id = hotel_image_data.hotel_id
    db.commit()
    db.refresh(hotel_image_db)
    return hotel_image_db


@hotel_image_router.delete("/{hotel_image_id}/")
async def delete_hotel_image(hotel_image_id: int, db: Session = Depends(get_db)):
    hotel_image_db = db.query(HotelImage).filter(HotelImage.id == hotel_image_id).first()
    if not hotel_image_db:
        raise HTTPException(status_code=404, detail="Hotel Image not found")
    db.delete(hotel_image_db)
    db.commit()
    return {"message": f"Hotel Image {hotel_image_id} deleted successfully"}
