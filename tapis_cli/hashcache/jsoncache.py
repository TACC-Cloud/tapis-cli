"""A memoizing cache built on the Python ``json`` module
"""
# Derived from: https://gist.github.com/adah1972/f4ec69522281aaeacdba65dbee53fade
# Supports BSON types as per https://stackoverflow.com/a/18405626
from collections import namedtuple
import functools
import json
import six
from bson import Binary, Code, Timestamp
from bson.json_util import loads, dumps

Serialized = namedtuple('Serialized', 'json')


def mcache(cache):
    def hashable_cache_internal(func):
        def deserialize(value):
            if isinstance(value, Serialized):
                return loads(value.json)
            else:
                return value

        def func_with_serialized_params(*args, **kwargs):
            _args = tuple([deserialize(arg) for arg in args])
            _kwargs = {k: deserialize(v) for k, v in six.viewitems(kwargs)}
            return func(*_args, **_kwargs)

        cached_func = cache(func_with_serialized_params)

        @functools.wraps(func)
        def hashable_cached_func(*args, **kwargs):
            _args = tuple([
                Serialized(dumps(arg, sort_keys=True))
                if type(arg) in (list, dict) else arg for arg in args
            ])
            _kwargs = {
                k: Serialized(dumps(v, sort_keys=True))
                if type(v) in (list, dict) else v
                for k, v in kwargs.items()
            }
            return cached_func(*_args, **_kwargs)

        hashable_cached_func.cache_info = cached_func.cache_info
        hashable_cached_func.cache_clear = cached_func.cache_clear
        return hashable_cached_func

    return hashable_cache_internal


# # Example usage below

# from cachetools.func import lru_cache

# @hashable_cache(lru_cache())
# def fib(n):
#     assert n >= 0
#     if n == 0:
#         return 0
#     elif n == 1:
#         return 1
#     else:
#         return fib(n - 1) + fib(n - 2)
