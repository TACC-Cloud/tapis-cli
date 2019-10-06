"""Data model and functions for Tapis apps
"""
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod
from tapis_cli import constants
from . import TapisModel

__all__ = ['Permission']


class Permission(TapisModel):
    """Model of a Tapis permission
    """

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

    def get_headers(self, verbosity_level=1, formatter='table'):
        """Custom headers by verbosity for AppPermission
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
