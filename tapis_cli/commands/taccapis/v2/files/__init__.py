"""Files service commands
"""
from tapis_cli.commands.taccapis.v2 import SERVICE_VERSION
from .models import File, API_NAME

from .copy import FilesCopy
from .delete import FilesDelete
from .download import FilesDownload
from .history import FilesHistory
from .list import FilesList
from .mkdir import FilesMakeDir
from .move import FilesMove
from .show import FilesShow
from .upload import FilesUpload
from .pems_list import FilesPemsList
from .pems_show import FilesPemsShow
from .pems_grant import FilesPemsGrant
from .pems_revoke import FilesPemsRevoke
from .pems_drop import FilesPemsDrop
