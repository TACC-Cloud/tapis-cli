"""Data model and functions for Tapis jobs
"""
import math
from datetime import timedelta
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
from tapis_cli.commands.taccapis import TapisModel
from tapis_cli.display import Verbosity
from tapis_cli.search import argtype, argmod

__all__ = ['Job', 'API_NAME', 'SERVICE_VERSION']

API_NAME = 'jobs'


class Job(TapisModel):
    """Model of a Tapis job
    """
    service_id_type = 'Job'

    SEARCH_ARGS = [
    # JSON_field, type, verbosity, mods_allowed, default_mod, choices, override_option, searchable
        ("_links", argtype.ARRAY, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, 'links', False),
        ("accepted", argtype.DATETIME, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("appId", argtype.STRING, Verbosity.LISTING_VERBOSE,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("appUuid", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("archive", argtype.BOOLEAN, Verbosity.RECORD, argmod.BOOL_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("archiveOnAppError", argtype.BOOLEAN, Verbosity.RECORD,
         argmod.BOOL_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("archivePath", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("archiveSystem", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("blockedCount", argtype.INTEGER, Verbosity.RECORD,
         argmod.NUMBER_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("created", argtype.DATETIME, Verbosity.LISTING_VERBOSE,
         argmod.DATE_DEFAULTS, argmod.DATE_DEFAULT_MOD, None, None, True),
        ("ended", argtype.DATETIME, Verbosity.LISTING_VERBOSE,
         argmod.DATE_DEFAULTS, argmod.DATE_DEFAULT_MOD, None, None, True),
        ("failedStatusChecks", argtype.INTEGER, Verbosity.RECORD,
         argmod.NUMBER_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("id", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("inputs", argtype.OBJECT, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("lastStatusCheck", argtype.DATETIME, Verbosity.LISTING_VERBOSE,
         argmod.DATE_DEFAULTS, argmod.DATE_DEFAULT_MOD, None, None, False),
        ("lastStatusMessage", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("lastUpdated", argtype.DATETIME, Verbosity.LISTING_VERBOSE,
         argmod.DATE_DEFAULTS, argmod.DATE_DEFAULT_MOD, None, None, True),
        ("maxHours", argtype.INTEGER, Verbosity.RECORD, argmod.NUMBER_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("memoryPerNode", argtype.INTEGER, Verbosity.RECORD,
         argmod.NUMBER_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("name", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("nodeCount", argtype.INTEGER, Verbosity.RECORD,
         argmod.NUMBER_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("owner", argtype.STRING, Verbosity.LISTING, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("parameters", argtype.OBJECT, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("processorsPerNode", argtype.INTEGER, Verbosity.RECORD,
         argmod.NUMBER_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("remoteEnded", argtype.DATETIME, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("remoteJobId", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("remoteOutcome", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("remoteQueue", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("remoteStarted", argtype.DATETIME, Verbosity.LISTING_VERBOSE,
         argmod.DATE_DEFAULTS, argmod.DATE_DEFAULT_MOD, None, None, False),
        ("remoteStatusChecks", argtype.INTEGER, Verbosity.RECORD,
         argmod.NUMBER_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("remoteSubmitted", argtype.DATETIME, Verbosity.LISTING_VERBOSE,
         argmod.DATE_DEFAULTS, argmod.DATE_DEFAULT_MOD, None, None, False),
        ("roles", argtype.ARRAY, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("schedulerJobId", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, False),
        ("status", argtype.STRING, Verbosity.BRIEF, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("submitRetries", argtype.INTEGER, Verbosity.RECORD,
         argmod.NUMBER_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("systemId", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("tenantId", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False),
        ("tenantQueue", argtype.STRING, Verbosity.RECORD,
         argmod.STRING_DEFAULTS, argmod.DEFAULT, None, None, True),
        ("visible", argtype.BOOLEAN, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, True),
        ("workPath", argtype.STRING, Verbosity.RECORD, argmod.STRING_DEFAULTS,
         argmod.DEFAULT, None, None, False)
    ]

    TEMPLATE_KEYS = [
        'appId', 'archive', 'archiveSystem', 'maxRunTime', 'inputs',
        'memoryPerNode', 'name', 'nodeCount', 'parameters', 'processorsPerNode'
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

    def get_template_headers(self, verbosity_level=None, formatter='table'):
        """Return only submittable Job fields
        """
        return self.TEMPLATE_KEYS

    @classmethod
    def render_key_value(cls, key, value):
        """Rules for transforming key names and values
        """
        if key == 'memoryPerNode':
            return key, str(math.ceil(value))
        elif key == 'maxHours':
            return 'maxRunTime', maxhours_to_hhmmss(value)
        return key, value


def maxhours_to_hhmmss(max_hours=0.5):
    """Convert Aloe maxHours to Agave-style HH:MM:SS
    """
    d = timedelta(0, hours=max_hours)
    return str(d)
