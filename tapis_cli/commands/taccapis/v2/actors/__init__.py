"""Abaco commands
"""
# from .. import SERVICE_VERSION
API_NAME = 'actors'
SERVICE_VERSION = 'v2'

from .init import ActorsInit
from .list import ActorsList
from .show import ActorsShow
from .delete import ActorsDelete
from .pems_list import ActorsPemsList
from .pems_grant import ActorsPemsGrant
from .pems_revoke import ActorsPemsRevoke
from .pems_show import ActorsPemsShow
from .execs_show import ActorsExecsShow
from .execs_list import ActorsExecsList
from .execs_logs import ActorsExecsLogs
from .execs_stop import ActorsExecsStop
from .workers_list import ActorsWorkersList
from .workers_show import ActorsWorkersShow
from .workers_delete import ActorsWorkersDelete
from .workers_create import ActorsWorkersCreate
from .aliases_show import ActorsAliasesShow
from .aliases_delete import ActorsAliasesDelete
from .aliases_list import ActorsAliasesList
from .aliases_create import ActorsAliasesCreate
from .aliases_update import ActorsAliasesUpdate
from .nonces_show import ActorsNoncesShow
from .nonces_list import ActorsNoncesList
from .nonces_delete import ActorsNoncesDelete
from .nonces_create import ActorsNoncesCreate
from .submit import ActorsSubmit
from .run import ActorsRun
from .deploy import ActorsDeploy

from .manage import ActorsCreate, ActorsUpdate
