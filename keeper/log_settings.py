import sys


# Python Logging documentation
# https://docs.python.org/3/library/logging.html

def get_logging_config(debug=False):
    return {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': ('at=%(levelname)s logger="%(name)s" lineno=%(lineno)s ' +
                           'funcname="%(funcName)s" msg="%(message)s"'),
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG' if debug else 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
                'stream': sys.stdout,
            },
        },
        'loggers': {
            'root': {
                'level': 'INFO',
                'handlers': ['console'],
                'propagate': True,
            },
            'django.server': {
                'level': 'WARNING',
                'handlers': ['console'],
            },
            'orgs': {
                'level': 'DEBUG' if debug else 'INFO',
                'handlers': ['console'],
                'propagate': True,
            },
        }
    }
