"""Web service implementations of ``jobs-output-list`` operations
"""
import copy
import logging
import os
import shutil

from attrdict import AttrDict

from tapis_cli.utils import (nanoseconds, microseconds, abspath, normpath,
                             relpath)
from tapis_cli.hashcache import lru_cache, picklecache

from .constants import (FILE_TYPES, DIRECTORY_TYPES, NAME_KEY, PATH_KEY,
                        TYPE_KEY, FILES_API_TYPES)
from .error import (read_tapis_http_error, handle_http_error,
                    TapisOperationFailed, AgaveError, HTTPError,
                    HTTPNotFoundError)

DEFAULT_PAGE_SIZE = 100

logging.getLogger(__name__).setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

__all__ = ['stat', 'rsrc_type', 'exists', 'isfile', 'isdir']


# TODO - this code duplicates files/helpers/stat almost entirely. Refactor to detect whether a job or file is being passed to the various methods?
def stat(file_path,
         job_uuid,
         root_dir='/',
         permissive=False,
         agave=None,
         **kwargs):
    """Retrieve attributes for a given path on a Tapis storageSystem

    Arguments:
        file_path (str): The path from which to fetch attributes
        job_uuid (str): The Tapis job for file_path
        root_dir (str, optional): Base path in output directory if file_path is relative
        permissive (bool, optional): Whether to raise an Exception on failure
        agave (Agave, optional): An active Tapis client

    Returns:
        dict: A dictionary containing Tapis attributes for a jobs output

    Raises:
        HTTPError: A transport or web services error was encountered
        TapisOperationFailed: Some other error prevented the operation
    """
    try:
        try:
            rooted_file_path = abspath(file_path, root_dir)
            resp = agave.jobs.listOutputs(jobId=job_uuid,
                                          filePath=rooted_file_path,
                                          limit=2)[0]
            return AttrDict(resp)
        except HTTPError as herr:
            handle_http_error(herr)
        except Exception as err:
            raise TapisOperationFailed(
                'Exception encountered with stat#files.list()', err)
    except Exception as err:
        logger.warning(
            'Exception encountered in rsrc_exists(): {}'.format(err))
        if permissive:
            return dict()
        else:
            raise


@picklecache.mcache(lru_cache(maxsize=256))
def rsrc_type(file_path,
              job_uuid,
              root_dir='/',
              permissive=False,
              agave=None,
              **kwargs):
    """Retrieve the ``type`` for a given path in a Tapis job output

    Arguments:
        file_path (str): The path from which to fetch attributes
        job_uuid (str): The Tapis job UUID for file_path
        root_dir (str, optional): Base path in output directory if file_path is relative
        permissive (bool, optional): Whether to raise an Exception on failure
        agave (Agave, optional): An active Tapis client

    Returns:
        string: Either ``file`` or ``dir``

    Raises:
        HTTPError: A transport or web services error was encountered
        TapisOperationFailed: Some other error prevented the operation
    """
    try:
        return stat(file_path,
                    job_uuid=job_uuid,
                    root_dir=root_dir,
                    permissive=False,
                    agave=agave).get(TYPE_KEY, None)
    except Exception as err:
        logger.warning('Exception encountered in rsrc_type(): {}'.format(err))
        if permissive:
            return False
        else:
            raise


@picklecache.mcache(lru_cache(maxsize=256))
def exists(file_path,
           job_uuid,
           root_dir='/',
           permissive=False,
           agave=None,
           **kwargs):
    """Determine if a path exists in a Tapis job output

    Arguments:
        file_path (str): The path from which to fetch attributes
        job_uuid (str): The Tapis job UUID for file_path
        root_dir (str, optional): Base path in output directory if file_path is relative
        permissive (bool, optional): Whether to raise an Exception on failure
        agave (Agave, optional): An active Tapis client

    Returns:
        bool: True if the path exists and False if not

    Raises:
        HTTPError: A transport or web services error was encountered
        TapisOperationFailed: Some other error prevented the operation
    """
    try:
        file_path_type = rsrc_type(file_path,
                                   job_uuid=job_uuid,
                                   root_dir=root_dir,
                                   permissive=False,
                                   agave=agave)
        return file_path_type in FILES_API_TYPES
    # We already know if the resource exists because tapis.stat() will throw
    # HTTPNotFoundError if the response code is 404
    except HTTPNotFoundError:
        return False
    except HTTPError as herr:
        logger.warning('HTTP error encountered in exists(): {}'.format(herr))
        raise
    except Exception as err:
        logger.warning('Exception encountered in exists(): {}'.format(err))
        if permissive:
            return False
        else:
            raise


@picklecache.mcache(lru_cache(maxsize=256))
def isfile(file_path,
           job_uuid,
           root_dir='/',
           permissive=False,
           agave=None,
           **kwargs):
    """Determine if a path exists and is a file in a Tapis job output

    Arguments:
        file_path (str): The path from which to fetch attributes
        job_uuid (str): The Tapis job UUID for file_path
        root_dir (str, optional): Base path in output directory if file_path is relative
        permissive (bool, optional): Whether to raise an Exception on failure
        agave (Agave, optional): An active Tapis client

    Returns:
        bool: True if the path is a file and False if not

    Raises:
        HTTPError: A transport or web services error was encountered
        TapisOperationFailed: Some other error prevented the operation
    """
    try:
        file_path_format = rsrc_type(file_path,
                                     job_uuid=job_uuid,
                                     root_dir=root_dir,
                                     permissive=False,
                                     agave=agave)
        return file_path_format in FILE_TYPES
    except Exception as err:
        logger.warning('Exception encountered in isfile(): {}'.format(err))
        if permissive:
            return False
        else:
            raise


@picklecache.mcache(lru_cache(maxsize=256))
def isdir(file_path,
          job_uuid,
          root_dir='/',
          permissive=False,
          agave=None,
          **kwargs):
    """Determine if a path exists and is a directory in a Tapis job output

    Arguments:
        file_path (str): The path from which to fetch attributes
        job_uuid (str): The Tapis job UUID for file_path
        root_dir (str, optional): Base path in output directory if file_path is relative
        permissive (bool, optional): Whether to raise an Exception on failure
        agave (Agave, optional): An active Tapis client

    Returns:
        bool: True if the path is a directory and False if not

    Raises:
        HTTPError: A transport or web services error was encountered
        TapisOperationFailed: Some other error prevented the operation
    """
    try:
        file_path_format = rsrc_type(file_path,
                                     job_uuid=job_uuid,
                                     root_dir=root_dir,
                                     permissive=False,
                                     agave=agave)
        return file_path_format in DIRECTORY_TYPES
    except Exception as err:
        logger.warning('Exception encountered in isdir(): {}'.format(err))
        if permissive:
            return False
        else:
            raise


def is_link(file_path,
            job_uuid,
            root_dir='/',
            permissive=False,
            agave=None,
            **kwargs):
    """Placeholder for a Tapis function to identify links
    """
    raise NotImplementedError(
        'Tapis files is unable to determine if a resource is a link')


def is_mount(file_path,
             job_uuid,
             root_dir='/',
             permissive=False,
             agave=None,
             **kwargs):
    """Placeholder for a Tapis function to identify mounts
    """
    raise NotImplementedError(
        'Tapis files is unable to determine if a resource is a mount')
