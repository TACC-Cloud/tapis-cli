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
          grant_system_roles=True,
          permissive=False,
          agave=None,
          **kwargs):
    """Helper to grant permission on a Tapis app
    """
    body = {'username': username, 'permission': permission.upper()}
    try:
        grant_result = agave.apps.updateApplicationPermissions(appId=app_id,
                                                               body=body)

        # Grant roles on system(s) as well - I wish we didn't have to do this
        if permission.upper() in [
                'ALL', 'READ_EXECUTE', 'WRITE_EXECUTE', 'EXECUTE'
        ]:
            if grant_system_roles:
                app_def = agave.apps.get(appId=app_id)
                systems = [
                    app_def['executionSystem'], app_def['deploymentSystem']
                ]
                for s in systems:

                    # Do not overwrite existing role for user
                    try:
                        existing_role = agave.systems.getRoleForUser(
                            systemId=s, username=username)['role']
                    except Exception:
                        existing_role = None

                    if existing_role is None:
                        role_body = {'username': username, 'role': 'USER'}
                        try:
                            agave.systems.updateRole(systemId=s,
                                                     body=role_body)
                        except Exception:
                            pass
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
