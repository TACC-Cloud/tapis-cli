"""Supports Jinja-based templating across the CLI
"""

from jinja2 import Template
from tapis_cli.utils import dynamic_import
from . import settings
from . import variables

__all__ = ['key_values', 'render_template', 'dot_notation']

# Each imported module *must* have a key_values method that returns a dict
IMPORTS = ['settings', 'variables']


def key_values(passed_vals=None):
    """Create a dict that can be used to render a Jinja template
    """
    kvals = dict()

    if not isinstance(passed_vals, dict):
        extras = dict()
    else:
        extras = passed_vals

    for i in IMPORTS:
        a = dynamic_import('tapis_cli.templating.{}'.format(i))
        d = a.key_values()
        kvals.update(d)
    # passed extras override computed or default values
    kvals.update(extras)
    return kvals


def all_keys():
    """Get names of all built-in, renderable variables
    """
    ks = list(key_values().keys())
    ks.sort()
    return ks


def render_template(doc_source, passed_vals=None, allow_undefined=True):
    """Render a string template using extant variables

    Parameters:
        doc_source (str): Template string

    Keyword Arguments:
        passed_vals (dict, optional): Dictionary of variable name/value pairs
        file (str|list, optional): One or more files containing variable data
        allow_undefined (bool, optional): Do not raise an Exception when there are un-rendered variables

    Returns:
        str: Rendered string
    """
    # TODO - actually implement support for allow_undefined
    template = Template(doc_source)
    values = key_values(passed_vals)
    # raise SystemError(values)
    return template.render(**values).encode('utf-8')


def dot_notation(sourcedict, replacelevel=None):
    """Transform a nested configparser option into section.option form
    """
    flat_dict = {}
    for l in list(sourcedict.keys()):
        level = l
        if replacelevel is not None:
            level = replacelevel
        for k in list(sourcedict[l].keys()):
            flat_dict['.'.join([level, k])] = sourcedict[l][k]
    return flat_dict
