"""Web service implementations of the ``walk`` operation.

Provides both ``walk`` and ``listdir`` functions
via recursive ``files-list`` web service operations.
"""
import copy
import logging
import os
import shutil

from tenacity import (retry, retry_if_exception_type, stop_after_delay,
                      wait_exponential)

from tapis_cli import settings
from tapis_cli.utils import (nanoseconds, microseconds, abspath, normpath,
                             relpath)

from .constants import (FILE_TYPES, DIRECTORY_TYPES, NAME_KEY, PATH_KEY,
                        TYPE_KEY)
from .stat import exists
from .error import (read_tapis_http_error, handle_http_error,
                    TapisOperationFailed, AgaveError, HTTPError)

logging.getLogger(__name__).setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

__all__ = ['walk', 'listdir']

DEFAULT_SYSTEM_ID = 'data-tacc-sandbox'
DEFAULT_PAGE_SIZE = 100


# Wrapping the core files-list function, which is called recursively by
# walk() and listdir(), with @retry prevents a single missed/errored API call
# from forcing the system to restart a possibly very expensive recursive
# directory tree traversal
@retry(retry=retry_if_exception_type(AgaveError),
       reraise=True,
       stop=stop_after_delay(8),
       wait=wait_exponential(multiplier=2, max=64))
def _files_list(directory_path,
                system_id=DEFAULT_SYSTEM_ID,
                limit=DEFAULT_PAGE_SIZE,
                offset=0,
                root_dir='/',
                agave=None):
    """Private function to resiliently list a Tapis files directory
    """
    rooted_directory_path = abspath(directory_path, root_dir)
    logger.info('_files_list: agave://{}{}'.format(system_id, directory_path))
    try:
        return agave.files.list(systemId=system_id,
                                filePath=rooted_directory_path,
                                limit=limit,
                                offset=offset)
    except Exception as err:
        logger.warning('_files_list.error: {}'.format(err))
        raise


def _walk(directory_path,
          current_listing=None,
          system_id=DEFAULT_SYSTEM_ID,
          root_dir='/',
          directories=False,
          dotfiles=False,
          page_size=DEFAULT_PAGE_SIZE,
          recurse=True,
          sort=False,
          agave=None,
          **kwargs):
    """Private function to emulate ``os.walk()`` using ``files-list``
    """
    if current_listing is None:
        current_listing = []
    # This is probably redundant
    listing = current_listing
    logger.info('_walk: agave://{}{}'.format(system_id, directory_path))
    # If current_listing is not cloned, it will grow without bounds each
    # time _walk is called.
    # listing = copy.copy(current_listing)
    # print('_walk: current_listing has {} elements'.format(len(listing)))
    keeplisting = True
    skip = 0
    while keeplisting:
        sublist = _files_list(directory_path,
                              system_id=system_id,
                              root_dir='/',
                              limit=page_size,
                              offset=skip,
                              agave=agave)
        # print('_walk: sublist has {} elements'.format(len(sublist)))
        skip = skip + page_size
        if len(sublist) < page_size:
            keeplisting = False
            # print('_walk: recursion has ended')
        for f in sublist:
            if f[NAME_KEY] != '.':
                exclude_dotfile = f[NAME_KEY].startswith('.') \
                    and dotfiles is False
                if f[TYPE_KEY] in \
                        FILE_TYPES or directories is True:
                    if not exclude_dotfile:
                        # print('KEEP {0}'.format(f))
                        listing.append(f)
                # Recurse into found directories
                if f[TYPE_KEY] in DIRECTORY_TYPES and recurse is True:
                    # print('_walk: descend into {}'.format(f[PATH_KEY]))
                    _walk(f[PATH_KEY],
                          current_listing=listing,
                          system_id=system_id,
                          root_dir=root_dir,
                          directories=directories,
                          dotfiles=dotfiles,
                          page_size=page_size,
                          recurse=recurse,
                          agave=agave)
        if sort:
            listing.sort()
        return listing


def walk(directory_path,
         system_id=DEFAULT_SYSTEM_ID,
         root_dir='/',
         directories=False,
         dotfiles=False,
         sort=False,
         page_size=DEFAULT_PAGE_SIZE,
         agave=None,
         **kwargs):
    """Recursively lists contents of a Tapis files directory.

    Arguments:
        directory_path (str): Full or relative path of directory to walk
        system_id (str, optional): Tapis storageSystem for directory_path
        root_dir (str, optional): Base path if directory_path is relative
        directories (bool, optional): Whether result should include directories
        dotfiles (bool, optional): Whether result should include dotfiles
        page_size (int, optional): Override default Tapis files-list page size
        agave (Agave, optional): Tapis (Agave) API client

    Returns:
        list: List of Tapis-canonical absolute paths as AnnotatedFile objects

    Raises:
       TapisOperationFailed: An exception or error happened
    """
    logger.info('walk: agave://{}{}'.format(system_id, directory_path))
    start_time = nanoseconds()

    listing = _walk(directory_path,
                    system_id=system_id,
                    root_dir=root_dir,
                    directories=directories,
                    dotfiles=dotfiles,
                    page_size=page_size,
                    agave=agave)

    if sort:
        listing.sort()

    end_time = nanoseconds()
    elapsed = int((end_time - start_time) / 1000 / 1000)
    logger.debug('walk: found {} elements in {} msec'.format(
        len(listing), elapsed))

    return listing


def listdir(directory_path,
            system_id=DEFAULT_SYSTEM_ID,
            root_dir='/',
            directories=True,
            dotfiles=False,
            page_size=DEFAULT_PAGE_SIZE,
            sort=True,
            agave=None,
            **kwargs):
    """Lists immediate contents of a Tapis files directory.

    Arguments:
        directory_path (str): Full or relative path of directory to walk
        system_id (str, optional): Tapis storageSystem for directory_path
        root_dir (str, optional): Base path if directory_path is relative
        directories (bool, optional): Whether result should include directories
        dotfiles (bool, optional): Whether result should include dotfiles
        agave (Agave, optional): Tapis (Agave) API client

    Returns:
        list: List of paths relative to directory_path

    Raises:
        TapisOperationFailed: Some error prevented the action from completing
    """
    logger.info('listdir: agave://{}{}'.format(system_id, directory_path))
    start_time = nanoseconds()

    resp = _walk(directory_path,
                 system_id=system_id,
                 root_dir=root_dir,
                 directories=directories,
                 dotfiles=dotfiles,
                 page_size=page_size,
                 recurse=False,
                 agave=agave)

    # filter dirname from paths to emulate os.listdir()
    if not directory_path.endswith('/'):
        directory_path_filter = directory_path + '/'
    else:
        directory_path_filter = directory_path

    listing = []
    for r in resp:
        r[PATH_KEY] = r[PATH_KEY].replace(directory_path_filter, '')
        listing.append(r)

    end_time = nanoseconds()
    elapsed = int((end_time - start_time) / 1000 / 1000)
    logger.debug('listdir: found {} elements in {} msec'.format(
        len(listing), elapsed))

    return listing
