"""Extends Python hashing to support memoization.

Extends Python's hashing support to support memoizing and
serialization of functions with complex parameters and/or returns.
"""
from functools import lru_cache
from . import jsoncache
from . import picklecache

__all__ = ['lru_cache', 'jsoncache', 'picklecache']
