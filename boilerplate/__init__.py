# coding=utf-8
import flask
from . import api
from . import models

def create_app():
    import config
    app = flask.Flask(
        __name__
    )
    #config
    app.config.from_object(config)
    app.config.from_pyfile('config.py',silent=True)
    app.secret_key = 'hello-world'

    api.init_app(app)
    models.init_app(app)
    return app

app = create_app()
