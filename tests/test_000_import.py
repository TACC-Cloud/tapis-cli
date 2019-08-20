import pytest


@pytest.mark.smoketest
def test_can_import_mod():
    import tapis_cli


@pytest.mark.smoketest
@pytest.mark.parametrize('attribute,accept_none,expect_exception',
                         [('title', False, False), ('url', False, True)])
def test_about(attribute, accept_none, expect_exception):
    from tapis_cli import About

    def test_code():
        a = About()
        val = getattr(a, attribute)
        if val is None and not accept_none:
            raise ValueError('{} cannot be None'.format(attribute))
