"""Representation and helpers for app, system, metadata, job permissions
"""

PEM_POSIX_MAPPING = {
    'NONE': '---',
    'READ': 'r--',
    'WRITE': '-w-',
    'EXECUTE': '--x',
    'READ_WRITE': 'rw-',
    'READ_EXECUTE': 'r-x',
    'WRITE_EXECUTE': '-wx',
    'ALL': 'rwx'
}

__all__ = ['posixify_pem']


def posixify_pem(pem):
    """Translate a Tapis systems, jobs, or apps pem into a POSIX-like string
    """
    return PEM_POSIX_MAPPING.get(pem.upper(), 'r--')
