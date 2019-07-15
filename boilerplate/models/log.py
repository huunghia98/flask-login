# coding=utf-8
import datetime
import bcrypt

from boilerplate.utils.enum_model import Role,Action
from flask_restplus import fields
from boilerplate.models import db, TimestampMixin

__author__ = 'ThucNC'


class Log(db.Model, TimestampMixin):
    """
    Contains information of temporary sign up users table
    """
    __tablename__ = 'log'

    def __init__(self, **kwargs):
        """
        Support direct initialization
        :param kwargs:
        """
        for k, v in kwargs.items():
            setattr(self, k, v)


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.Enum(Action),nullable=False)

