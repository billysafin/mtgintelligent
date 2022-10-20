# -*- encoding:utf8 -*-
import os
import time

ACCESS_FORMAT = "time:%(asctime)s\t%(message)s"
CRITICAL_FORMAT = "time:%(asctime)s\t%(message)s"
SQL_FORMAT = "time:%(asctime)s\t%(message)s"

LOGGING = {
    "version" : 1,
    "disable_existing_loggers": False,
    "formatters": {
        "access" : {
            "format" : ACCESS_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "critical" : {
            "format" : CRITICAL_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "sql" : {
            "format" : SQL_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "access_logfile" : {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(os.path.dirname(__file__), "../../log/", time.strftime("%Y-%m-%d") + "_access.log"),
            "formatter": "access",
            "when" : 'D',
            "interval" : 1,
            "backupCount": 14
        },
        "critical_logfile" : {
            "level": "CRITICAL",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(os.path.dirname(__file__), "../../log/", time.strftime("%Y-%m-%d") + "_critical.log"),
            "formatter": "critical",
            "when" : 'D',
            "interval" : 1,
            "backupCount": 14
        },
        "sql_logfile" : {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(os.path.dirname(__file__), "../../log/", time.strftime("%Y-%m-%d") + "_sql.log"),
            "formatter": "sql",
            "when" : 'D',
            "interval" : 1,
            "backupCount": 14
        }
    },
    'loggers': {
        'access_logger': {
            'handlers': ['access_logfile'],
            'level': 'INFO'
         },
        'critical_logger': {
            'handlers': ['critical_logfile'],
            'level': 'CRITICAL'
        },
        'sqlalchemy.engine': {
            'handlers': ['sql_logfile'],
            'level': 'INFO'
        }
    }
}