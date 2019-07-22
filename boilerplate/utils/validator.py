import re

PASSWORD_REGEX = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$'
USERNAME_REGEX = r'^[a-z0-9A-Z]{6,}$'
EMAIL_REGEX = r'^[a-z][a-z0-9_\.]{5,32}@[a-z0-9]{2,}(\.[a-z0-9]{2,4}){1,2}$'
FULLNAME_REGEX = r'^([a-zA-Z]+\s?)*$'

def validate_password(password):
    return (len(password) < 100) and password and re.match(PASSWORD_REGEX, password)


def validate_username(username):
    return (len(username) < 100) and username and re.match(USERNAME_REGEX, username)


def validate_email(email):
    return (len(email) < 100) and email and re.match(EMAIL_REGEX, email)

def validate_fullname(fullname):
    return (len(fullname) < 100) and fullname and re.match(FULLNAME_REGEX, fullname)

def validate_gender(gender):
    return gender == 'male' or gender == 'female'
