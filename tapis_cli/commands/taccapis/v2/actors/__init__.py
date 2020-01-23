"""Abaco commands
"""
# from .. import SERVICE_VERSION
API_NAME = 'actors'
SERVICE_VERSION = 'v2'

from .list import ActorsList
from .show import ActorsShow
from .delete import ActorsDelete
from .pems_list import ActorsPemsList
from .pems_grant import ActorsPemsGrant
from .pems_revoke import ActorsPemsRevoke
from .pems_show import ActorsPemsShow
