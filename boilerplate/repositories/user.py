import datetime
from boilerplate import models as m
from sqlalchemy import or_


def save_user(**kwargs):
    try:
        user = m.User(**kwargs)
        m.db.session.add(user)
        m.db.session.commit()
        return user
    except:
        raise Exception("Can't save user")


def get_one_user_by_email_or_username(username, email):
    user = m.User.query.filter(or_(m.User.username == username, m.User.email == email)).first()
    return user or None


def update_recover_hash(user, hash):
    user.recover_hash = hash
    m.db.session.commit()


def update_password_hash(user, hash):
    user.password_hash = hash
    m.db.session.commit()


def update_last_login(user_id):
    u = m.User.query.get(user_id)
    u.last_login = datetime.datetime.now()
    m.db.session.commit()
