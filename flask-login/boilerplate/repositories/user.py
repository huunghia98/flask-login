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


# def get_user(username,password):
#     user = m.User.query.filter(m.User.username == username).all()
#     if len(user) > 1:
#         return None
#     else:
#         if
#         return user