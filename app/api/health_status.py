from fastapi import APIRouter
from starlette.responses import HTMLResponse
from app.db.database import SessionLocal


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


health_routers = APIRouter(prefix="/health/home", tags=["Health"])


@health_routers.get("/", response_class=HTMLResponse)
async def home():
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

@health_routers.get("/health")
async def health_check():
    return {
        "status": "ok",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }
