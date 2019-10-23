"""Metadata service commands
"""
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
API_NAME = 'meta'

from .create import MetadataCreate
from .delete import MetadataDelete
from .list import MetadataList
from .show import MetadataShow
from .search import MetadataSearch
from .update import MetadataUpdate
from .pems_list import MetadataPemsList
from .pems_show import MetadataPemsShow
from .pems_grant import MetadataPemsGrant
from .pems_revoke import MetadataPemsRevoke
from .pems_drop import MetadataPemsDrop
