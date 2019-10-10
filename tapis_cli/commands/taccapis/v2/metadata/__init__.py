"""Metadata service commands
"""
from .. import SERVICE_VERSION
API_NAME = 'meta'

from .create import MetadataCreate
from .delete import MetadataDelete
from .list import MetadataList
from .show import MetadataShow
from .search import MetadataSearch
from .update import MetadataUpdate
