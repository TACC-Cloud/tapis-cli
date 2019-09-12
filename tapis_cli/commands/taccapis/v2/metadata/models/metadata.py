"""Data model and functions for Tapis apps
"""
from .. import SERVICE_VERSION
from tapis_cli.commands.taccapis import TapisModel
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod

__all__ = ['Metadata', 'API_NAME', 'SERVICE_VERSION']

API_NAME = 'meta'


class Metadata(TapisModel):
    """Model of a Tapis metadata record
    """
    service_id_type = 'Unique'
    payload = dict()

    SEARCH_ARGS = [
        # JSON_field, type, verbosity, mods_allowed, default_mod, choices, override_option, searchable
        ("uuid", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("schemaId", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("internalUsername", argtype.STRING, Verbosity.EXPANDED,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("owner", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("associationIds", argtype.ARRAY, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("name", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("value", argtype.OBJECT, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("created", argtype.DATETIME, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("lastUpdated", argtype.DATETIME, Verbosity.LISTING,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("_links", argtype.ARRAY, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, 'links', False)
    ]

    def __init__(self):
        self.add_fields(self.SEARCH_ARGS)

    def get_headers(self, verbosity_level=None, formatter='table'):
        if verbosity_level is None:
            verbosity_level = Verbosity.LISTING
        headers = list()
        for f in self.fields:
            # print('{}: {}> = {}'.format(f, verbosity_level, f.verbosity))
            if verbosity_level >= f.verbosity:
                if argtype.format_allows_param_type(f, formatter):
                    headers.append(f.param_name)
        return headers
