import string
import random


def random_string(n=12):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
