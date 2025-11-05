import uvicorn
from fastapi import FastAPI, HTTPException, Depends, APIRouter
#
#from app.api.soical_auth import social_router
#from app.db.database import  SessionLocal
##from app.api import (user, country, city, hotel, hotelimage,
#                     favourite, favouriteitem, review, room,
#                     roomimage, service, bookings, health_status,
#                     auth, soical_auth)
#from app.admin.setup import setup_admin
#from starlette.middleware.sessions import SessionMiddleware
#from app.middlewares.middleware import LoggingMiddleware
#import os
import uvicorn
from fastapi.responses import HTMLResponse
from app.routers.router import *
from app.db.database import  SessionLocal


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#booking = FastAPI() если в роутере есть booking, то не нужно создать booking

@booking.get("/", response_class=HTMLResponse)
async def Home():
    return """
    <html>
        <head>
            <title>Booking</title>
        </head>
        <body>
            <h1>Salam Aleikum</h1>
            <p>Документация: <a href="/docs">Swagger</a></p>
        </body>
    </html>
    """


if __name__ == '__main__':
    uvicorn.run(booking, host='127.0.0.1', port=8001)