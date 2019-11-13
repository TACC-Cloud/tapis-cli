import configparser
import os

__all__ = ['FILENAMES', 'load_config', 'save_config', 'config_path']

# Other inis might exist but we will only actively try loading from these
FILENAMES = ['app.ini', 'reactor.ini', 'project.ini']
DEFAULT_FILENAME = 'project.ini'


def load_config(filename):
    config = configparser.ConfigParser()
    if os.path.basename(filename) in FILENAMES:
        # Fail gracefully if does not exist
        config.read(filename)
    else:
        raise ValueError(
            'Invalid config file name. Allowed values are: {0}'.format(
                ', '.join(FILENAMES)))
    return config


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
