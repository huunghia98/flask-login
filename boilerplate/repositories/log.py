from boilerplate import models as m

def save_log(**kwargs):
    try:
        log = m.Log(**kwargs)
        m.db.session.add(log)
        return log
    except:
        raise Exception("Can't save Log")