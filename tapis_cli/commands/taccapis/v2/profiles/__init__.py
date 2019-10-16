"""Profiles service commands
"""
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
API_NAME = 'profiles'

from .list import ProfilesList
from .search import ProfilesSearch
from .show import ProfilesShow
from .show_self import ProfilesShowSelf
