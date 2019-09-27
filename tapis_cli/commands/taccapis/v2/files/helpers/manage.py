from tapis_cli.utils import seconds

__all__ = ['makedirs', 'delete']


def makedirs(file_path,
             system_id,
             destination='/',
             exist_ok=True,
             permissive=False,
             agave=None):
    # TODO - if exist_ok is False, add a check for existence of the remote. Not doing the check is saves an API call and corresponding remote system access, so it's advantageous to avoid it
    try:
        body = {'action': 'mkdir', 'path': file_path}
        agave.files.manage(body=body, systemId=system_id, filePath=destination)
        return True
    except Exception:
        if permissive:
            return False
        else:
            raise


def delete(file_path, system_id, permissive=False, agave=None):
    try:
        agave.files.delete(filePath=file_path, systemId=system_id)
    except Exception:
        if permissive:
            return False
        else:
            raise
