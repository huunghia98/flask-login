# coding=utf-8

import flask_restplus as _fr
from flask import request
from boilerplate.extensions import Namespace
from boilerplate.extensions import exceptions
from boilerplate import models
from boilerplate.services import user
import flask_jwt_extended as _jwt

wc = Namespace('welcome', description='welcome page')


@wc.route('/', methods=['GET'])
class Welcome(_fr.Resource):
    @_jwt.jwt_required
    def get(self):
        """
        Welcome user
        """
        identity = _jwt.get_jwt_identity()
        return {
            'welcome': 'Hello, you are welcome'
        }

