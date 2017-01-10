import os
import json
import pkgutil
from copy import deepcopy
from importlib import import_module
from collections import Mapping, OrderedDict

POSIX = os.name != 'nt'


def multiply(expression):
    """ A simple multiplication parser
        :param expression: e.g. "1024*1024*50"
    """
    value = 1
    for n in expression.split('*'):
        value *= int(n)
    return value


def merge_dict(base, upd, inplace=False):
    """ Merge data or configure
    """
    assert isinstance(base, Mapping), isinstance(upd, Mapping)
    dst = base if inplace else deepcopy(base)
    stack = [(dst, upd)]
    while stack:
        current_dst, current_src = stack.pop()
        for key in current_src:
            if key not in current_dst:
                current_dst[key] = current_src[key]
            else:
                if isinstance(current_src[key], Mapping) and isinstance(current_dst[key], Mapping):
                    stack.append((current_dst[key], current_src[key]))
                else:
                    current_dst[key] = current_src[key]
    return dst


def recursive_import(package):
    """ Recursive import python package
    """
    for importer, modname, is_pkg in pkgutil.iter_modules(package.__path__):
        sub_package = import_module('%s.%s' % (package.__package__ or package.__name__, modname))
        if is_pkg:
            recursive_import(sub_package)


def deep_sort(data):
    """ Sort data and it's daughter element
    """
    if type(data) == list:
        ret = []
        data.sort()
        for item in data:
            ret.append(deep_sort(item))
        return ret
    elif type(data) == dict:
        ret = OrderedDict()
        keys = data.keys()
        keys.sort()
        for key in keys:
            ret[key] = deep_sort(data[key])
        return ret
    else:
        return data


class JsonShow(object):
    """ Performance optimization for log, execute json.dumps only on log.level allowed
    """

    def __init__(self, data_object):
        self.data_object = data_object

    def __str__(self):
        try:
            content = json.dumps(self.data_object, indent=4)
        except TypeError:
            # data_object is not JSON serializable
            content = str(self.data_object)

        return os.linesep + content
