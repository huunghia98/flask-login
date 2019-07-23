import bcrypt
import datetime

from boilerplate.repositories import user, log, signup_user, history_pass
from boilerplate.extensions.exceptions import BadRequestException
from boilerplate.utils.validator import *
from boilerplate.utils import email as e_m
from boilerplate.utils import random_string

HOST = 'http://127.0.0.1:5000'

def create_user_to_signup_users(username, email, password, fullname, gender, **kwargs):
    validGender = (not gender) or validate_gender(gender)
    if validate_username(username) and validate_password(password) and validate_email(email) and validate_fullname(fullname) and validGender:
        exist = user.get_one_user_by_email_or_username(username, email)
        if exist:
            raise BadRequestException('User {username} or email {email} existed'.format(username=username, email=email))
        else:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
            active_token = bcrypt.hashpw(random_string().encode('utf-8'), bcrypt.gensalt())
            link_active = HOST+"/api/users/active/?active_token={}".format(active_token.decode('utf-8'))
            us = signup_user.save_user_to_signup_users(username=username, email=email, password_hash=password_hash,
                                                       fullname=fullname, active_token=active_token,
                                                       **kwargs)
            try:
                e_m.send_email({
                    'username': username,
                    'password': password,
                    'active': link_active
                }, email)
            except:
                print('Email user {} not be sent'.format(email))
            return us
    else:
        raise BadRequestException('Invalid data')

def update_login(user_id):
    log.save_log(user_id=user_id,action='login')
    user.update_last_login(user_id)

def check_user(username, password):
    if (not username) or (not password):
        raise BadRequestException('Username and Password must not be empty')
    if not validate_username(username) or not validate_password(password):
        raise BadRequestException('Invalid data')
    u = user.get_one_user_by_email_or_username(username, '')
    if not u:
        raise BadRequestException('User not exist')
    if u.status > 1:
        raise BadRequestException('User was banned or deleted')
    if not (bcrypt.checkpw(password.encode('utf-8'), u.password_hash.encode('utf-8')) or bcrypt.checkpw(
            password.encode('utf-8'), u.recover_hash.encode('utf-8'))):
        raise BadRequestException('Username and password not match')
    return u


def can_reset_password(username, email):
    if (not username) or (not email):
        raise BadRequestException('Username and email must not be empty')
    u = user.get_one_user_by_email_or_username(username, '')
    if u:
        if u.email == email:
            if u.status > 1:
                raise BadRequestException('User was banned or deleted')
            log.save_log(user_id = u.id,action='forgot')
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

            history = history_pass.get_history_5_pass(u.id)
            if validate_password(newpass):
                for pwd in history:
                    try:
                        pw = pwd.encode('utf-8')
                    except:
                        pw = pwd
                    if bcrypt.checkpw(newpass.encode('utf-8'), pw):
                        raise BadRequestException('Password must be different from 5 lastest password')
                history_pass.save_history_pass(user_id=u.id,
                                               password_hash=bcrypt.hashpw(newpass.encode('utf-8'), bcrypt.gensalt()))
                user.update_password_hash(u, bcrypt.hashpw(newpass.encode('utf-8'), bcrypt.gensalt()))
                log.save_log(user_id=u.id, action='change')
            else:
                raise BadRequestException('New password must be in format')
            return True
        else:
            raise BadRequestException('2 password must be different')
    else:
        raise BadRequestException('User not exist')


def active_account(active_token):
    u = signup_user.get_one_signup_user_by_active_token(active_token)
    if not u:
        raise BadRequestException('Active invalid')
    if u.token_expire_at < datetime.datetime.now():
        raise BadRequestException('Token expired')
    us = signup_user.move_signup_user_to_user(u)
    log.save_log(user_id = us.id,action='create')
    return True
