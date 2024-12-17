import sys
import logging
import logging.config
from colorama import Fore, Style

from src.core.config import LOG_LEVEL

log = logging.getLogger('user_auth_service')

# Логгер и его форматеры
class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.WHITE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, Style.RESET_ALL)
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        record.msg = f"{log_color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)
    
logger_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "()": ColorFormatter,
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(filename)s:%(lineno)s | %(message)s",
            "datefmt": "%H:%M:%S"
        }
    },
    "handlers": {
        "screen_handler": {
            "class": "logging.StreamHandler",
            "level": LOG_LEVEL,
            "formatter": "base",
            "stream": sys.stdout
        },
    },
    "loggers": {
        'user_auth_service': {
            'level': LOG_LEVEL,
            'handlers': ["screen_handler"],
            'propagate': False
        }
    }
}
logging.config.dictConfig(logger_config)