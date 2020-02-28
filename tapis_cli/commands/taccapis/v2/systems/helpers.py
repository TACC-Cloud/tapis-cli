__all__ = ['default_execution_system', 'default_storage_system']


def default_execution_system(agave, public_only=False):
    """Determines a default execution system for the current user

    Resolves private default, followed by public default, or None
    """
    if not public_only:
        try:
            resp = agave.systems.list(default=True,
                                      limit=1,
                                      offset=0,
                                      public=False,
                                      type='EXECUTION')
            if len(resp) > 0:
                return resp[0].get('id', None)
        except Exception:
            pass

    try:
        resp = agave.systems.list(default=True,
                                  limit=1,
                                  offset=0,
                                  public=True,
                                  type='EXECUTION')
        if len(resp) > 0:
            return resp[0].get('id', None)
    except Exception:
        pass

    return None


def default_storage_system(agave, public_only=False):
    """Determines a default storage system for the current user

    Resolves private default, followed by public default, or None
    """
    if not public_only:
        try:
            resp = agave.systems.list(default=True,
                                      limit=1,
                                      offset=0,
                                      public=False,
                                      type='STORAGE')
            if len(resp) > 0:
                return resp[0].get('id', None)
        except Exception:
            pass

    try:
        resp = agave.systems.list(default=True,
                                  limit=1,
                                  offset=0,
                                  public=True,
                                  type='STORAGE')
        if len(resp) > 0:
            return resp[0].get('id', None)
    except Exception:
        pass

    return None
