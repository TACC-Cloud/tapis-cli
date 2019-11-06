import re
import collections
import stringcase

__all__ = ['Argdef', 'optionize', 'propertize', 'tapisize', 'spinal_to_camel']

Argdef = collections.namedtuple(
    'Argdef',
    'param_name param_type verbosity mod_types default_mod choices override_option searchable'
)


def optionize(fieldKeyName):
    """Transforms a string into an argparse option
    """
    cased = stringcase.spinalcase(fieldKeyName)
    # Strip leading dash, which can get introduced if the fieldKeyName starts
    # with a character that stringcase interprets as a delimiter
    cased = re.sub('^(-){1,}', '', cased)
    return '--{0}'.format(cased)


def propertize(fieldKeyName):
    """Transforms a string into an Python parameter name
    """
    return stringcase.snakecase(fieldKeyName)


def tapisize(fieldKeyName):
    """Transforms a string into a Tapis query parameter
    """
    return fieldKeyName.lower()


def spinal_to_camel(optionName):
    option = re.sub('(-){1,}', '_', optionName)
    option = re.sub('^(_){1,}', '', option)
    return stringcase.camelcase(option)
