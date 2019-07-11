import re
import bcrypt
from boilerplate.repositories import user
from boilerplate.extensions.exceptions import BadRequestException
from . import email as e_m

def create_user(username, email, password, fullname, **kwargs):
    if (username and re.match(r'^[a-z0-9A-Z]{6,}$', username)
            and email and re.match(r'^[a-z][a-z0-9_\.]{5,32}@[a-z0-9]{2,}(\.[a-z0-9]{2,4}){1,2}$', email)
            and password and re.match(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$', password)
            and fullname):
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
    return bcrypt.checkpw(password.encode('utf-8'), u.password_hash.encode('utf-8')) or bcrypt.checkpw(password.encode('utf-8'), u.recover_hash.encode('utf-8'))

def can_reset_password(username,email):
    u = user.get_one_user_by_email_or_username(username, '')
    if u:
        if u.email == email:
            p = username + email
            p = bcrypt.hashpw(p.encode('utf-8'),bcrypt.gensalt())
            user.update_recover_hash(u, bcrypt.hashpw(p,bcrypt.gensalt()))
            new_detail = {
                'username': username,
                'password': p.decode()
            }
            e_m.send_email(new_detail,email)
            return p
        else:
            return False
    else:
        return False

def change_password(username,oldpass,newpass):
    u = user.get_one_user_by_email_or_username(username, '')
    if u:
        if oldpass != newpass:
            if check_user(username,oldpass):
                user.update_password_hash(u,bcrypt.hashpw(newpass.encode('utf-8'),bcrypt.gensalt()))
                return True
            else:
                raise BadRequestException('Not match password to username')
        else:
            raise BadRequestException('2 password must be different')
    else:
        return BadRequestException('User not exist')
