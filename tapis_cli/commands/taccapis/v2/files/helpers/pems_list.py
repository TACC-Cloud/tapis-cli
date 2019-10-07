from tapis_cli.utils import (abspath, splitall)

DEFAULT_SYSTEM_ID = 'data-tacc-sandbox'
DEFAULT_PAGE_SIZE = 200

__all__ = ['pems_list']


def pems_list(file_path,
              system_id=DEFAULT_SYSTEM_ID,
              limit=DEFAULT_PAGE_SIZE,
              offset=0,
              root_dir='/',
              permissive=False,
              agave=None,
              **kwargs):
    try:
        resp = agave.files.listPermissions(systemId=system_id,
                                           filePath=file_path,
                                           limit=limit,
                                           offset=offset)
        # This fixes an issue with files.listPermissions where the topmost
        # path element is returned as a username. This is probably a service-
        # level bug, rather than an AgavePy defect
        top_dir = splitall(abspath(file_path, root_dir))[1]
        pems = [p for p in resp if p['username'] != top_dir]
        return pems
    except Exception:
        if permissive:
            return []
        else:
            raise
