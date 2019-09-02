"""Profiles service commands
"""
from .. import SERVICE_VERSION
API_NAME = 'profiles'

# from .list import MetadataList
# from .search import MetadataSearch
from .show import ProfilesShow
from .show_self import ProfilesShowSelf
