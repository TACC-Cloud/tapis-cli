import pytest

__all__ = ['testing_envs']

@pytest.fixture(scope='session')
def testing_envs(monkeypatch):
    monkeypatch.setenv("PAGE_SIZE", "10")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("RESPONSE_FORMAT", "json")
    monkeypatch.setenv("TENANT_DNS_DOMAIN", "tacc.dev")
    monkeypatch.setenv("RESPONSE_FORMAT", "json")
    monkeypatch.setenv("TACC_PROJECT_NAME", "SANDBOX")
