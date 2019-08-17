import pytest
from .fixtures import *

def pytest_addoption(parser):
    parser.addoption('--smoketest', action='store_true', dest='smoketest',
                     default=False, help='Run developer smoktests')
    parser.addoption('--networked', action='store_true', dest='networked',
                     default=False, help='Run tests that require external network access')
    parser.addoption('--longrun', action='store_true', dest='longrun',
                     default=False, help='Run tests that might take a long time')

def pytest_runtest_setup(item):
    if 'smoketest' in item.keywords and not item.config.getvalue('smoketest'):
        pytest.skip('needs --smoketest option to run')
    if 'networked' in item.keywords and not item.config.getvalue('networked'):
        pytest.skip('needs --networked option to run')
    if 'longrun' in item.keywords and not item.config.getvalue('longrun'):
        pytest.skip('needs --longrun option to run')

