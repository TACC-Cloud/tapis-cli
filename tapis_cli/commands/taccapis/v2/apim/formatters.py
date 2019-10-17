"""Formatters customized for token, client, and client subscription responses
"""
from tapis_cli.commands.taccapis.formatters import (TaccApisCommandBase,
                                                    TaccApisFormatOne,
                                                    TaccApisFormatMany,
                                                    TaccApisFormatOneNoBearer)

# from tapis_cli.clients.services.taccapis import (TaccApisCommandBase,
#                                                  TaccApisFormatOne,
#                                                  TaccApisFormatMany,
#                                                  TaccApisFormatOneNoBearer)

from .models import Token

__all__ = ['TokenFormatOne', 'CreateTokenFormatOne']


class TokensBase(TaccApisCommandBase):
    id_display_name = Token.id_display_name


class TokenFormatOne(TokensBase, TaccApisFormatOne):
    pass


class CreateTokenFormatOne(TokensBase, TaccApisFormatOneNoBearer):
    pass
