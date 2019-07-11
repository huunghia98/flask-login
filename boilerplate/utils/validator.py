import re

PASSWORD_REGEX = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$'
USERNAME_REGEX = r'^[a-z0-9A-Z]{6,}$'
EMAIL_REGEX = r'^[a-z][a-z0-9_\.]{5,32}@[a-z0-9]{2,}(\.[a-z0-9]{2,4}){1,2}$'


def validate_password(password):
    return (password and re.match(PASSWORD_REGEX, password))


def validate_username(username):
    return (username and re.match(USERNAME_REGEX, username))


def validate_email(email):
    return (email and re.match(EMAIL_REGEX, email))
