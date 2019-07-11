import string
import random

N = 12

def random_string():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
