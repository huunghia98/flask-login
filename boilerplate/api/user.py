# coding=utf-8

import datetime

import flask_restplus as _fr
from flask import request
import flask_jwt_extended as _jwt

from boilerplate.extensions import Namespace
from boilerplate.services import user, auth

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
        data = request.values or request.json
        username = data.get('username')
        auth.handle_before_user(username)
        will_lock = auth.will_lock_user_in_time_if_unsuccessful(username)
        try:
            if auth.is_need_captcha(data.get('username')):
                u = user.check_user_with_captcha(data.get('username'), data.get('password'), data.get('captcha'))
            else:
                u = user.check_user(data.get('username'), data.get('password'))
            if u:
                user.update_login(u.id)
                access_token = auth.get_access_token(data, True)

                return {
                    'access_token': access_token
                }
        except Exception as e:
            user.update_log_login_attempt(data.get('username'))
            if will_lock:
                auth.lock_user_in_time(username)
            raise e


@ns.route('/register', methods=['POST'])
class Register(_fr.Resource):
    def post(self):
        """
        Create new user
        """
        data = request.values or request.json

        user.create_user_to_signup_users(data.get('username'), data.get('email'), data.get('password'),
                                         data.get('fullname'), data.get('gender'))
        return {
            'message': 'User was created successfully!'
        }


@ns.route('/forgot', methods=['POST'])
class ForgotPassword(_fr.Resource):
    def post(self):
        """
        Forgot user password
        """
        data = request.values or request.json
        auth.handle_before_user(data.get('username'))
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
        data = request.values or request.json
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
        data = request.values or request.json
        active_token = data.get('active_token')
        user.active_account(active_token=active_token)
        return {
            'message': 'Active success'
        }
