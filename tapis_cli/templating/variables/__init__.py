from tapis_cli.utils import dynamic_import

__all__ = ['key_values']

IMPORTS = ['cli', 'date_time', 'git', 'posix']


def key_values():
    kvals = dict()
    for i in IMPORTS:
        a = dynamic_import('tapis_cli.templating.variables.{}'.format(i))
        d = a.key_values()
        kvals.update(d)
    return kvals
