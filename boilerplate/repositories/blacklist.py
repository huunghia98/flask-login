from boilerplate import models as m
from .user import get_one_user_by_email_or_username


def save_user_to_blacklist(**kwargs):
    try:
        u = m.Blacklist(**kwargs)
        m.db.session.add(u)
        m.db.session.commit()
        return log
    except:
        print("Can't save user to blacklist")


def get_user_in_blacklist(username):
    user = get_one_user_by_email_or_username(username, '')
    if user:
        return m.Blacklist.query.get(user.id),1
    return None,False


def save_user_to_blacklist_by_username(username):
    try:
        user = get_one_user_by_email_or_username(username, '')
        data = m.Blacklist(user_id=user.id)
        m.db.session.add(data)
        m.db.session.commit()
        return data
    except:
        print("Can't save user to blacklist")
