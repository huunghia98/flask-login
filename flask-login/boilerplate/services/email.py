import smtplib

def send_email(data,to):
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

    server.sendmail('hnnghia2@gmail.com',to,msg)
    server.quit()
