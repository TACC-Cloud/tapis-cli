"""Manages cache of current Abaco actor ID
"""
import os

IDFILE = '.actorid'
FILENAMES = [IDFILE, '.ACTOR_ID']


def read_id(filename=None):
    """Read from cache
    """
    try:
        with open(get_cachefile(filename), 'r') as cache:
            lines = cache.readlines()
            actorid = lines[0].strip()
            validate(actorid, permissive=False)
            return actorid
    except Exception:
        actorid = None
        return actorid


def write_id(actor_id, filename=IDFILE):
    """Write to cache
    """
    if validate(actor_id, permissive=True):
        with open(filename, 'w') as cache:
            cache.write(actor_id)
            return True
    else:
        return False


def get_cachefile(filename=None):
    """Resolve cachefile path
    """
    if filename is None:
        for f in FILENAMES:
            if os.path.exists(f):
                return f
        return IDFILE
    else:
        return filename


def validate(actor_id, permissive=True):
    """Validate actorId
    """
    # TODO - validate against Abaco hashid
    try:
        if not isinstance(actor_id, str):
            raise TypeError('Actor ID must be a <str>')
        if len(actor_id) > 14 or len(actor_id) < 13:
            raise ValueError('Invalid actorId')
        if actor_id.isalnum() is False:
            raise ValueError('Invalid actorId')
        return True
    except Exception:
        if permissive:
            return False
        else:
            raise
