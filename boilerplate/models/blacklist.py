# coding=utf-8
import datetime
import bcrypt

from boilerplate.utils.enum_model import Status
from boilerplate.models import db, TimestampMixin

__author__ = 'ThucNC'


class Blacklist(db.Model, TimestampMixin):
    """
    Contains information of user in blacklist
    """
    __tablename__ = 'blacklist'

    def __init__(self, **kwargs):
        """
        Support direct initialization
        :param kwargs:
        """
        for k, v in kwargs.items():
            setattr(self, k, v)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),primary_key=True)
    status = db.Column(db.Enum(Status),default=Status.lock_in_time)
    expire_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now() + datetime.timedelta(minutes=15))
