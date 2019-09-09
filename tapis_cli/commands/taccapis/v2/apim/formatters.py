"""Formatters customized for token, client, and client subscription responses
"""
from tapis_cli.clients.services.taccapis import (TaccApisBase,
                                                 TaccApisFormatOne,
                                                 TaccApisFormatMany,
                                                 TaccApisFormatManyUnlimited,
                                                 TaccApisWithRefreshFormatOne)
# RefreshBearerTokenFormatOne

from .models import Token

__all__ = ['TokenFormatOne']


class TokensBase(object):
    id_display_name = Token.id_display_name


class TokenFormatOne(TaccApisWithRefreshFormatOne):
    pass
