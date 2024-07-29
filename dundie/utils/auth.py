from functools import wraps


def requires_authentication(f):
    @wraps(f)
    def decorator(self, *args, **kwargs):
        """Decorator for authenticating"""
        # email = os.getenv('DUNDIE_EMAIL')
        # password = os.getenv('DUNDIE_PASSWORD')
