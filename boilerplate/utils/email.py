import smtplib

def send_email(data,to):
    print('send email to {}'.format(to))
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('hnnghia2@gmail.com','matkhaukhongdailam')
    msg = """
        From: Super power
        To: {to}
        Here is your account detail to login my service.
        Username: {username}
        Password: {password}
    """.format(to=to,username= data['username'],password = data['password'])
    if data.get('active'):
        msg = msg + """Active link: {}""".format(data.get('active'))

    server.sendmail('hnnghia2@gmail.com',to,msg)
    server.quit()
