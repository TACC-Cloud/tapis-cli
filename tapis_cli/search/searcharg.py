import arrow
import dateparser
from datetime import datetime
# from bson.regex import Regex
from collections import namedtuple
from .arrowspan import ArrowSpan
from . import argmod, argtype, optionize, propertize, tapisize

BOOLEAN_TRUE_STRINGS = ('true', 'on', 'ok', 'y', 'yes', '1')
DATETIME = 'datetime'

Argument = namedtuple('Argument', 'argument, attributes')


class SearchArg(object):
    """Uses metadata to generate argparse and param views of a search term
    """
    PARAMS = [('argument', False, 'argument', 'str', None),
              ('field', False, 'field', 'str', None),
              ('destination', False, 'destination', None, None),
              ('choices', False, 'choices', None, None),
              ('mods', False, 'mods', 'list', [argmod.EQUALS]),
              ('default_mod', False, 'default_mod', 'str', argmod.EQUALS)]

    def __init__(self, field_type=argtype.STRING, **kwargs):
        setattr(self, 'field_type', field_type)
        setattr(self, 'inflection', True)
        for param, required, attr, typ, default in self.PARAMS:
            val = kwargs.get(param, default)
            if required:
                if param not in kwargs:
                    raise ValueError(
                        'Parameter "{}" is required'.format(param))
            setattr(self, attr, val)

        argument = optionize(self.argument)
        destination = tapisize(self.argument)
        field = tapisize(self.argument)

        self.argument = argument
        if self.destination is None:
            self.destination = destination
        if self.field is None:
            self.field = field

    def _mod_help(self):
        orig_mods = self.mods
        mods = []
        for o in orig_mods:
            if o == self.default_mod:
                mods.append(o + '*')
            else:
                mods.append(o)
        modifier_help = '|'.join(mods)
        return modifier_help

    def _metavar_help(self):
        if self.choices is not None:
            metavar = '|'.join(sorted(self.choices))
        else:
            metavar = argtype.param_type_repr(getattr(self,
                                                      'field_type')).lower()

        return metavar

    def get_argparse(self):
        """Generate an argparse argument for a MongoDB collection field
        """
        param_type_text = argtype.param_type_repr(getattr(
            self, 'field_type')).lower()
        modifier = self._mod_help()
        params = {
            'nargs': 2,
            'dest': self.destination,
            'metavar': (modifier, self._metavar_help())
        }
        # Using Argparse's choices param is not currently compatible
        # with nargs:2 where arg.1 is the modifier
        #
        # if self.choices is not None:
        #     params['choices'] = self.choices
        arg = Argument(self.argument, params)
        return arg

    def get_param(self, values):
        """Render a query from the argument's metadata and value(s)
        """
        modifier = None
        # Assumption: first element is search modifier. Otherwise, use
        # default, allowing for --param <value> behavior
        if len(values) == 2:
            modifier = values[0]
            values.remove(values[0])
        elif modifier is None:
            modifier = self.default_mod
        # Now, type-cast values as per SearchArg.field_type
        casted_values = [self.cast(v) for v in values]
        if modifier in self.mods:
            # Expectation: There is a function defined by current class or
            # subclass named `query_X` where X is the modifier. For example,
            # the 'not equals' modifier 'neq' is implemented in `query_neq`
            fn = getattr(self, 'query_' + modifier)
            return fn(casted_values)
        else:
            raise ValueError('"{}" is not a valid modifier for "{}"'.format(
                modifier, self.argument))

    def cast(self, value, field_type=None):
        """Cast a value into a defined Python type
        """
        if field_type is None:
            field_type = self.field_type
        if value:
            # human-provided date string => Python datetime(s)
            if field_type is DATETIME:
                # orig_val = value
                value = self.parse_datetime(value)
                # value.setup(orig_val)
                return value
            # human-provided boolean => Python bool
            elif field_type is bool:
                value = value.lower() in BOOLEAN_TRUE_STRINGS
                return value
            # Fall back to generic Python casting behavior
            try:
                return field_type(value)
            except ValueError:
                raise Exception('Unable to cast {} to {}'.format(
                    value, field_type))

    @classmethod
    def parse_datetime(cls, value, span=None):
        """Transform a human date or time string to a Python UTC datetime
        """
        factory = arrow.ArrowFactory(ArrowSpan)
        dta = factory.get(dateparser.parse(value, settings={'TIMEZONE':
                                                            'UTC'}))
        dta.setup(value)
        return dta

    def to_values(self, value, delim=','):
        """Transform a value into a list of values
        """
        qvals = list()
        if isinstance(value, list):
            return value
        elif isinstance(value, tuple):
            return list(value)
        elif isinstance(value, (bool, int, float)):
            return [value]
        elif isinstance(value, str):
            qvals = value.split(delim)
            qvals = [q.strip() for q in qvals]

        qvals = [self.cast(q) for q in qvals]
        return qvals
