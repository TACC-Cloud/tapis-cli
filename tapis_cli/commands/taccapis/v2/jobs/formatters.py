"""Formatters customized for job records and listings
"""

from tapis_cli.commands.taccapis.formatters import (
    TaccApisCommandBase, TaccApisFormatOne, TaccApisFormatMany,
    TaccApisFormatManyUnlimited)
from .models import Job

__all__ = [
    'JobsFormatOne', 'JobsFormatMany', 'JobsHistoryFormatMany',
    'JobsFormatManyUnlimited'
]


class JobsBase(TaccApisCommandBase):
    # Aloe /jobs return UTC whereas other Agave and Abaco
    # services return CDT. This overrides value rendering
    # to account for the difference in implementation
    # between the services
    TIMEZONE = 'UTC'


class JobsFormatOne(JobsBase, TaccApisFormatOne):
    pass


class JobsFormatMany(JobsBase, TaccApisFormatMany):
    pass


class JobsFormatManyUnlimited(JobsBase, TaccApisFormatManyUnlimited):
    pass


class JobsHistoryFormatMany(JobsBase, TaccApisFormatManyUnlimited):
    pass
