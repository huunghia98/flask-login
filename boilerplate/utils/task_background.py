from __future__ import absolute_import
from celery import Celery
import smtplib

CELERY_RESULT_BACKEND = 'amqp://huunghia98:nghia123@localhost/flask_login_host'
CELERY_BROKER_URL = 'amqp://huunghia98:nghia123@localhost/flask_login_host'


def make_celery():
    celery = Celery(
        name='celery_task',
        backend=CELERY_RESULT_BACKEND,
        broker=CELERY_BROKER_URL
    )
    return celery


worker = make_celery()

@worker.task
def send_email_task(data, to):
    print('send email to {}'.format(to))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('hnnghia2@gmail.com', 'matkhaukhongdailam')
    msg = """
        From: Super power
        To: {to}
        Here is your account detail to login my service.
        Username: {username}
        Password: {password}
    """.format(to=to, username=data['username'], password=data['password'])
    if data.get('active'):
        msg = msg + """Active link: {}""".format(data.get('active'))

    server.sendmail('hnnghia2@gmail.com', to, msg)
    server.quit()
