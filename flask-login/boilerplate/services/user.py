import re
import bcrypt
from boilerplate.repositories import user
from boilerplate.extensions.exceptions import BadRequestException
from . import email as e_m

def create_user(username, email, password, fullname, **kwargs):
    if (username and re.match(r'^[a-z0-9A-Z]{6,}$', username)
            and email and re.match(r'^[a-z][a-z0-9_\.]{5,32}@[a-z0-9]{2,}(\.[a-z0-9]{2,4}){1,2}$', email)
            and password and re.match(r'^[a-z0-9A-Z]{8,}$', password)):
        exist = user.get_one_user_by_email_or_username(username, email)
        if exist:
            raise BadRequestException('User {username} or email {email} existed'.format(username=username, email=email))
        else:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
            us = user.save_user(username=username, email=email, password_hash=password_hash, fullname=fullname,
                                **kwargs)
            # try:
            #     e_m.send_email({
            #         'username':username,
            #         'password': password
            #     }, email)
            # except:
            #     print('Email user {} not be sent'.format(email))
            return us
    else:
        raise BadRequestException('Invalid data')


def check_user(username, password):
    u = user.get_one_user_by_email_or_username(username, '')
    if not u :
        return False
    return bcrypt.checkpw(password.encode('utf-8'), u.password_hash.encode('utf-8'))

def can_reset_password(username,email):
    u = user.get_one_user_by_email_or_username(username, '')