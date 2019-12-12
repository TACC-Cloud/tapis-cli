from tapis_cli.utils import seconds

__all__ = ['list, ' 'grant', 'revoke', 'drop']


def list(app_id, permissive=False, agave=None, **kwargs):
    """Helper to list permissions
    """
    try:
        results = agave.apps.listPermissions(appId=app_id)
        return results
    except Exception:
        if permissive:
            return {}
        else:
            raise


def grant(app_id,
          username,
          permission,
          permissive=False,
          agave=None,
          **kwargs):
    """Helper to grant permission on a Tapis app
    """
    body = {'username': username, 'permission': permission.upper()}
    try:
        grant_result = agave.apps.updateApplicationPermissions(appId=app_id,
                                                               body=body)
        return grant_result
    except Exception:
        if permissive:
            return {}
        else:
            raise


def revoke(app_id, username, permissive=False, agave=None, **kwargs):
    pass


def drop(app_id, permissive=False, agave=None, **kwargs):
    pass
