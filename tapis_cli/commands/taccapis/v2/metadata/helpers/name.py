import hashlib
import json
import random
import string
from tapis_cli.utils import timestamp

HASH_LENGTH = 16

__all__ = ['generate_name']


def random_hex(length=HASH_LENGTH):
    """Generate a random string of lowercase and uppercase letters
    """
    letters = string.hexdigits
    return ''.join(random.choice(letters).lower() for i in range(length))


def generate_name(username=None, data=None):
    """Deterministically generate a name for a metadata document
    """
    # username.hash(data).timestamp

    id_els = []
    if username is not None:
        id_els.append(username)

    if data is None:
        hashed = random_hex()
    else:
        s = json.dumps(data, indent=None, sort_keys=True)
        hashed = hashlib.sha256(s.encode('utf-8')).hexdigest()[:HASH_LENGTH]
    id_els.append(hashed)

    id_els.append(timestamp())
    return '.'.join(id_els)
