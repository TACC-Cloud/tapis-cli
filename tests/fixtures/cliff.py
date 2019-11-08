import pytest
from attrdict import AttrDict

__all__ = ['cliff_app', 'parsed_args_gen', 'fn_header_exists', 'fn_key_exists']


@pytest.fixture(scope='function')
def cliff_app():
    from tapis_cli.main import Tapis_App
    app = Tapis_App()


@pytest.fixture(scope='function')
def parsed_args_gen():
    """Returns a function which creates an emulated parsed_args from kwargs
    """
    def generator(**kwargs):
        pdict = {}
        for k, v in kwargs.items():
            pdict[k] = v
        return AttrDict(pdict)

    return generator


@pytest.fixture(scope='function')
def fn_header_exists():
    """Returns a function to determine if a header of a given name exists
    """
    def hexist(headers_tuple, header_name):
        return header_name in headers_tuple

    return hexist


@pytest.fixture(scope='function')
def fn_key_exists():
    """Returns a function for interrogating a tuple response from take_action
    """
    def kexists(data_tuple, data_value, position=None):
        for row in list(data_tuple):
            if data_value in row:
                return True
        return False

    return kexists
