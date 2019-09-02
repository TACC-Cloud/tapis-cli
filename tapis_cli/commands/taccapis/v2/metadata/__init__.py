"""Metadata service commands
"""
from .. import SERVICE_VERSION
API_NAME = 'meta'

from .list import MetadataList
from .show import MetadataShow
from .search import MetadataSearch
