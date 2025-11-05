from .views import *
from fastapi import FastAPI
from sqladmin import Admin
from app.db.database import engine


def setup_admin(booking: FastAPI):
    admin = Admin(booking, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CountryAdmin)
    admin.add_view(AuthAdmin)