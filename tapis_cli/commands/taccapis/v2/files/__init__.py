"""Files service commands
"""
from .. import SERVICE_VERSION
from .models import File, API_NAME

from .download import FilesDownload
from .list import FilesList
from .show import FilesShow
from .upload import FilesUpload
