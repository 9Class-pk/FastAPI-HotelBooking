from datetime import datetime, date
from sqlalchemy import (Integer, String, Enum, DateTime, DECIMAL,
                        Text, ForeignKey, Column, Table, Date)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from app.db.database import Base
from enum import Enum as PyEnum
from decimal import Decimal


hotel_service = Table(
    'hotel_service',
    Base.metadata,
    Column('hotel_id', ForeignKey('hotel.id'), primary_key=True),
    Column('service_id', ForeignKey('service.id'), primary_key=True)
)


class RoleChoices(str, PyEnum):
    admin = 'admin'
    owner = 'owner'
    client = 'client'


class RoomType(str, PyEnum):
    lux = 'lux'
    junior_lux = 'junior_lux'
    family = 'family'
    single = 'single'


class RoomStatus(str, PyEnum):
    available = 'available'
    booked = 'booked'
    occupied = 'occupied'



class BookingStatus(str, PyEnum):
    pending = 'pending'
    confirmed = 'confirmed'
    cancelled = 'cancelled'
    completed = 'completed'


class Country(Base):
    __tablename__ = 'country'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, index=True)
    country_name: Mapped[String] = mapped_column(String(16), unique=True, index=True )
    country_image: Mapped[String] = mapped_column(String, nullable=True)

    countries: Mapped[List['Hotel']] =relationship('Hotel', back_populates='country')


class UserProfile(Base):
    __tablename__ = 'userprofile'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    user_name: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), default=RoleChoices.client)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    password: Mapped[str] = mapped_column(String, nullable=False)

    owners: Mapped[List['Hotel']] = relationship('Hotel', back_populates='owner',
                                           cascade='all, delete-orphan')

    user_bookings: Mapped[List['Booking']] = relationship('Booking', back_populates='user',
                                                          cascade='all, delete-orphan')

    user_reviews: Mapped[List['Review']] = relationship('Review', back_populates='user',
                                                        cascade='all, delete-orphan')

    user_favourites: Mapped[List['Favourite']] = relationship('Favourite', back_populates='user',
                                                              cascade='all, delete-orphan')

    refresh_tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user',
                                                                cascade='all, delete-orphan')


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, index=True)
    city_name: Mapped[String] = mapped_column(String(16), index=True)
    city_image: Mapped[String] = mapped_column(String, nullable=True)

    cities: Mapped[List['Hotel']] = relationship('Hotel', back_populates='city')



class Service(Base):
    __tablename__ = 'service'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    service_name: Mapped[String] = mapped_column(String(32))
    service_image: Mapped[String] = mapped_column(String, nullable=True)

    hotels: Mapped[List['Hotel']] = relationship('Hotel',
                                                    secondary=hotel_service,
                                                    back_populates='services')


class Hotel(Base):
    __tablename__ = 'hotel'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    hotel_name: Mapped[str] = mapped_column(String(64))
    stars: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    street: Mapped[str] = mapped_column(String(100), nullable=True)
    postal_index: Mapped[str] = mapped_column(String(32), nullable=True)
    description: Mapped[str] = mapped_column(Text)

    country_id: Mapped[int] = mapped_column(ForeignKey('country.id'))
    country: Mapped[Country] = relationship('Country', back_populates='countries')

    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    city: Mapped[City] = relationship('City', back_populates='cities')

    owner_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    owner: Mapped[UserProfile] = relationship('UserProfile', back_populates='owners')

    services: Mapped[List[Service]] = relationship('Service',
                                                   secondary=hotel_service, back_populates='hotels')

    hotel_images: Mapped[List['HotelImage']] = relationship('HotelImage', back_populates='hotel',
                                                            cascade='all, delete-orphan')

    hotel_bookings: Mapped[List['Booking']] = relationship('Booking', back_populates='hotel',
                                                           cascade='all, delete-orphan')

    #room_bookings: Mapped[List['Booking']] = relationship('Booking', back_populates='hotel',
                                                          #cascade='all, delete-orphan')

    hotel_reviews: Mapped[List['Review']] = relationship('Review', back_populates='hotel', cascade=
                                                         'all, delete-orphan')

    hotel_favourites: Mapped[List['FavouriteItem']] = relationship('FavouriteItem', back_populates='hotel',
                                                                   cascade='all, delete-orphan')


class HotelImage(Base):
    __tablename__ ='hotel_image'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    hotel_image: Mapped[str] = mapped_column(String, nullable=True)

    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    hotel: Mapped[Hotel] = relationship('Hotel', back_populates='hotel_images')


class Room(Base):
    __tablename__ = 'room'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    room_number: Mapped[str] = mapped_column(String(10))
    room_type: Mapped[RoomType] = mapped_column(Enum(RoomType), default=RoomType.single)
    room_status: Mapped[RoomStatus] = mapped_column(Enum(RoomStatus), default=RoomStatus.available)
    room_description: Mapped[str] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10,2))
    max_guests: Mapped[int] = mapped_column(Integer, nullable=False)

    room_images: Mapped[List['RoomImage']] = relationship('RoomImage', back_populates='room',
                                                          cascade='all, delete-orphan')

    room_bookings: Mapped[List['Booking']] = relationship('Booking', back_populates='room',
                                                          cascade='all, delete-orphan')


class RoomImage(Base):
    __tablename__ = 'room_image'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    room_image: Mapped[str] = mapped_column(String, nullable=True)

    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    room: Mapped[Room] = relationship('Room', back_populates='room_images')


class Booking(Base):
    __tablename__ = 'booking'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    check_in: Mapped[date] = mapped_column(Date, nullable=True)
    check_out: Mapped[date] = mapped_column(Date, nullable=True)
    booking_status: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus),
                                                         default=BookingStatus.pending)

    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    hotel: Mapped[Hotel] = relationship('Hotel', back_populates='hotel_bookings')

    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    room: Mapped[Room] = relationship('Room', back_populates='room_bookings')

    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    user: Mapped[UserProfile] = relationship('UserProfile', back_populates='user_bookings')


class Review(Base):
    __tablename__  = 'review'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    stars: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    hotel: Mapped[Hotel] = relationship('Hotel', back_populates='hotel_reviews')

    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    user: Mapped[UserProfile] = relationship('UserProfile', back_populates='user_reviews')


class Favourite(Base):
    __tablename__ = 'favourite'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    user: Mapped[UserProfile] = relationship('UserProfile', back_populates='user_favourites')

    item_favourites: Mapped[List['FavouriteItem']] = relationship('FavouriteItem', back_populates='favourite',
                                                                  cascade='all, delete-orphan')


class FavouriteItem(Base):
    __tablename__ = 'favourite_item'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)

    favourite_id: Mapped[int] = mapped_column(ForeignKey('favourite.id'))
    favourite: Mapped[Favourite] = relationship('Favourite', back_populates='item_favourites')

    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    hotel: Mapped[Hotel] = relationship('Hotel', back_populates='hotel_favourites')



class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    user: Mapped[UserProfile] = relationship('UserProfile', back_populates='refresh_tokens')
    token: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)










