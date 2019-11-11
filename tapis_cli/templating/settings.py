"""Imports Tapis CLI settings to a Jinja environment

Prefixes TAPIS_PY and TAPIS_CLI are stripped and key names are lowercased.
"""
import re
from tapis_cli import settings

BLACKLIST = ['TAPIS_CLI_ALLOW_EMPTY_VARS']

__all__ = ['key_values']


def key_values():
    key_vals = dict()
    cli_settings = settings.all_settings()
    for k, v in cli_settings.items():
        if k not in BLACKLIST and not k.startswith('_'):
            k = k.lower()
            k = re.sub('^tapis_py_', '', k)
            k = re.sub('^tapis_cli_', '', k)
            key_vals[k] = v
    return key_vals
