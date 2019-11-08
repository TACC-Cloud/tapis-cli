from tapis_cli.utils import seconds

__all__ = ['copy', 'delete', 'makedirs', 'move']

DEFAULT_SYSTEM_ID = 'data-tacc-sandbox'


def copy(file_path,
         system_id=DEFAULT_SYSTEM_ID,
         destination=None,
         permissive=False,
         agave=None):
    try:
        if destination is None:
            raise ValueError('Value for "destination" must be provided')
        body = {'action': 'copy', 'path': destination}
        resp = agave.files.manage(body=body,
                                  systemId=system_id,
                                  filePath=file_path)
        return resp
    # TODO - handle 404 differently than other errors
    except Exception:
        if permissive:
            return False
        else:
            raise


def delete(file_path,
           system_id=DEFAULT_SYSTEM_ID,
           permissive=False,
           agave=None):
    try:
        agave.files.delete(filePath=file_path, systemId=system_id)
    # TODO - handle 404 differently than other errors
    except Exception:
        if permissive:
            return False
        else:
            raise


def makedirs(file_path,
             system_id=DEFAULT_SYSTEM_ID,
             destination='/',
             exist_ok=True,
             permissive=False,
             agave=None):
    # TODO - if exist_ok is False, add a check for existence of the remote. Not doing the check is saves an API call and corresponding remote system access, so it's advantageous to avoid it
    try:
        body = {'action': 'mkdir', 'path': file_path}
        resp = agave.files.manage(body=body,
                                  systemId=system_id,
                                  filePath=destination)
        return resp
    # TODO - handle 404 differently than other errors
    except Exception:
        if permissive:
            return False
        else:
            raise


def move(file_path,
         system_id=DEFAULT_SYSTEM_ID,
         destination=None,
         permissive=False,
         agave=None):
    try:
        if destination is None:
            raise ValueError('Value for "destination" must be provided')
        body = {'action': 'move', 'path': destination}
        resp = agave.files.manage(body=body,
                                  systemId=system_id,
                                  filePath=file_path)
        return resp
    # TODO - handle 404 differently than other errors
    except Exception:
        if permissive:
            return False
        else:
            raise
