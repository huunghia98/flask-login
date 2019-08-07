import logging

import flask_sqlalchemy as _fs
import flask_migrate as _fm

db = _fs.SQLAlchemy()
migrate = _fm.Migrate(db=db)
_logger = logging.getLogger(__name__)

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
    _logger.info('Start app in {env} environment with database: {db}'.format(
        env=app.config['ENV_MODE'],
        db=app.config['SQLALCHEMY_DATABASE_URI']
    ))

from .base import TimestampMixin
from .user import User, UserSchema
from .signup_user import Signup_user
from .log import Log
from .history_pass import History_pass
