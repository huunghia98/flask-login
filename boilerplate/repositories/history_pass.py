from boilerplate import models as m

def get_history_5_pass(user_id):
    history = m.History_pass.query.filter(m.History_pass.user_id==user_id).order_by(m.History_pass.created_at.desc()).limit(5).all()
    a = [x.password_hash for x in history]
    return a


def save_history_pass(**kwargs):
    try:
        p = m.History_pass(**kwargs)
        m.db.session.add(p)
        m.db.session.commit()
        return p
    except:
        raise Exception("Can't save history pass")