
__all__ = ['default_execution_system', 'default_storage_system']

def default_execution_system(agave, public_only=False):
    resp = agave.systems.list(default=True, limit=1, offset=0, public=public_only, type='EXECUTION')
    if isinstance(resp, list):
        return resp[0]

def default_storage_system(agave, public_only=False):
    resp = agave.systems.list(default=True, limit=1, offset=0, public=public_only, type='STORAGE')
    if isinstance(resp, list):
        return resp[0]

