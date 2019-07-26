# coding=utf-8
import datetime
import bcrypt

from boilerplate.utils.random_string import random_string
from boilerplate.utils.enum_model import Role,Gender
from flask_restplus import fields
from boilerplate.models import db, TimestampMixin

__author__ = 'ThucNC'


class User(db.Model, TimestampMixin):
    """
    Contains information of users table
    """
    __tablename__ = 'users'

    def __init__(self, **kwargs):
        """
        Support direct initialization
        :param kwargs:
        """
        for k, v in kwargs.items():
            setattr(self, k, v)



    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(191), nullable=False, unique=True)
    username = db.Column(db.String(191), nullable=False, unique=True)
    fullname = db.Column(db.String(191), nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=True,default=Gender.male)
    status = db.Column(db.Integer, default=1)
    # status: 1-normal 2-banned 3-deleted
    password_hash = db.Column(db.String(100))
    recover_hash = db.Column(db.String(100), default= bcrypt.hashpw(random_string().encode('utf-8'), bcrypt.gensalt()))
    id_token = db.Column(db.String(512), nullable=True)
    image = db.Column(db.Text(), nullable=True)
    role = db.Column(db.Enum(Role), nullable=False, default=Role.viewer)
    last_login = db.Column(db.TIMESTAMP, default=datetime.datetime.now)

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True

    def to_dict(self):
        """
        Transform user obj into dict
        :return:
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'fullname': self.fullname,
            'status': self.status
        }


class UserSchema:
    user = {
        'id': fields.Integer(required=True, description='user id'),
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'role': fields.String(required=False,
                              description='user role (admin|moderator|viewer)')
    }

    user_create_req = user.copy()
    user_create_req.pop('id', None)
    user_create_req.update({
        'password': fields.String(required=True, description='user password'),
    })
