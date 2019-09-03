"""Profiles service commands
"""
from .. import SERVICE_VERSION
API_NAME = 'profiles'

from .list import ProfilesList
from .search import ProfilesSearch
from .show import ProfilesShow
from .show_self import ProfilesShowSelf
