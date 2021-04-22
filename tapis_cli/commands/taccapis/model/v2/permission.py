"""Data model and functions for Tapis apps
"""
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod
from tapis_cli import constants
from . import TapisModel

__all__ = ['Permission', 'AbacoPermission']


class Permission(TapisModel):
    """Model of a Tapis permission
    """

    NAMES = [
        'ALL', 'READ', 'WRITE', 'READ_WRITE', 'EXECUTE', 'READ_EXECUTE',
        'WRITE_EXECUTE', 'NONE'
    ]

    PEM_POSIX_MAPPING = {
        'NONE': '---',
        'READ': 'r--',
        'WRITE': '-w-',
        'EXECUTE': '--x',
        'READ_WRITE': 'rw-',
        'READ_EXECUTE': 'r-x',
        'WRITE_EXECUTE': '-wx',
        'ALL': 'rwx'
    }

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
    def pem_to_row(cls, permission):
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

    @classmethod
    def pem_to_unix(cls, permission):
        """Returns a UNIX shell representation of a Tapis permission
        """
        return cls.PEM_POSIX_MAPPING.get(permission.upper(), '---')

    @classmethod
    def validate(cls, permission, permissive=False):
        if permission in cls.NAMES:
            return True
        else:
            if permissive:
                return False
            else:
                raise ValueError(
                    '{0} not a valid Permission'.format(permission))


class AbacoPermission(TapisModel):
    """Model of an Abaco permission
    """

    NAMES = ['READ', 'EXECUTE', 'UPDATE', 'NONE']

    SEARCH_ARGS = [
    # JSON_field, type, verbosity, mods_allowed, default_mod, choices, override_option, searchable
        ("result", argtype.ARRAY, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("message", argtype.OBJECT, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("status", argtype.OBJECT, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, 'links', False)
    ]

    def get_headers(self, verbosity_level=1, formatter='table'):
        """Custom headers by verbosity for ActorPermission
        """
        if verbosity_level is None:
            verbosity_level = Verbosity.LISTING
        if verbosity_level > Verbosity.BRIEF:
            return ['username', 'permission', 'status']
        else:
            return ['username', 'permission']

    @classmethod
    def validate(cls, permission, permissive=False):
        if permission in cls.NAMES:
            return True
        else:
            if permissive:
                return False
            else:
                raise ValueError(
                    '{0} not a valid Permission'.format(permission))
