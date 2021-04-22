import configparser
import os

__all__ = [
    'FILENAMES', 'DEFAULT_FILENAME', 'load_config', 'save_config',
    'config_path'
]

# Other inis might exist but we will only actively try loading from these
FILENAMES = ['app.ini', 'actor.ini', 'project.ini', 'reactor.ini']
DEFAULT_FILENAME = 'project.ini'


def load_config(filename=None, as_dict=False):
    if filename is None:
        filename = config_path()
    else:
        # Fail if filename is passed but does not exist
        if not os.path.exists(filename):
            raise FileNotFoundError('{0} was not found'.format(filename))
    if os.path.basename(filename) in FILENAMES:
        # Fail gracefully if does not exist
        config = configparser.ConfigParser()
        # Preserve case when reading from ini file - this is needed to support
        # loading and using the [environments] stanza as shell variables are
        # most decidedly case-sensitive!
        # Source: https://stackoverflow.com/a/63067604
        config.optionxform = str
        config.read(filename)
        if as_dict is False:
            return config
        else:
            dict_config = {}
            for section in config.sections():
                for k, v in config.items(section):
                    if section not in dict_config:
                        dict_config[section] = {}
                    dict_config[section][k] = v
            return dict_config

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


def config_path(filename=None, working_directory=None):
    if working_directory is None:
        working_directory = os.getcwd()

    if filename is not None:
        return filename
    else:
        for fname in FILENAMES:
            ipath = os.path.join(working_directory, fname)
            if os.path.exists(ipath):
                return ipath

        return os.path.join(working_directory, DEFAULT_FILENAME)
