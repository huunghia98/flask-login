import datetime
import flask_jwt_extended as _jwt
import requests
import json
from boilerplate.extensions.exceptions import BadRequestException,ForbiddenException
from boilerplate.repositories import log_login_attempt as l_a,blacklist,user

SECRET_KEY_CAPTCHA = '6Lc5j7EUAAAAABlK_ZdsKxdKOLYUXpBFD08W7DT5'


def get_access_token(data, fresh):
    iden = {
        'username': data.get('username'),
        'role': 'viewer'
    }
    return _jwt.create_access_token(identity=iden, fresh=fresh, expires_delta=datetime.timedelta(minutes=30))


def verify_captcha_user_token(token):
    res = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
        'secret': SECRET_KEY_CAPTCHA,
        'response': token,
    })

    if res.status_code == 200:
        data = json.loads(res.content)
        if not data.get('success'):
            raise BadRequestException('Captcha invalid')
        return True
    raise Exception('System error')


def is_need_captcha(username):
    attempt = l_a.get_number_last_login_attempt_in_time(username, 2, 5)
    if not attempt:
        return False

    if len(attempt) < 2:
        return False
    return True

def handle_before_user(username):
    bl_user,user_exist = blacklist.get_user_in_blacklist(username)
    if not user_exist:
        raise BadRequestException('User not exist')
    if not bl_user:
        return True
    if bl_user.expire_at < datetime.datetime.now():
        return True
    raise ForbiddenException('User locked')


def will_lock_user_in_time_if_unsuccessful(username):
    attempt = l_a.get_number_last_login_attempt_in_time(username, 4, 10)
    if not attempt:
        return False
    if len(attempt) < 4:
        return False

    return True

def lock_user_in_time(username):
    u,_ = blacklist.get_user_in_blacklist(username)
    if not u:
        blacklist.save_user_to_blacklist_by_username(username)
    if u:
        u.expire_at = datetime.datetime.now()+datetime.timedelta(minutes=15)
