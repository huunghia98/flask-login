from boilerplate import models as m
from . import user


def save_user_to_signup_users(**kwargs):
    try:
        user = m.Signup_user(**kwargs)
        m.db.session.add(user)
        return user
    except:
        raise Exception("Can't save user for signing up")


def get_one_signup_user_by_active_token(active_token):
    sgp_user = m.Signup_user.query.filter(m.Signup_user.active_token == active_token).first()
    return sgp_user or None


def move_signup_user_to_user(signup_user):
    exist = user.get_one_user_by_email_or_username(signup_user.username, signup_user.email)
    if exist:
        raise Exception('Sorry. User with this detail actived before you')
    try:
        us = user.save_user(username=signup_user.username, password_hash=signup_user.password_hash,
                            email=signup_user.email, fullname=signup_user.fullname, gender=signup_user.gender)
        m.db.session.delete(signup_user)
        m.db.session.commit()
        return True
    except:
        raise Exception("Can't save user from signup user")
