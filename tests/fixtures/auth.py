"""Read from tests/configuration.json or environment vars
"""
import json
import os
import pytest
from agavepy.agave import Agave

PWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
GPARENT = os.path.dirname(PARENT)
CREDENTIALS = os.path.join(PARENT, 'configuration.json')

ENV_KEY_MAP = [('TEST_TAPIS_API_KEY', 'apikey', None),
               ('TEST_TAPIS_API_SECRET', 'apisecret', None),
               ('TEST_TAPIS_USERNAME', 'username', None),
               ('TEST_TAPIS_PASSWORD', 'password', None),
               ('TEST_TAPIS_BASE_URL', 'apiserver',
                'https://api.tacc.utexas.edu/'),
               ('TEST_TAPIS_TENANT_ID', 'tenantid', 'tacc.prod')]


@pytest.fixture(scope='function')
def credentials():
    try:
        creds = json.load(open(CREDENTIALS, 'r'))
    except Exception:
        creds = dict()
    client = dict()
    for e, k, d in ENV_KEY_MAP:
        client[k] = creds.get(k, os.environ.get(e, d))
    return client


@pytest.fixture(scope='function')
def test_username(credentials):
    return credentials.get('username')


@pytest.fixture(scope='function')
def test_password(credentials):
    return credentials.get('password')


@pytest.fixture(scope='function')
def test_tenant_id(credentials):
    return credentials.get('tenantid')


@pytest.fixture(scope='function')
def test_api_key(credentials):
    return credentials.get('apikey')


@pytest.fixture(scope='function')
def test_api_secret(credentials):
    return credentials.get('apisecret')


@pytest.fixture(scope='function')
def test_api_server(credentials):
    return credentials.get('apiserver')


@pytest.fixture(scope='function')
def test_client(test_api_key, test_api_secret, test_username, test_password,
                test_tenant_id, test_api_server):
    return {
        'TAPIS_API_KEY': test_api_key,
        'TAPIS_API_SECRET': test_api_secret,
        'TAPIS_USERNAME': test_username,
        'TAPIS_PASSWORD': test_password,
        'TAPIS_TENANT_ID': test_tenant_id,
        'TAPIS_BASE_URL': test_api_server
    }


@pytest.fixture(scope='function')
def tapis_active_client(test_client):
    return Agave(**test_client).restore()


@pytest.fixture(scope='function')
def temp_cache_env(temp_cache, monkeypatch):
    """Set credentials cache to a temp directory
    """
    monkeypatch.setenv('TAPIS_CACHE_DIR', temp_cache)
    return temp_cache


@pytest.fixture(scope='function')
def temp_cache_b_env(temp_cache_b, monkeypatch):
    """Set credentials cache to a temp directory
    """
    monkeypatch.setenv('TAPIS_CACHE_DIR', temp_cache_b)
    return temp_cache_b


@pytest.fixture(scope='function')
def temp_testing_env(test_client, temp_cache_env, monkeypatch):
    """Configure client with test credentials and temp dir
    """
    for k, v in test_client.items():
        monkeypatch.setenv(k, v)
