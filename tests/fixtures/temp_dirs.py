import os
import pytest
from tempfile import mkdtemp

__all__ = ['temp_dir', 'temp_cache', 'temp_cache_alternate']


@pytest.fixture(scope='session')
def temp_dir():
    """Alternative to pytest's temporary directory function
    """
    return mkdtemp(prefix='tapis-cli-', suffix='-tests')


@pytest.fixture(scope='session')
def temp_cache():
    """Alternative to pytest's temporary directory function
    """
    return mkdtemp(prefix='tapis-cli-', suffix='-cache')


@pytest.fixture(scope='session')
def temp_cache_alternate():
    """Alternative to pytest's temporary directory function
    """
    return mkdtemp(prefix='tapis-cli-', suffix='-cache-alternate')
