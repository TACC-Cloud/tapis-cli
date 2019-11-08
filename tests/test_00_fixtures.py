import pytest


@pytest.mark.smoketest
def test_get_test_name(request):
    assert request.node.name == 'test_get_test_name'


@pytest.mark.smoketest
def test_parsed_args_gen(parsed_args_gen):
    """Fixture exists
    """
    pass


@pytest.mark.smoketest
def test_parsed_args_gen_kwargs(parsed_args_gen):
    """Generates proper parsed_args emulatory object from kwargs
    """
    parsed_args = parsed_args_gen(identifier='abcde1234')

    # Has attribute
    assert getattr(parsed_args, 'identifier')
    # Attribute populated
    assert getattr(parsed_args, 'identifier') is not None
    # Attribute is correct
    assert parsed_args.identifier == 'abcde1234'
    # No other attrs
    try:
        getattr(parsed_args, 'dummy')
    except AttributeError:
        pass
