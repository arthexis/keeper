import os
import random
import string
import logging

from django.urls import path as _path
from django.views.generic import TemplateView, View

logger = logging.getLogger(__name__)


__all__ = (
    'exists',
    'getenv',
    'missing',
    'path',
    'rand_string'
)


def getenv(var, default=None):
    """ Fetches an environment variable and coerces it into a Python type.

    :param var: Name of the OS environment variable.
    :param default: Value to return if the variable is not found.
    :return:
    """
    r = os.environ.get(var, default)
    logger.debug("[ENV] {}={}".format(var, r))
    if isinstance(r, (bool, int, list, tuple)) or not r:
        return r
    if r.upper() == "TRUE":
        return True
    elif r.upper() == "FALSE":
        return False
    elif r.upper() == "NONE" or r.strip() == "":
        return None
    if ',' in r:
        return list(filter(lambda x: x, (i.strip() for i in r.split(','))))
    try:
        return int(r)
    except ValueError:
        pass
    return r


def missing(val):
    """ Decorator that makes a function catch ValueError and return a value instead.

    :param val: Value to return when the exceptions are caught, defaults to None
    :return: A decorated function.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (IndexError, AttributeError, TypeError):
                return val
        return wrapper

    return decorator


def path(pattern, view, name=None, **kwargs):
    """ Simplifies django.urls.path

    :param pattern: URL pattern, same syntax as django.urls.path
    :param view: View, can be class or function
    :param name: Name used for reverse, defaults to view.name if exists
    :param kwargs: Keyword arguments for the view
    :return: An object that can be added to urlpatterns
    """

    if name is None:
        try:
            name = view.name
        except AttributeError:
            pass

    if name is None:
        logger.warning(f'Path {pattern} to view {view} missing name.')

    try:
        if issubclass(view, View):
            # logger.debug(f'URL View {view} = {name}')
            return _path(pattern, view.as_view(), kwargs=kwargs, name=name)
    except TypeError:
        pass
    if isinstance(view, str):
        return _path(
            pattern, TemplateView.as_view(template_name=view),
            kwargs=kwargs, name=name)
    return _path(pattern, view, name=name, kwargs=kwargs)


def rand_string(chars):
    return ''.join(random.choice(string.ascii_letters) for _ in range(chars))


def exists(model, instance=None, **kwargs):
    """ Finds is a model instance with certain values already exists.

    :param model: Model class
    :param instance: Optional instance to exclude, for example form.instance
    :param kwargs: Query filters used to identify the instance.
    :return: True if the instance exists, False otherwise.
    """
    qs = model.objects.filter(**kwargs)
    if instance and instance.pk:
        qs = qs.exclude(pk=instance.pk)
    return qs.exists()


def aggregate(queryset, operator, field):
    return queryset.aggregate(x=operator(field))['x']



