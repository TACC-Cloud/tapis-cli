"""Provides config file loading and management
"""
import os
from dotenv import load_dotenv, find_dotenv
import warnings

__all__ = ['find_config', 'load_config']


def find_config(filename='.env'):
    """Wrapper for find_dotenv that searches module path, CWD, and HOME
    """
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        # Default to $HOME
        env_file = os.path.join(os.path.expanduser('~'), filename)
        # But, try find_dotenv to find overrides
        try:
            # Search from __file__ up to /
            env_file = find_dotenv(filename, raise_error_if_not_found=True)
        except (IOError, OSError):
            pass
    return env_file


def load_config(filename='.env', override=False):
    """Wrapper for load_env that considers module path, CWD, and HOME
    """
    file_name = find_config(filename='.env')
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')

        # Load into environment
        try:
            load_dotenv(file_name, override=override)
        except Exception:
            pass

    # Return path to env file so it can be displayed
    return file_name
