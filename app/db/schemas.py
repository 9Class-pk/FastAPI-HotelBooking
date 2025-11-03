from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from app.db.models import RoomStatus, BookingStatus, RoomType, RoleChoices
from datetime import datetime, date



class CountryOutSchema(BaseModel):
    id: int
    country_name: str
    country_image: str

    class Config:
        from_attributes = True


class CountryCreateSchema(BaseModel):
    country_name: str
    country_image: str

    class Config:
        from_attributes = True


class CountryUpdateSchema(BaseModel):
    country_name: str
    country_image: str

    class Config:
        from_attributes = True


class UserProfileSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    user_name: str
    email: EmailStr
    age: Optional[int] = None
    phone_number: Optional[str]
    role: RoleChoices
    created_date: datetime
    password: str

    class Config:
        from_attributes = True


class CityBase(BaseModel):
    city_name: str
    city_image: Optional[str] = None

class CityCreate(CityBase):
    pass

class CityOut(CityBase):
    id: int

    class Config:
        from_attributes = True


class ServiceSchema(BaseModel):
    id: int
    service_name: str
    service_image: str

    class Config:
        from_attributes = True


class HotelSchema(BaseModel):
    id: int
    hotel_name: str
    stars: Optional[int] = Field(None, gt=0, lt=6)
    postal_index: str
    description: str
    street: str
    country_id: int
    city_id: int
    owner_id: int

class Config:
        from_attributes = True


class HotelImageSchema(BaseModel):
    id: int
    hotel_image: str

    class Config:
        from_attributes = True


class RoomSchema(BaseModel):
    id: int
    room_number: str
    room_type: RoomType
    room_status: RoomStatus
    room_description: str
    price: float
    max_guests: int

    class Config:
        from_attributes = True


class RoomImageSchema(BaseModel):
    id:int
    room_image: str

    class Config:
        from_attributes = True


class BookingSchema(BaseModel):
    id:int
    check_in: date
    check_out: date
    booking_status: BookingStatus
    hotel_id: int
    room_id: int
    user_id: int

    class Config:
        from_attributes = True


class ReviewSchema(BaseModel):
    id: int
    stars: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None

    class Config:
        from_attributes = True


class FavouriteSchema(BaseModel):
    id: int
    user_id: int


    class Config:
        from_attributes = True


class FavouriteItemSchema(BaseModel):
    id: int
    favourite_id: int
    hotel_id: int

    class Config:
        from_attributes = True