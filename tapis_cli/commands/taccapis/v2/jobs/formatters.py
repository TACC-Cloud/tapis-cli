"""Formatters customized for job records and listings
"""

from tapis_cli.commands.taccapis.formatters import (
    TaccApisCommandBase, TaccApisFormatOne, TaccApisFormatMany,
    TaccApisFormatManyUnlimited)
from .models import Job

__all__ = ['JobsFormatOne', 'JobsFormatMany', 'JobsHistoryFormatMany']


class JobsBase(TaccApisCommandBase):
    pass


class JobsFormatOne(JobsBase, TaccApisFormatOne):
    pass


class JobsFormatMany(JobsBase, TaccApisFormatMany):
    pass


class JobsHistoryFormatMany(JobsBase, TaccApisFormatManyUnlimited):
    pass
