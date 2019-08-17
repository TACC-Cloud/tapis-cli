import pytest

@pytest.mark.smoketest
def test_can_import_mod():
    import tapis_cli

@pytest.mark.smoketest
def test_datacalog_about_version():
    from tapis_cli import __about__ as about
    assert about.__version__ is not None
