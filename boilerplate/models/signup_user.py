# coding=utf-8
import datetime
import bcrypt

from flask_restplus import fields
from boilerplate.utils.random_string import random_string
from boilerplate.utils.enum_model import Gender
from boilerplate.models import db, TimestampMixin

__author__ = 'ThucNC'


class Signup_user(db.Model, TimestampMixin):
    """
    Contains information of temporary sign up users table
    """
    __tablename__ = 'signup_users'

    def __init__(self, **kwargs):
        """
        Support direct initialization
        :param kwargs:
        """
        for k, v in kwargs.items():
            setattr(self, k, v)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(191), nullable=False)
    username = db.Column(db.String(191), nullable=False)
    fullname = db.Column(db.String(191), nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=True,default=Gender.male)
    password_hash = db.Column(db.String(100))
    active_token = db.Column(db.String(512), nullable=False, default= bcrypt.hashpw(random_string().encode('utf-8'), bcrypt.gensalt()))
    token_expire_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now() + datetime.timedelta(minutes=30))
