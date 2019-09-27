__all__ = ['makedirs']


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
