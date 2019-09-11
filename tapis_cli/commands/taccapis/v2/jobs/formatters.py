"""Formatters customized for job records and listings
"""

from tapis_cli.clients.services.taccapis import (TaccApisCommandBase,
                                                 TaccApisFormatOne,
                                                 TaccApisFormatMany,
                                                 TaccApisFormatManyUnlimited)
from .models import Job

__all__ = ['JobsFormatOne', 'JobsFormatMany', 'JobsHistoryFormatMany']


class JobsBase(TaccApisCommandBase):
    service_id_type = Job.service_id_type


class JobsFormatOne(JobsBase, TaccApisFormatOne):
    pass


class JobsFormatMany(JobsBase, TaccApisFormatMany):
    pass

class JobsHistoryFormatMany(JobsBase, TaccApisFormatManyUnlimited):
    pass
