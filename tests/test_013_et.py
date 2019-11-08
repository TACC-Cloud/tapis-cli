import pytest
import validators


def test_phone_home_url():
    """Check that a valid URL is generated at run-time
    """
    from tapis_cli import et
    assert validators.url(et.generate_tracking_url()) is True
