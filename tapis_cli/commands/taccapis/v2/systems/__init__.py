"""Systems service commands
"""

from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
from .models import System, API_NAME

from .show import SystemsShow
from .list import SystemsList
from .search import SystemsSearch
from .status import SystemsStatus
from .history import SystemsHistory
from .roles_list import SystemsRolesList
from .queues_list import SystemsQueuesList
from .create import SystemsCreate
from .update import SystemsUpdate
from .enable import SystemsEnable
from .disable import SystemsDisable
from .publish import SystemsPublish
from .unpublish import SystemsUnpublish
from .roles_grant import SystemsRolesGrant
from .roles_revoke import SystemsRolesRevoke
from .roles_drop import SystemsRolesDrop
from .roles_show import SystemsRolesShow
from .default_set import SystemsDefaultSet
from .default_unset import SystemsDefaultUnset
