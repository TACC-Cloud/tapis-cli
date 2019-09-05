"""Formatters customized for job records and listings
"""
from tapis_cli.clients.services.taccapis import (TaccApisBase,
                                                 TaccApisFormatOne,
                                                 TaccApisFormatMany,
                                                 TaccApisFormatManyUnlimited)
from .models import Job

__all__ = ['JobsFormatOne', 'JobsFormatMany', 'JobsHistoryFormatMany']


class JobsBase(TaccApisBase):
    id_display_name = Job.id_display_name


class JobsFormatOne(TaccApisFormatOne, JobsBase):
    pass


class JobsFormatMany(TaccApisFormatMany, JobsBase):
    pass


class JobsHistoryFormatMany(TaccApisFormatManyUnlimited, JobsBase):
    pass
