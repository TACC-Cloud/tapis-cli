"""A memoizing cache built on the Python ``cloudpickle``
(preferred) or ``pickle`` module.
"""
# Derived from: https://gist.github.com/adah1972/f4ec69522281aaeacdba65dbee53fade
# Supports BSON types as per https://stackoverflow.com/a/18405626
from collections import namedtuple
import functools
import six

try:
    from cloudpickle import dumps, loads, HIGHEST_PROTOCOL
except Exception:
    from pickle import dumps, loads, HIGHEST_PROTOCOL

Serialized = namedtuple('Serialized', 'payload')

# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return json.JSONEncoder.default(self, o)


def mcache(cache):
    def hashable_cache_internal(func):
        def deserialize(value):
            if isinstance(value, Serialized):
                return loads(value.payload)
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
                Serialized(dumps(arg, protocol=HIGHEST_PROTOCOL))
                if type(arg) in (list, dict) else arg for arg in args
            ])
            _kwargs = {
                k: Serialized(dumps(v, protocol=HIGHEST_PROTOCOL))
                if type(v) in (list, dict) else v
                for k, v in kwargs.items()
            }
            return cached_func(*_args, **_kwargs)

        hashable_cached_func.cache_info = cached_func.cache_info
        hashable_cached_func.cache_clear = cached_func.cache_clear
        return hashable_cached_func

    return hashable_cache_internal
