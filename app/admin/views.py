from sqladmin import ModelView
from sqlalchemy.testing.pickleable import User

from app.db.models import *



class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name, UserProfile.role]


class CountryAdmin(ModelView, model=Country):
    column_list = [Country.country_name, Country.country_image]


class AuthAdmin(ModelView, model=Auth):
    column_list = [Auth.first_name, Auth.last_name]
