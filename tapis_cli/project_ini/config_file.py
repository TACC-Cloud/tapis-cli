import configparser
import os

__all__ = [
    'FILENAMES', 'DEFAULT_FILENAME', 'load_config', 'save_config',
    'config_path'
]

# Other inis might exist but we will only actively try loading from these
FILENAMES = ['app.ini', 'reactor.ini', 'project.ini']
DEFAULT_FILENAME = 'project.ini'


def load_config(filename=None):
    if filename is None:
        filename = config_path()
    else:
        # Fail if filename is passed but does not exist
        if not os.path.exists(filename):
            raise FileNotFoundError('{0} was not found'.format(filename))
    if os.path.basename(filename) in FILENAMES:
        # Fail gracefully if does not exist
        config = configparser.ConfigParser()
        config.read(filename)
        return config
    else:
        raise ValueError(
            'Invalid config file name. Allowed values are: {0}'.format(
                ', '.join(FILENAMES)))


def save_config(config, filename=DEFAULT_FILENAME):
    if os.path.basename(filename) in FILENAMES:
        with open(filename, 'w') as f:
            config.write(f)
    else:
        raise ValueError(
            'Invalid config file name. Allowed values are: {0}'.format(
                ', '.join(FILENAMES)))


def config_path(filename=None):
    if filename is not None:
        return filename
    else:
        return os.path.join(os.getcwd(), DEFAULT_FILENAME)
