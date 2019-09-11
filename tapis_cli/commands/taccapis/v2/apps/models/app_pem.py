"""Data model and functions for Tapis apps
"""
from .. import SERVICE_VERSION
from tapis_cli.commands.taccapis import TapisModel
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod
from tapis_cli import constants
from .app import App

__all__ = ['App', 'API_NAME', 'SERVICE_VERSION']

API_NAME = 'apps'


class AppPermission(App):
    """Model of a Tapis application permission
    """
    payload = dict()
    NAMES = [
        'ALL', 'READ', 'WRITE', 'READ_WRITE', 'EXECUTE', 'READ_EXECUTE',
        'WRITE_EXECUTE', 'NONE'
    ]

    SEARCH_ARGS = [
        # JSON_field, type, verbosity, mods_allowed, default_mod, choices, override_option, searchable
        ("username", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("permission", argtype.OBJECT, Verbosity.LISTING,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("_links", argtype.ARRAY, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, 'links', False)
    ]

    def __init__(self):
        self.add_fields(self.SEARCH_ARGS)

    def get_headers(self, verbosity_level=1, formatter='table'):
        """Get headers by verbosity for the AppPermission class
        """
        if verbosity_level is None:
            verbosity_level = Verbosity.LISTING
        if verbosity_level > Verbosity.BRIEF:
            return ['username', 'permission', '_links']
        else:
            return ['username', 'read', 'write', 'execute']

    @classmethod
    def pem_to_row(self, permission):
        """Transforms a 'permission' object into an array of strings

        Values for 'True' and 'False' are defined in constants.PEM_TRUE and
        constants.PEM_FALSE.
        """
        row_data = list()
        for i in ['read', 'write', 'execute']:
            if permission.get(i, False) is True:
                row_data.append(constants.PEM_TRUE)
            else:
                row_data.append(constants.PEM_FALSE)
        return row_data
