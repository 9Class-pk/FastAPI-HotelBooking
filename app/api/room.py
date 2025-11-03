from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.models import Room
from app.db.schemas import RoomSchema
from app.db.database import SessionLocal

room_router = APIRouter(prefix="/room", tags=["Room"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@room_router.post("/", response_model=RoomSchema)
async def create_room(room_data: RoomSchema, db: Session = Depends(get_db)):
    new_room = Room(**room_data.dict())

    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


@room_router.get("/", response_model=List[RoomSchema])
async def list_room(db: Session = Depends(get_db)):
    return db.query(Room).all()


@room_router.get("/{room_id}/", response_model=RoomSchema)
async def get_detail(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@room_router.put("/{room_id}/", response_model=RoomSchema)
async def update_room(room_data: RoomSchema, room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    room.room_number = room_data.room_number
    room.room_type = room_data.room_type
    room.room_status = room_data.room_status
    room.room_description = room_data.room_description
    room.price = room_data.price
    room.max_guests = room_data.max_guests
    room.hotel_id = room_data.hotel_id

    db.commit()
    db.refresh(room)
    return room


@room_router.delete("/{room_id}/")
async def delete_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    db.delete(room)
    db.commit()
    return {"message": f"Room {room_id} deleted successfully"}