from boilerplate import models as m

def save_log(**kwargs):
    try:
        log = m.Log(**kwargs)
        m.db.session.add(log)
        m.db.session.commit()
        return log
    except:
        print("Can't save Log")