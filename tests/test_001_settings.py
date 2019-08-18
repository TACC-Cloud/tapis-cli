import pytest
from .data import settings as settings_data

@pytest.mark.smoketest
def test_envs_are_settings(testing_envs):
    from tapis_cli import settings
    for k, v in settings_data.ENVS_AND_VALS:
        vv = getattr(settings, k)
        assert v == vv, \
            'Env {} not propagated as a setting'.format(k)
