import pytest
from .fixtures import *


def pytest_addoption(parser):
    parser.addoption('--smoketest',
                     action='store_true',
                     dest='smoketest',
                     default=False,
                     help='Run only developer smoketests')
    parser.addoption('--longrun',
                     action='store_true',
                     dest='longrun',
                     default=False,
                     help='Run tests that can take a long time')


def pytest_runtest_setup(item):
    if item.config.getvalue('smoketest') is True:
        if 'smoketest' not in item.keywords:
            pytest.skip('not a smoketest')
    if 'longrun' in item.keywords and not item.config.getvalue('longrun'):
        pytest.skip('needs --longrun option to run')
