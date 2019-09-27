"""Web service implementations of files ``sync`` operations.
"""
import copy
import logging
import os
import requests
import shutil

from tapis_cli import settings
from tapis_cli.utils import (nanoseconds, seconds, abspath, normpath, relpath,
                             print_stderr, datestring_to_epoch)

from .error import (read_tapis_http_error, handle_http_error,
                    TapisOperationFailed, AgaveError, HTTPError)
from .stat import isdir, isfile
from .walk import walk

from queue import Queue
import threading
from threading import Thread

logging.getLogger(__name__).setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

__all__ = ['download', 'FileExistsError']

DEFAULT_SYSTEM_ID = 'data-tacc-sandbox'
DEFAULT_PAGE_SIZE = 100


class FileExistsError(IOError):
    pass


def __download(src,
               system_id,
               dest=None,
               block_size=4096,
               atomic=False,
               force=False,
               agave=None):
    """WIP: Function for implementing threaded downloads
    """
    # Setup requests client
    token = agave._token
    headers = {'authorization': 'Bearer {}'.format(token)}
    api_server = agave.api_server
    download_url = '{0}/files/v2/media/system/{1}/{2}'.format(
        api_server, system_id, src)
    rsp = requests.get(download_url, headers=headers)
    rsp.raise_for_status()


class DownloadWorker(Thread):
    """Thread for implementing parallel downloads
    """
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            src, system, dest, ag = self.queue.get()
            if src is None:
                break
            try:
                __download(src, system, dest, agave=ag)
            except Exception:
                self.queue.put((src, system, dest, ag))
            finally:
                self.queue.task_done()


def _local_temp_filename(src_filename, dest_filename=None, atomic=False):
    """Compute local and temp-local filenames, allowing for atomic writes
    """
    file_name = dest_filename
    if file_name is None:
        filename = os.path.basename(src_filename)
    if atomic:
        temp_file_name = '{0}-{1}'.format(file_name, nanoseconds())
    else:
        temp_file_name = file_name
    return file_name, temp_file_name


def _check_write(filename, size, timestamp, excludes, sync=True, force=False):
    """Determine whether to write (or overwrite) a local file
    """
    relative_excludes = []
    for e in excludes:
        if not e.startswith('./'):
            relative_excludes.append('./' + e)
        else:
            relative_excludes.append(e)

    if filename in relative_excludes:
        return False
    if not os.path.exists(filename) or force is True:
        return True
    else:
        if sync is False:
            return True

        # TODO - May need to factor in local filesystem blocksize
        local_size = os.path.getsize(filename)
        # Timestamp comaprison is done at the second level
        # TODO - Do we need to consider time zone?
        local_timestamp = round(os.path.getmtime(filename))
        if (timestamp > local_timestamp) or (size != local_size):
            return True
        else:
            return False


def _download(src,
              system_id,
              size=None,
              timestamp=None,
              excludes=None,
              dest=None,
              block_size=4096,
              atomic=False,
              force=False,
              sync=False,
              agave=None):

    local_filename, tmp_local_filename = _local_temp_filename(
        src, dest, atomic)

    if not _check_write(
            local_filename, size, timestamp, excludes, force=force, sync=sync):
        raise FileExistsError(
            'Local {0} exists and was not different from remote.'.format(
                local_filename))

    try:
        rsp = agave.files.download(filePath=src, systemId=system_id)
        if isinstance(rsp, dict):
            raise TapisOperationFailed("Failed to download {}".format(src))
        with open(tmp_local_filename, 'wb') as dest_file:
            for block in rsp.iter_content(block_size):
                if not block:
                    break
                dest_file.write(block)
        if atomic:
            try:
                os.rename(tmp_local_filename, local_filename)
            except Exception as err:
                raise IOError('Rename failed after download', err)
    except HTTPError as h:
        handle_http_error(h)
    except (OSError, IOError) as err:
        logger.error(str(err))
        raise
    except Exception as exc:
        raise TapisOperationFailed("Download failed: {}".format(exc))


def download(source,
             system_id,
             destination='.',
             excludes=None,
             force=False,
             sync=False,
             atomic=False,
             progress=False,
             agave=None):

    downloaded, skipped, errors, dl_bytes, runtime = ([], [], [], 0, None)

    if excludes is None:
        excludes = []

    if progress:
        print_stderr('Walking remote resource...')
    start_time = seconds()
    all_targets = walk(source, system_id=system_id, recurse=True, agave=agave)
    elapsed_walk = seconds() - start_time

    msg = 'Found {0} file(s) in {1}s'.format(len(all_targets), elapsed_walk)
    logger.debug(msg)
    if progress:
        print_stderr(msg)

    # Filters that build up list of paths to create and files to download
    abs_names = [f['path'] for f in all_targets]
    sizes = [f['length'] for f in all_targets]
    mods = [datestring_to_epoch(f['lastModified']) for f in all_targets]
    dest_names = [f.replace(source, '.') for f in abs_names]
    dest_paths = [f.replace('./', '') for f in dest_names]
    dest_paths = [
        os.path.join(destination, os.path.dirname(f)) for f in dest_paths
    ]
    # Remove references to current working directory and any redundant dir names
    create_paths = []
    create_paths = [
        f for f in dest_paths
        if f != './' and '{0}/'.format(destination) not in create_paths
    ]

    # Create destinations
    for p in create_paths:
        os.makedirs(p, exist_ok=True)

    # Do the downloads
    downloads = [list(a) for a in zip(abs_names, sizes, mods, dest_names)]
    start_time_all = seconds()
    for src, size, mod, dest in downloads:
        if progress:
            print_stderr('Downloading {0}...'.format(os.path.basename(src)))
        try:
            _download(src,
                      system_id,
                      size=size,
                      timestamp=mod,
                      dest=dest,
                      excludes=excludes,
                      force=force,
                      sync=sync,
                      atomic=False,
                      agave=agave)
            downloaded.append(src)
            # Track cumulative data size
            dl_bytes = dl_bytes + size
        except FileExistsError as fxerr:
            if sync or force:
                skipped.append(src)
            else:
                errors.append(fxerr)
        except Exception as exc:
            errors.append(exc)

    elapsed_download = seconds() - start_time_all
    msg = 'Downloaded {0} files in {1}s'.format(len(abs_names),
                                                elapsed_download)
    logger.debug(msg)
    if progress:
        print_stderr(msg)

    return downloaded, skipped, errors, dl_bytes, elapsed_walk + elapsed_download
