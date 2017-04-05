import os
import logging
logger = logging.getLogger(__name__)


# Return an environment variable by name.
# Allows "plain text" booleans and comma-separated lists.

def getenv(var, default=None):
    result = os.environ.get(var, default)
    logger.debug("[ENV] {}={}".format(var, result))
    if isinstance(result, (bool, int, list, tuple)) or not result:
        return result
    if result.upper() == "TRUE":
        return True
    elif result.upper() == "FALSE":
        return False
    elif result.upper() == "NONE" or result.strip() == "":
        return None
    if ',' in result:
        return list(filter(lambda x: x, (i.strip() for i in result.split(','))))
    try:
        return int(result)
    except ValueError:
        pass
    return result


# A decorator that returns a default value when ValueError is caught in the decorated function
# This is intended for use with getters on Django Models

def missing(f, exceptions=None, default=None):
    exceptions = exceptions or (AttributeError,)

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except exceptions:
            return default

    return inner


__all__ = ('getenv', 'missing')