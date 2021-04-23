"""Exceptions and error handlers
"""
import logging
import re
import os
import time
from agavepy.agave import AgaveError
from attrdict import AttrDict
from requests.exceptions import HTTPError

__all__ = [
    'AgaveError', 'HTTPError', 'HTTPNotFoundError', 'TapisOperationFailed',
    'ImportNotCompleteError', 'FileExcludedError', 'read_tapis_http_error',
    'handle_http_error'
]


class FileExcludedError(IOError):
    pass


class TapisOperationFailed(AgaveError):
    pass


class HTTPNotFoundError(HTTPError):
    pass


class ImportNotCompleteError(HTTPNotFoundError):
    pass


def read_tapis_http_error(http_error_object):
    """Extract useful details from an exception raised by interactting
    with a Tapis API
    """
    h = http_error_object
    # extract HTTP response code
    code = -1
    try:
        code = h.response.status_code
        assert isinstance(code, int)
    except Exception:
        # we have no idea what happened
        code = 418

    # extract HTTP reason
    reason = 'UNKNOWN ERROR'
    try:
        reason = h.response.reason
    except Exception:
        pass

    # Tapis APIs will give JSON responses if the target web service is at all
    # capable of fulfilling the request. Therefore, try first to extract fields
    # from the JSON response, then fall back to returning the plain text from
    # the response.
    err_msg = 'Unexpected encountered by the web service'
    status_msg = 'error'
    version_msg = 'unknown'
    try:
        j = h.response.json()
        if 'message' in j:
            err_msg = j['message']
        if 'status' in j:
            status_msg = j['status']
        if 'version' in j:
            version_msg = j['version']
    except Exception:
        err_msg = h.response.text

    httperror = '[{}] {}; message: {}; status: {}; version: {}; response.content: {}'
    return httperror.format(code, reason, err_msg, status_msg, version_msg,
                            h.response.content)


def handle_http_error(httperror):
    decorated_http_error = read_tapis_http_error(httperror)
    if httperror.response.status_code == 404:
        raise HTTPNotFoundError(httperror)
    else:
        raise AgaveError(decorated_http_error)
