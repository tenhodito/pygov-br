# -*- coding: utf-8 -*-
import pygov_br
import importlib

ModuleType = type(pygov_br)


class DataSourceNode(object):
    """
    Implements the lazy module-loader API:

    >>> import pygov_br
    >>> deputies = pygov_br.data.camara_deputados.deputy.all()

    Consider the query ``data.<mod1>.<mod2>...<name>``. It creates an instance
    of one of two classes:

    * ``pygov_br.<mod1>.<mod2>...<name>.<NameClient>``
    * ``pygov_br.<mod1>.<mod2>....<NameClient>``

    Think about this when organizing your files/classes.
    """

    def __init__(self, path=('pygob_br', 'data'), object=None):
        self._path = tuple(path)
        self._object = object or pygov_br

    def __getattr__(self, attr):
        classname = camelcase(attr + '_client')
        try:
            mod_name = self._object.__name__ + '.' + attr
            mod = importlib.import_module(mod_name)
        except ImportError:
            mod = self._object

        # Try to load class from mod
        if hasattr(mod, classname):
            cls = getattr(mod, classname)
            instance = cls()
            setattr(self, attr, instance)
            return instance

        # either mod is a sub-module or we have an error
        if mod is self._object:
            path = self._path + (attr,)
            path = '.'.join(path)
            raise AttributeError('invalid data source: %s' % path)
        else:
            node = DataSourceNode(self._path + (attr,), mod)
            setattr(self, attr, node)
            return node


def camelcase(attr):
    attr = attr.split('_')
    return ''.join(x.title() for x in attr)
