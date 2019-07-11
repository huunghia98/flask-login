from boilerplate import models as m

def save_user(**kwargs):
    try:
        user = m.User(**kwargs)
        m.db.session.add(user)
        return user
    except:
        raise Exception("Can't save user")


def get_one_user_by_email_or_username(username, email):
    user = m.User.query.filter((m.User.username == username) | (m.User.email == email)).first()
    return user or None

def update_recover_hash(user,hash):
    user.recover_hash = hash
    m.db.session.commit()

def update_password_hash(user,hash):
    user.password_hash = hash
    m.db.session.commit()