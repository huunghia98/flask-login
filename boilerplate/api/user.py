# coding=utf-8
import copy
import flask_restplus as _fr
from flask import request
import flask_jwt_extended as _jwt

from boilerplate.extensions import Namespace
from boilerplate.extensions import exceptions
from boilerplate import models
from boilerplate.services import user
from boilerplate.utils import Role

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
        if data.get('username') and data.get('password'):
            if user.check_user(data.get('username'), data.get('password')):
                access_token = _jwt.create_access_token(identity=data.get('username'));
                return {
                    'access_token': access_token
                }
            else:
                raise exceptions.BadRequestException('Username and password not match')
                # raise Exception('username and password not match')
        else:
            raise exceptions.BadRequestException('Invalid data')


@ns.route('/register', methods=['POST'])
class Register(_fr.Resource):
    def post(self):
        """
        Create new user
        """
        data = request.values
        if data.get('username') and data.get('email') and data.get('password') and data.get('fullname'):
            # if data.get('role') in Role.__members__:
            #     role = Role(data.get('role'))
            # else:
            #     role = Role.viewer
            user.create_user(data.get('username'), data.get('email'), data.get('password'), data.get('fullname'),
                             gender=data.get('gender'), status=data.get('status')
                             # ,role=role
                             )
            return True
        else:
            raise exceptions.BadRequestException('Invalid data')


@ns.route('/forgot', methods=['POST'])
class ForgotPassword(_fr.Resource):
    def post(self):
        """
        Forgot user password
        """
        data = request.values
        if data.get('username') and data.get('email'):
            pw = user.can_reset_password(data.get('username'), data.get('email'))
            if pw:
                return True
            else:
                return exceptions.NotFoundException('Username and email not match')
        else:
            raise exceptions.BadRequestException('Invalid data')


@ns.route('/change', methods=['POST'])
class ChangePassword(_fr.Resource):
    @_jwt.jwt_required
    def post(self):
        """
        Change user password
        """
        identity = _jwt.get_jwt_identity()
        data = request.values
        if data.get('oldpass') and data.get('newpass'):
            if user.change_password(identity, data.get('oldpass'), data.get('newpass')):
                return True
            else:
                return exceptions.ForbiddenException('UnauthorizedU!')
        else:
            raise exceptions.BadRequestException('Invalid data')