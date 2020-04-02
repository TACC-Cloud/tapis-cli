"""Jobs service commands
"""
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION

from .models import Job, API_NAME
from .cancel import JobsCancel
from .hide import JobsHide
from .history import JobsHistory
from .list import JobsList
from .resubmit import JobsResubmit
from .search import JobsSearch
from .show import JobsShow
from .status import JobsStatus
from .submit import JobsSubmit
from .outputs_list import JobsOutputsList
from .outputs_download import JobsOutputsDownload
from .outputs_logs import JobsOutputsLogs
from .pems_list import JobsPemsList
from .pems_show import JobsPemsShow
from .pems_grant import JobsPemsGrant
from .pems_revoke import JobsPemsRevoke
from .pems_drop import JobsPemsDrop
from .unhide import JobsUnhide
from .init import JobsInit
