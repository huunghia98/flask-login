# coding=utf-8

from flask import Blueprint
from flask_restplus import Api
from boilerplate.extensions.exceptions import global_error_handler
from .user import ns as user_ns
from .welcome import wc as wc_ns
import flask_jwt_extended as _jwt

api_bp = Blueprint('api', __name__, url_prefix='/api')

api = Api(
    app=api_bp,
    version='1.0',
    title='LoginAPI',
    validate=False,
    # doc='' # disable Swagger UI
)


def init_app(app, **kwargs):
    """
    :param flask.Flask app: the app
    :param kwargs:
    :return:
    """
    app.config['JWT_SECRET_KEY'] = 'hello-boy'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 300
    jwt = _jwt.JWTManager(app)

    api.add_namespace(user_ns)
    api.add_namespace(wc_ns)
    app.register_blueprint(api_bp)
    api.error_handlers[Exception] = global_error_handler