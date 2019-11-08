import pytest
from .data import clients as clients_data


@pytest.mark.smoketest
def test_taccapis_direct_client_init(tapis_active_client):
    from tapis_cli.clients.services.taccapis.v2.direct import TaccApiDirectClient
    t = TaccApiDirectClient(tapis_active_client)
    # Check user agent, which is not set until access token is processed
    assert t.user_agent is not None


@pytest.mark.smoketest
def test_taccapis_direct_client_setup_no_path(tapis_active_client):
    from tapis_cli.clients.services.taccapis.v2.direct import TaccApiDirectClient
    t = TaccApiDirectClient(tapis_active_client)
    t.setup('generic', 'v3')
    url = t.build_url()
    assert 'generic/v3' in url


@pytest.mark.smoketest
def test_taccapis_direct_client_setup_with_path(tapis_active_client):
    from tapis_cli.clients.services.taccapis.v2.direct import TaccApiDirectClient
    t = TaccApiDirectClient(tapis_active_client)
    t.setup('generic', 'v3', 'details')
    url = t.build_url()
    assert 'generic/v3/details' in url


@pytest.mark.smoketest
def test_taccapis_direct_client_build_url_args(tapis_active_client):
    """Test build_url with arbitrary number of additional path elements
    """
    from tapis_cli.clients.services.taccapis.v2.direct import TaccApiDirectClient
    t = TaccApiDirectClient(tapis_active_client)
    t.setup('generic', 'v3', 'details')
    url = t.build_url('storage', 'is', 'managed', 'by', 'files', 'service')
    assert url.endswith('/service')
