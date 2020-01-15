"""Apps service commands
"""

from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
from .models import App, API_NAME

from .show import AppsShow
from .list import AppsList
from .search import AppsSearch
from .enable import AppsEnable
from .disable import AppsDisable
from .history import AppsHistory
from .create import AppsCreate
from .update import AppsUpdate
from .pems_list import AppsPemsList
from .pems_show import AppsPemsShow
from .pems_grant import AppsPemsGrant
from .pems_revoke import AppsPemsRevoke
# The apps.deletePermissions method returns a 500 so command is disabled
# from .pems_drop import AppsPemsDrop
from .clone import AppsClone
from .publish import AppsPublish
from .unpublish import AppsUnpublish

# Workflows
from .deploy import AppsDeploy
from .init import AppsInit
