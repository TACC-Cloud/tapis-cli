"""Data model and functions for Tapis files
"""
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
from tapis_cli.commands.taccapis import TapisModel
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod

__all__ = ['File', 'API_NAME']

API_NAME = 'files'


class File(TapisModel):
    """Model of a Tapis file
    """
    service_id_type = 'File'
    payload = dict()

    SEARCH_ARGS = [
    # JSON_field, type, verbosity, mods_allowed, default_mod, choices, override_option, searchable
        ("_links", argtype.ARRAY, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, 'links', False),
        ("name", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("path", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("lastModified", argtype.DATETIME, Verbosity.BRIEF,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("length", argtype.INTEGER, Verbosity.BRIEF, argmod.NUMBER_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("permissions", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("mimeType", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("type", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("system", argtype.STRING, Verbosity.RECORD_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False)
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
