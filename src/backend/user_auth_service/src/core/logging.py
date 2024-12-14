import sys
from colorama import Fore, Style
import logging

log = logging.getLogger('main_service')

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
            "level": "DEBUG",
            "formatter": "base",
            "stream": sys.stdout
        },
    },
    "loggers": {
        'main_service': {
            'level': 'DEBUG',
            'handlers': ["screen_handler"],
            'propagate': False
        },
        'user_auth_service': {
            'level': 'DEBUG',
            'handlers': ["screen_handler"],
            'propagate': False
        },
    }
}