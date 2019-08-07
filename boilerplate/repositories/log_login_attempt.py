import datetime
from boilerplate import models as m


def save_log_login_attempt(**kwargs):
    try:
        log = m.Log_login_attempt(**kwargs)
        m.db.session.add(log)
        m.db.session.commit()
        return log
    except Exception as e:
        print("Can't save log login attempt")


def get_number_last_login_attempt_in_time(username, number, time_delta_minutes=3):
    time = datetime.datetime.now() - datetime.timedelta(minutes=time_delta_minutes)
    data = m.Log_login_attempt.query.filter(m.Log_login_attempt.username == username).filter(
        m.Log_login_attempt.created_at > time).order_by(m.Log_login_attempt.created_at.desc()).limit(number).all()
    return data or None
