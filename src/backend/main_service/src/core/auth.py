from functools import wraps
from src.core.logging import log

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ...
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ...
        return f(*args, **kwargs)
    return decorated_function