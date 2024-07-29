

from functools import wraps
import os


def requires_authentication(f):
    @wraps(f)
    def decorator(self, *args, **kwargs):
        email = os.getenv('DUNDIE_EMAIL')
        password = os.getenv('DUNDIE_PASSWORD')
