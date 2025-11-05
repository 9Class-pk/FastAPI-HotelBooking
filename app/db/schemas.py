from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict
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
    country_image: str = None


class CountryUpdateSchema(BaseModel):
    country_name: Optional[str] = None
    country_image: Optional[str] = None


#/////////////////////////////////////////////////////////
class UserProfileSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    user_name: str
    email: EmailStr
    age: Optional[int] = None
    phone_number: Optional[str] = None
    role: RoleChoices
    created_date: datetime


    class Config:
        from_attributes = True


class UserProfileLoginSchema(BaseModel):
    user_name: EmailStr
    password: str


class UserProfileCreateSchema(BaseModel):
    first_name: str
    last_name: str
    user_name: str = Field(min_length=3, max_length=50)
    role: RoleChoices
    age: Optional[int] = Field(None, ge=16, le=90)
    phone_number: Optional[str] = None
    email: EmailStr
    password: str = Field(min_length=8)


class UserProfileUpdateSchema(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    user_name: Optional[str] = Field(None, min_length=3, max_length=50)
    age: Optional[int] = Field(None, ge=0, le=150)
    phone_number: Optional[str] = None


class AuthBaseSchema(BaseModel):
    first_name: str
    last_name: str
    user_name: str
    email: EmailStr
    age: Optional[int] = None
    phone_number: Optional[str] = None
    role: RoleChoices
    created_date: datetime

class AuthOutSchema(AuthBaseSchema):
    id: int

    class Config:
        from_attributes = True


class AuthCreateSchema(AuthBaseSchema):
    pass


class AuthUpdateSchema(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None,min_length=2, max_length=50)
    user_name: Optional[str] = Field(None, min_length=3, max_length=50)
    email: EmailStr
    age: Optional[int] = Field(None, ge=0, le=150)
    phone_number: Optional[str] = None
    role: RoleChoices
    created_date: datetime


class AuthDeleteSchema(AuthBaseSchema):
    pass


class AuthDetailSchema(AuthBaseSchema):
    pass



class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8)


#////////////////////////////////////////////////
class CityBase(BaseModel):
    city_name: str
    city_image: Optional[str] = None

class CityCreate(CityBase):
    pass

class CityOut(CityBase):
    id: int

    class Config:
        from_attributes = True


#////////////////////////////////////////////////

class ServiceBaseSchema(BaseModel):
    service_name: str
    service_image: str


class ServiceSchema(ServiceBaseSchema):
    id: int

    class Config:
        from_attributes = True

class ServiceCreateSchema(ServiceBaseSchema):
    pass


class ServiceUpdateSchema(ServiceBaseSchema):
    pass


#////////////////////////////////////////////////////////////
class HotelOutSchema(BaseModel):
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


class HotelDetailSchema(BaseModel):
    hotel_name: str
    stars: Optional[int] = Field(None, ge=1, le=5)
    postal_index: str
    description: str
    street: str
    country_id: int
    city_id: int
    owner_id: int

    class Config:
        from_attributes = True


class HotelCreateSchema(BaseModel):
    hotel_name: str = Field(min_length=2, max_length=200)
    stars: Optional[int] = Field(None, ge=1, le=5)
    postal_index: str = Field(min_length=4, max_length=20)
    description: str = Field(min_length=10, max_length=2000)
    street: str = Field(min_length=3, max_length=200)
    country_id: int = Field(gt=0) #для положительных чисел gt=0
    city_id: int = Field(..., gt=0)


class HotelUpdateSchema(BaseModel):
    hotel_name: Optional[str] = Field(None, min_length=2, max_length=200)
    stars: Optional[int] = Field(None, ge=1, le=5)
    postal_index: Optional[str] = Field(None, min_length=4, max_length=20)
    description: Optional[str] = Field(None, min_length=10, max_length=2000)
    street: Optional[str] = Field(None, min_length=3, max_length=200)
    country_id: Optional[int] = Field(None, gt=0)
    city_id: Optional[int] = Field(None, gt=0)


#/////////////////////////////////////////////////////////
class HotelImageBaseSchema(BaseModel):
    hotel_image: str
    hotel_id: int


class HotelImageOutSchema(HotelImageBaseSchema):
    model_config = ConfigDict(from_attributes=True) # удобно для наследование (Pydantic.ver2.0)

    id: int


class HotelImageCreateSchema(BaseModel):
    hotel_image: str
    hotel_id: int


class HotelImageDetailSchema(HotelImageBaseSchema):
    pass


class HotelImageUpdateSchema(BaseModel):
    hotel_image: Optional[str] = None
    hotel_id: Optional[int] = None


#class RoomOutSchema(BaseModel):
#    id: int
#    room_number: str
#    room_type: RoomType
#    room_status: RoomStatus
#    room_description: str
#    price: float
#    max_guests: int
#
#    class Config:
#        from_attributes = True

# важно для наследование
class RoomBaseSchema(BaseModel):
    room_number: str = Field(min_length=1, max_length=20)
    room_type: RoomType
    room_status: RoomStatus
    room_description: str = Field(max_length=1000)
    price: float = Field(gt=0)
    max_guests: int = Field(gt=0, le=100)


class RoomCreateSchema(RoomBaseSchema):
    pass


class RoomDetailSchema(RoomBaseSchema):
    pass


class RoomUpdateSchema(BaseModel):
    room_number: Optional[str] = Field(None, min_length=1, max_length=20)
    room_type: Optional[RoomType] = None
    room_status: Optional[RoomStatus] = None
    room_description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    max_guests:  Optional[int] = Field(None, gt=0, le=10)


class RoomOutSchema(RoomBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


#/////////////////////////////
class RoomImageOutSchema(BaseModel):
    id: int
    room_image : str
    room_id: int

    class Config:
        from_attributes = True


class RoomImageBaseShema(BaseModel):
    room_image: str
    room_id: int


class RoomImageCreateSchema(RoomImageBaseShema):
    pass


class RoomImageDetailSchema(RoomImageBaseShema):
    pass


class RoomImageUpdateSchema(BaseModel):
    room_image: Optional[str] = None
    room_id: Optional[int] = None


#///////////////////////////////////////////////////
class BookingOutSchema(BaseModel):
    id:int
    check_in: date
    check_out: date
    booking_status: BookingStatus
    hotel_id: int
    room_id: int
    user_id: int

    class Config:
        from_attributes = True


class BookingCreateSchema(BaseModel):
    check_in: date
    check_out: date
    booking_status: BookingStatus
    hotel_id: int
    room_id: int
    user_id: int


class BookingDetailSchema(BookingOutSchema):
    pass


class BookingUpdateSchema(BaseModel):
    check_in: Optional[date] = None
    check_out: Optional[date] = None
    booking_status: Optional[BookingStatus] = None
    hotel_id: Optional[int] = None
    room_id: Optional[int] = None


#///////////////////////////////////////////////////
class ReviewOutSchema(BaseModel):
    id: int
    stars: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=1000)
    hotel_id : int
    user_id: int

    class Config:
        from_attributes = True


class ReviewCreateSchema(BaseModel):
    stars: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=1000)
    hotel_id : int
    user_id: int


class ReviewUpdateSchema(BaseModel):
    stars: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=1000)


#////////////////////////////////////////////////////
class FavouriteBaseSchema(BaseModel):
    user_id: int


class FavouriteOutSchema(FavouriteBaseSchema):
    id: int

    class Config:
        from_attributes = True


class FavouriteCreateSchema(FavouriteBaseSchema):
    pass


class FavouriteDetailSchema(FavouriteBaseSchema):
    pass


class FavouriteUpdateSchema(FavouriteBaseSchema):
    pass


#////////////////////////////////////////////////////////
class FavouriteItemBaseSchema(BaseModel):
    favourite_id: int
    hotel_id: int


class FavouriteItemOutSchema(FavouriteItemBaseSchema):
    id: int

    class Config:
        from_attributes = True


class FavouriteItemCreateSchema(FavouriteItemBaseSchema):
   pass


class FavouriteItemDetailSchema(FavouriteItemBaseSchema):
    pass


class FavouriteItemUpdateSchema(FavouriteItemBaseSchema):
    pass