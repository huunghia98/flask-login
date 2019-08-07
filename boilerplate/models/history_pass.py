# coding=utf-8
import datetime
import bcrypt

from boilerplate.utils import random_string
from boilerplate.utils.enum_model import Role
from flask_restplus import fields
from boilerplate.models import db, TimestampMixin

__author__ = 'ThucNC'


class History_pass(db.Model, TimestampMixin):
    """
    Contains information of temporary sign up users table
    """
    __tablename__ = 'history_pass'

    def __init__(self, **kwargs):
        """
        Support direct initialization
        :param kwargs:
        """
        for k, v in kwargs.items():
            setattr(self, k, v)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    password_hash = db.Column(db.String(100))
