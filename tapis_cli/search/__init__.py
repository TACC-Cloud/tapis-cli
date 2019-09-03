"""Methods and classes for building CLI-driven search and filtering
"""
# from .argument import SearchArg
from .argdef import Argdef, optionize, propertize, tapisize
from .searcharg import SearchArg
from .param import SearchWebParam, SearchWebParamEqualsOnly
from .mongoql import SearchMongoQuery
from . import argmod
from . import argtype
# from .. import utils
