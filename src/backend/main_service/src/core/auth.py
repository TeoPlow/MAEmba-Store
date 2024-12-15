from functools import wraps
from src.core.logging import log

def login_required(f):
    """
    Проверка на то, авторизован ли пользователь
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ...
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Проверка на то, является ли пользователь Админом
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ...
        return f(*args, **kwargs)
    return decorated_function

def same_user_required(f):
    """
    Проверка на то, совершает ли запрос тот же пользователь, чей ID передаётся в запросе.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ...
        return f(*args, **kwargs)
    return decorated_function