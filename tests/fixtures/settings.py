import pytest
from ..data import settings

__all__ = ['testing_envs']


@pytest.fixture(scope='function')
def testing_envs(monkeypatch):
    for k, v in settings.ENVS_AND_VALS:
        monkeypatch.setenv(k, v)
