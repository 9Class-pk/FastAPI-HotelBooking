from datetime import datetime
from fastapi import APIRouter
from app.db.database import SessionLocal


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


health_routers = APIRouter(prefix="/health", tags=["Health"])


@health_routers.get("/health/")
async def health_check():
    return {
        "status": "ok",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }
