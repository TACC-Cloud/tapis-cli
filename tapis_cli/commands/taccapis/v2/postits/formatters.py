"""Formatters customized for postit records and listings
"""
from tapis_cli.commands.taccapis.formatters import (
    TaccApisCommandBase, TaccApisFormatOne, TaccApisFormatMany,
    TaccApisFormatManyUnlimited)
from .models import PostIt

__all__ = ['PostItsFormatOne', 'PostItsFormatMany']


class PostItsBase(TaccApisCommandBase):
    service_id_type = PostIt.service_id_type


class PostItsFormatOne(PostItsBase, TaccApisFormatOne):
    pass


class PostItsFormatMany(PostItsBase, TaccApisFormatManyUnlimited):
    pass
