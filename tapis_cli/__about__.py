import os.path

# As per https://packaging.python.org/guides/single-sourcing-package-version/
# Example 3, warehouse
# https://github.com/pypa/warehouse/blob/64ca42e42d5613c8339b3ec5e1cb7765c6b23083/warehouse/__about__.py

__all__ = [
    "__title__",
    "__project__",
    "__summary__",
    "__uri__",
    "__version__",
    "__sub_version__",
    "__commit__",
    "__author__",
    "__email__",
    "__license__",
    "__copyright__",
]

try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_dir = None

__title__ = 'tapis_cli'
__project__ = 'Tapis CLI'
__summary__ = 'Command line tools to support TACC Tapis {}'.format(__project__)
__uri__ = 'https://github.com/TACC-Cloud/tapis-cli-ng'
__version__ = '0.0.1'
__sub_version__ = '-dev'

if base_dir is not None and os.path.exists(os.path.join(base_dir, ".commit")):
    with open(os.path.join(base_dir, ".commit")) as fp:
        __commit__ = fp.read().strip()
else:
    __commit__ = None

__author__ = ','.join([
    'Matthew Vaughn',
    'Erik Ferlanti',
    'John Fonner',
    'William Allen']
)
__email__ = "tapis-help@tacc.cloud"

__license__ = "BSD-3"
__copyright__ = "2019- %s" % __author__


def version(*args, **kwargs):
    return __title__ + '.' + str(__version__)
