import bcrypt

from boilerplate.repositories import user
from boilerplate.extensions.exceptions import BadRequestException
from boilerplate.utils.validator import *
from boilerplate.utils import email as e_m


def create_user(username, email, password, fullname, **kwargs):
    if (validate_username(username) and validate_password(password) and validate_email(email) and fullname):
        exist = user.get_one_user_by_email_or_username(username, email)
        if exist:
            raise BadRequestException('User {username} or email {email} existed'.format(username=username, email=email))
        else:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
            us = user.save_user(username=username, email=email, password_hash=password_hash, fullname=fullname,
                                **kwargs)
            try:
                e_m.send_email({
                    'username':username,
                    'password': password
                }, email)
            except:
                print('Email user {} not be sent'.format(email))
            return us
    else:
        raise BadRequestException('Invalid data')


def check_user(username, password):
    if (not username) or (not password):
        raise BadRequestException('Username and Password must not be empty')
    u = user.get_one_user_by_email_or_username(username, '')

    if not u:
        raise BadRequestException('User not exist')
    if not (bcrypt.checkpw(password.encode('utf-8'), u.password_hash.encode('utf-8')) or bcrypt.checkpw(
            password.encode('utf-8'), u.recover_hash.encode('utf-8'))):
        raise BadRequestException('Username and password not match')
    return True


def can_reset_password(username, email):
    if (not username) or (not email):
        raise BadRequestException('Username and email must not be empty')
    u = user.get_one_user_by_email_or_username(username, '')
    if u:
        if u.email == email:
            p = username + email
            p = bcrypt.hashpw(p.encode('utf-8'), bcrypt.gensalt())
            user.update_recover_hash(u, bcrypt.hashpw(p, bcrypt.gensalt()))
            new_detail = {
                'username': username,
                'password': p.decode()
            }
            e_m.send_email(new_detail, email)
            return p
        else:
            raise BadRequestException('Username and email not match')
    else:
        raise BadRequestException('Username not found')


def change_password(username, oldpass, newpass):
    if (not username) or (not oldpass) or (not newpass):
        raise BadRequestException('Data fields must not be empty')
    u = user.get_one_user_by_email_or_username(username, '')
    if u:
        if oldpass != newpass:
            try:
                check_user(username, oldpass)
            except:
                raise BadRequestException('Password was incorrect!')
            if validate_password(newpass):
                user.update_password_hash(u, bcrypt.hashpw(newpass.encode('utf-8'), bcrypt.gensalt()))
            else:
                raise BadRequestException('New password must be in format')
            return True
        else:
            raise BadRequestException('2 password must be different')
    else:
        raise BadRequestException('User not exist')
