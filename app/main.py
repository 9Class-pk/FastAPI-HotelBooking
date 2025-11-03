import uvicorn
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, APIRouter

from app.api.soical_auth import social_router
from app.db.database import  SessionLocal
from app.api import (user, country, city, hotel, hotelimage,
                     favourite, favouriteitem, review, room,
                     roomimage, service, bookings, health_status,
                     auth, soical_auth)
#from app.api import
#from app.admin.setup import setup_admin
from starlette.middleware.sessions import SessionMiddleware
from app.middlewares.middleware import LoggingMiddleware
import os
from fastapi.responses import HTMLResponse


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


booking = FastAPI()

booking.include_router(user.user_router)
booking.include_router(auth.auth_router)
booking.include_router(soical_auth.social_router)
booking.include_router(country.country_router)
booking.include_router(city.city_router)
booking.include_router(hotel.hotel_router)
booking.include_router(hotelimage.hotel_image_router)
booking.include_router(room.room_router)
booking.include_router(roomimage.room_image_router)
booking.include_router(bookings.booking_router)
booking.include_router(service.service_router)
booking.include_router(review.review_router)
booking.include_router(favourite.favourite_router)
booking.include_router(favouriteitem.favouriteitem_router)
booking.include_router(health_status.health_routers)


#oauth middlewares
booking.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")
booking.add_middleware(LoggingMiddleware)



if __name__ == '__main__':
    uvicorn.run(booking, host='127.0.0.1', port=8001)