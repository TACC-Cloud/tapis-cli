"""Data model and functions for Tapis Alias
"""
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
from tapis_cli.commands.taccapis import TapisModel
from tapis_cli.display import Verbosity

__all__ = ['Alias']

class Alias(TapisModel):
    service_id_type = 'Alias'
    FILTERABLE_KEYS = ['owner']
    SEARCH_ARGS = []
