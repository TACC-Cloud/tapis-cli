import os
from tapis_cli.utils import (get_local_username, get_hostname, get_public_ip,
                             getfqdn)

__all__ = ['key_values']


def key_values():
    facts = dict()
    facts['homedir'] = os.path.expanduser('~')
    facts['cwd'] = os.getcwd()
    facts['posix_username'] = get_local_username()
    facts['hostname'] = get_hostname()
    facts['fqdn'] = getfqdn()
    facts['public_ip'] = get_public_ip()
    return facts
