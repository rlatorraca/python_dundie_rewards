from random import sample
from string import ascii_letters, digits


def generate_random_simple_password(size=12):
    """Generates a random password
    [A-Z][a-z][0-9]
    """
    password = sample(ascii_letters + digits, size)
    return "".join(password)
