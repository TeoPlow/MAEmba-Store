from functools import wraps
import logging
import logging.config
from core.logging import logger_config, log

logging.config.dictConfig(logger_config)

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