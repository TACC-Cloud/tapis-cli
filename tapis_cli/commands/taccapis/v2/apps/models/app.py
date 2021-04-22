"""Data model and functions for Tapis apps
"""
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
from tapis_cli.commands.taccapis import TapisModel
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod

__all__ = ['App', 'API_NAME', 'SERVICE_VERSION']

API_NAME = 'apps'


class App(TapisModel):
    """Model of a Tapis application
    """
    service_id_type = 'App'

    SEARCH_ARGS = [
    # WARNING - date search apparently does not work on apps so never make datetime fields searchable
    # JSON_field, type, verbosity, mods_allowed, default_mod, choices, override_option, searchable
        ("id", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("name", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("version", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("revision", argtype.INTEGER, Verbosity.LISTING,
         argmod.NUMBER_DEFAULTS, argmod.NUMBER_DEFAULT_MOD, None, None, True),
        ("label", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("lastModified", argtype.DATETIME, Verbosity.LISTING_VERBOSE,
         argmod.DATE_DEFAULTS, argmod.DATE_DEFAULT_MOD, None, None, False),
        ("shortDescription", argtype.STRING, Verbosity.LISTING,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("longDescription", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("owner", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("isPublic", argtype.BOOLEAN, Verbosity.LISTING, argmod.BOOL_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("executionType", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, ['HPC', 'CLI'], None, True),
        ("executionSystem", argtype.STRING, Verbosity.LISTING,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("deploymentSystem", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("available", argtype.BOOLEAN, Verbosity.RECORD, argmod.BOOL_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("parallelism", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, ['SERIAL',
                                                  'PARALLEL'], None, True),
        ("defaultProcessorsPerNode", argtype.INTEGER, Verbosity.RECORD,
         argmod.NUMBER_DEFAULTS, argmod.NUMBER_DEFAULT_MOD, None, None, True),
        ("defaultMemoryPerNode", argtype.INTEGER, Verbosity.RECORD,
         argmod.NUMBER_DEFAULTS, argmod.NUMBER_DEFAULT_MOD, None, None, True),
        ("defaultNodeCount", argtype.INTEGER, Verbosity.RECORD,
         argmod.NUMBER_DEFAULTS, argmod.NUMBER_DEFAULT_MOD, None, None, True),
        ("defaultMaxRunTime", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("defaultQueue", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("tags", argtype.ARRAY, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("ontology", argtype.ARRAY, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("helpURI", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("deploymentPath", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("templatePath", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("testPath", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("checkpointable", argtype.BOOLEAN, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.BOOL_DEFAULT_MOD, None, None, False),
        ("modules", argtype.ARRAY, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("inputs", argtype.ARRAY, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("parameters", argtype.ARRAY, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("outputs", argtype.ARRAY, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("uuid", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("icon", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("_links", argtype.ARRAY, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, 'links', False)
    ]

    # def __init__(self):
    #     self.add_fields(self.SEARCH_ARGS)

    # def get_headers(self, verbosity_level=None, formatter='table'):
    #     if verbosity_level is None:
    #         verbosity_level = Verbosity.LISTING
    #     headers = list()
    #     for f in self.fields:
    #         # print('{}: {}> = {}'.format(f, verbosity_level, f.verbosity))
    #         if verbosity_level >= f.verbosity:
    #             if argtype.format_allows_param_type(f, formatter):
    #                 headers.append(f.param_name)
    #     return headers
