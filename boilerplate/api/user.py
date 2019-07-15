# coding=utf-8
import copy
import datetime

import flask_restplus as _fr
from flask import request
import flask_jwt_extended as _jwt

from boilerplate.extensions import Namespace
from boilerplate.services import user

ns = Namespace('users', description='User operations')


# _user_res = ns.model('user_res', models.UserSchema.user)
# _user_create_req = ns.model('user_create_req',models.UserSchema.user_create_req)

@ns.route('/login', methods=['POST'])
class Login(_fr.Resource):
    # @ns.expect(_user_create_req, validate=True)
    # @ns.marshal_with(_user_res)
    def post(self):
        """
        Get access token
        """
        data = request.values
        if user.check_user(data.get('username'), data.get('password')):
            iden = {
                'username': data.get('username'),
                'role': 'viewer'
            }
            access_token = _jwt.create_access_token(identity=iden,fresh=True,expires_delta=datetime.timedelta(minutes=30))
            return {
                'access_token': access_token
            }


@ns.route('/register', methods=['POST'])
class Register(_fr.Resource):
    def post(self):
        """
        Create new user
        """
        data = request.values
        user.create_user_to_signup_users(data.get('username'), data.get('email'), data.get('password'), data.get('fullname'),
                             gender=data.get('gender'), status=data.get('status')
                             # ,role=role
                             )
        return {
            'message':'User was created successfully!'
        }

@ns.route('/forgot', methods=['POST'])
class ForgotPassword(_fr.Resource):
    def post(self):
        """
        Forgot user password
        """
        data = request.values
        pw = user.can_reset_password(data.get('username'), data.get('email'))
        return {
            'message': 'Success. Please check email for new information.'
        }


@ns.route('/change', methods=['POST'])
class ChangePassword(_fr.Resource):
    @_jwt.fresh_jwt_required
    def post(self):
        """
        Change user password
        """
        identity = _jwt.get_jwt_identity()
        data = request.values
        user.change_password(identity.get('username'), data.get('oldpass'), data.get('newpass'))
        return {
            'message': 'Password was changed successfully'
        }

@ns.route('/active/', methods=['GET'])
class Active(_fr.Resource):
    def get(self):
        """
        Active account
        """
        data = request.values
        active_token = data.get('active_token')
        return user.active_account(active_token=active_token)