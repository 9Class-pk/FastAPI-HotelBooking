from fastapi import HTTPException, Depends, APIRouter
from app.db.models import UserProfile
from app.db.schemas import UserProfileSchema, UserProfileUpdateSchema
from app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_router = APIRouter(prefix='/user', tags=['UserProfile'])


@user_router.get('/me/', response_model=List[UserProfileSchema])
async def list_user(db: Session = Depends(get_db)):

    return db.query(UserProfile).all()


@user_router.get('/me/{user_id}/', response_model=UserProfileSchema)
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user_db


@user_router.put('/{user_id}/', response_model=UserProfileSchema)
async def update_user(user_data: UserProfileUpdateSchema, user_id: int, db: Session=Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()

    if user_db is None:
        raise HTTPException(status_code=404, detail='User not found')

    for user_key, user_value in user_data.dict().items():
        setattr(user_db, user_key, user_value)

    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@user_router.delete('/me/{user_id}/')
async def delete_user(user_id: int, db: Session=Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()

    if user_db is None:
        raise HTTPException(status_code=404, detail='User not found')
    db.delete(user_db)
    db.commit()
    return {'message': f'User {user_id} deleted successfully'}