# coding=utf-8
from boilerplate.models import db, TimestampMixin

__author__ = 'ThucNC'


class Log_login_attempt(db.Model, TimestampMixin):
    """
    Contains information of attempt login unsuccessfully
    """
    __tablename__ = 'log_login_attempt'

    def __init__(self, **kwargs):
        """
        Support direct initialization
        :param kwargs:
        """
        for k, v in kwargs.items():
            setattr(self, k, v)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(191), nullable=False)
