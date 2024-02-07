import logging
import logging.config
from datetime import datetime
from functools import wraps
import psutil

from config import config


class Logger:
    @staticmethod
    def get_path_to_log_file():
        path_to_logs = config["PATH_TO_LOGS"]
        now = datetime.now()
        return path_to_logs + str(now.strftime("%Y%m%d")) + ".log"

    @classmethod
    def get_logger(cls):
        config = cls.get_log_config()
        logging.config.dictConfig(config)
        __logger = logging.getLogger('root')
        return __logger

    @classmethod
    def get_log_config(cls):
        path_to_file = cls.get_path_to_log_file()
        return {
            "version": 1,
            "handlers": {
                "fileHandler": {
                    "class": "logging.FileHandler",
                    "formatter": "myFormatter",
                    "filename": path_to_file
                }
            },
            "loggers": {
                "root": {
                    "handlers": ["fileHandler"],
                    "level": logging.INFO,
                }
            },
            "formatters": {
                "myFormatter": {
                    "format": "%(levelname)s|%(asctime)s|%(message)s"
                }
            }
        }

    @classmethod
    def save_action_message(cls, action_type, message, is_error=True, is_start=False):
        logger = cls.get_logger()
        pid = psutil.Process().pid
        if is_error:
            logger.error(f"{pid}|{action_type}|{'START' if is_start else 'FINISH'}|{message}")
        else:
            logger.info(f"{pid}|{action_type}|{'START' if is_start else 'FINISH'}|{message}")

    @classmethod
    def __log_method(cls, func, error_message="", is_start=True):
        try:
            action_type = func.__qualname__
            is_error = False
            message = ""
            if error_message:
                message = str(error_message)[:500]
                is_error = True

            cls.save_action_message(action_type, message, is_error, is_start)
        except Exception as e:
            print("Failed to action", func.__qualname__, e)

    @classmethod
    def log_method_start(cls, func):
        cls.__log_method(func)

    @classmethod
    def log_method_finish(cls, func, error_message=""):
        cls.__log_method(func, error_message=error_message, is_start=False)


def log_func(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            Logger.log_method_start(f)
            result = f(*args, **kwargs)
            Logger.log_method_finish(f)
            return result
        except Exception as e:
            Logger.log_method_finish(f, str(e))
            raise e
    return decorated


def log_method(f):
    @wraps(f)
    def decorated(this, *args, **kwargs):
        try:
            Logger.log_method_start(f)
            result = f(this, *args, **kwargs)
            Logger.log_method_finish(f)
            return result
        except Exception as e:
            Logger.log_method_finish(f, str(e))
            raise e
    return decorated
