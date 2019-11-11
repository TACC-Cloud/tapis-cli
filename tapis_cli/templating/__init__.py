"""Supports Jinja-based templating across the CLI
"""

from jinja2 import Template
from tapis_cli.utils import dynamic_import
from . import settings
from . import variables

__all__ = ['key_values', 'render_template']

# Each imported module *must* have a key_values method that returns a dict
IMPORTS = ['settings', 'variables']


def key_values(supplemental=None):
    """Create a dict that can be used to render a Jinja template
    """
    if not isinstance(supplemental, dict):
        kvals = dict()
    else:
        kvals = supplemental
    for i in IMPORTS:
        a = dynamic_import('tapis_cli.templating.{}'.format(i))
        d = a.key_values()
        kvals.update(d)
    return kvals


def all_keys():
    """Return all available template variable names
    """
    ks = list(key_values().keys())
    ks.sort()
    return ks


def render_template(doc_source, supplemental=None):
    template = Template(doc_source)
    values = key_values(supplemental)
    return template.render(**values)
