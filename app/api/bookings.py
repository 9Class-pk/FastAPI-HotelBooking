from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.models import Booking
from app.db.schemas import BookingSchema
from app.db.database import SessionLocal



booking_router = APIRouter(prefix="/bookings", tags=["Bookings"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@booking_router.post("/", response_model=BookingSchema)
async def create_booking(booking_data: BookingSchema, db: Session = Depends(get_db)):
    new_booking = Booking(**booking_data.dict())

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


@booking_router.get("/", response_model=List[BookingSchema])
async def list_booking(db: Session = Depends(get_db)):
    return db.query(Booking).all()


@booking_router.get("/{booking_id}/", response_model=BookingSchema)
async def detail_booking(booking_id: int, db: Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking_db:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking_db


@booking_router.put("/{booking_id}/", response_model=BookingSchema)
async def update_booking(booking_data: BookingSchema, booking_id: int, db: Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking_db:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking_db.check_in = booking_data.check_in
    booking_db.check_out = booking_data.check_out
    booking_db.booking_status = booking_data.booking_status
    db.commit()
    db.refresh(booking_db)
    return booking_db


@booking_router.delete("/{booking_id}/")
async def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking_db:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking_db)
    db.commit()
    return {"message": f"Booking {booking_id} deleted successfully"}
