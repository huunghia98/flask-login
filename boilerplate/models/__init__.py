import flask_sqlalchemy as _fs
import flask_migrate as _fm

db = _fs.SQLAlchemy()
migrate = _fm.Migrate(db=db)

def init_app(app, **kwargs):
    """
    Extension initialization point
    :param flask.Flask app:
    :param kwargs:
    :return:
    """
    db.app = app
    db.init_app(app)
    migrate.init_app(app)

from .base import TimestampMixin
from .user import User, UserSchema
