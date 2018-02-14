import importlib

__all__ = (
    'import_object',
)


def import_object(path):
    if not isinstance(path, str):
        return path
    modpath, objname = path.rsplit('.', 1)
    module = importlib.import_module(modpath)
    return getattr(module, objname)

