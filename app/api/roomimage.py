from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.models import RoomImage
from app.db.schemas import RoomImageSchema
from app.db.database import SessionLocal

room_image_router = APIRouter(prefix="/room-image", tags=["RoomImage"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@room_image_router.post("/", response_model=RoomImageSchema)
async def create_room_image(room_image_data: RoomImageSchema, db: Session = Depends(get_db)):
    new_room_image = RoomImage(room_image=room_image_data.room_image, room_id=room_image_data.room_id)
    db.add(new_room_image)
    db.commit()
    db.refresh(new_room_image)
    return new_room_image


@room_image_router.get("/", response_model=List[RoomImageSchema])
async def list_room_images(db: Session = Depends(get_db)):
    return db.query(RoomImage).all()


@room_image_router.get("/{room_image_id}/", response_model=RoomImageSchema)
async def detail_room_image(room_image_id: int, db: Session = Depends(get_db)):
    room_image_db = db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if not room_image_db:
        raise HTTPException(status_code=404, detail="Room Image not found")
    return room_image_db


@room_image_router.put("/{room_image_id}/", response_model=RoomImageSchema)
async def update_room_image(room_image_data: RoomImageSchema, room_image_id: int, db: Session = Depends(get_db)):
    room_image_db = db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if not room_image_db:
        raise HTTPException(status_code=404, detail="Room Image not found")
    room_image_db.room_image = room_image_data.room_image
    room_image_db.room_id = room_image_data.room_id
    db.commit()
    db.refresh(room_image_db)
    return room_image_db


@room_image_router.delete("/{room_image_id}/")
async def delete_room_image(room_image_id: int, db: Session = Depends(get_db)):
    room_image_db = db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if not room_image_db:
        raise HTTPException(status_code=404, detail="Room Image not found")
    db.delete(room_image_db)
    db.commit()
    return {"message": f"Room Image {room_image_id} deleted successfully"}
