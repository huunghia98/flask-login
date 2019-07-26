from .task_background import send_email_task

def send_email(data,to):
    send_email_task.delay(data,to)
