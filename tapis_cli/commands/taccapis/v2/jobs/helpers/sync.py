"""Web service implementations of jobs-output ``sync`` operations.
"""
import copy
import logging
import os
import re
import requests
import shutil

import datetime
from dateutil.tz import tzoffset

from tapis_cli import settings
from tapis_cli.commands.taccapis.v2.files.helpers.error import FileExcludedError
from tapis_cli.utils import (nanoseconds, seconds, abspath, normpath, relpath,
                             print_stderr, datestring_to_epoch, fnmatches,
                             makedirs)
from tapis_cli.clients.services.taccapis.v2 import TaccApiDirectClient

from .error import (read_tapis_http_error, handle_http_error,
                    TapisOperationFailed, AgaveError, HTTPError,
                    OutputFileExistsError)
from .stat import isdir, isfile
from .walk import walk

from queue import Queue
import threading
from threading import Thread

logging.getLogger(__name__).setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

__all__ = ['download', 'basic_download']

DEFAULT_SYSTEM_ID = 'data-tacc-sandbox'
DEFAULT_PAGE_SIZE = 100


def __download(src,
               job_uuid,
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
        api_server, job_uuid, src)
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
        file_name = os.path.basename(src_filename)
    if atomic:
        temp_file_name = '{0}-{1}'.format(file_name, nanoseconds())
    else:
        temp_file_name = file_name
    if temp_file_name.startswith('/'):
        temp_file_name = temp_file_name[1:]
    return file_name, temp_file_name


def _check_write(filename, size, timestamp, sync=False, force=False):
    """Determine whether to write (or overwrite) a local file
    """

    # Does the filename not exist? OK, write it
    if not os.path.exists(filename) or force is True:
        return True

    if sync is True:
        # TODO - May need to factor in local filesystem blocksize
        local_size = os.path.getsize(filename)
        # Timestamp comaprison is done at the second level
        # TODO - Do we need to consider time zone?
        local_timestamp = round(os.path.getmtime(filename))
        if (timestamp > local_timestamp) or (size != local_size):
            return True

    return False


def _download(src,
              job_uuid,
              size=None,
              timestamp=None,
              excludes=None,
              includes=None,
              dest=None,
              block_size=4096,
              atomic=False,
              force=False,
              sync=False,
              agave=None):

    local_filename, tmp_local_filename = _local_temp_filename(
        src, dest, atomic)

    if isinstance(includes, list) and len(includes) > 0:
        if not fnmatches(src, includes):
            raise FileExcludedError(
                '{0} did not match --include filter'.format(src))

    # Check filename is in the excludes list
    if isinstance(excludes, list) and len(excludes) > 0:
        if fnmatches(src, excludes):
            raise FileExcludedError('{0} matched --exclude filter'.format(src))

    if not _check_write(
            local_filename, size, timestamp, sync=sync, force=force):
        raise OutputFileExistsError(
            'Local {0} exists and was not different from remote'.format(
                local_filename))

    try:
        client = TaccApiDirectClient(agave)
        # jobs/v2/9e74b852-0e1f-4363-8c09-5ab9f5299797-007/outputs/media/20190221t174839.out
        url_path = '{0}/outputs/media'.format(job_uuid)
        client.setup('jobs', 'v2', url_path)
        # raise SystemError(client.build_url(src[1:]))
        rsp = client.get_bytes(src[1:])
        #rsp = agave.jobs.downloadOutput(filePath=src, jobId=job_uuid)
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


def basic_download(src, job_uuid, dest=None, agave=None):
    client = TaccApiDirectClient(agave)
    # jobs/v2/9e74b852-0e1f-4363-8c09-5ab9f5299797-007/outputs/media/20190221t174839.out
    url_path = '{0}/outputs/media'.format(job_uuid)
    client.setup('jobs', 'v2', url_path)
    # raise SystemError(client.build_url(src[1:]))
    try:
        rsp = client.get_bytes(src)
        #rsp = agave.jobs.downloadOutput(filePath=src, jobId=job_uuid)
        if isinstance(rsp, dict):
            raise TapisOperationFailed("Failed to download {}".format(src))
        with open(dest, 'wb') as dest_file:
            for block in rsp.iter_content(2048):
                if not block:
                    break
                dest_file.write(block)
    except HTTPError as h:
        handle_http_error(h)
    except (OSError, IOError) as err:
        logger.error(str(err))
        raise
    except Exception as exc:
        raise TapisOperationFailed("Download failed: {}".format(exc))


def download(source,
             job_uuid,
             destination=None,
             excludes=None,
             includes=None,
             force=False,
             sync=False,
             atomic=False,
             progress=False,
             agave=None):

    downloaded, skipped, errors, runtime = ([], [], [], None)

    if destination is None:
        dest_dir = str(job_uuid)
    else:
        dest_dir = destination

    # else:
    #     includes = [os.path.join('/', i) for i in includes]

    if progress:
        print_stderr('Walking remote resource...')
    start_time = seconds()
    # Try to avoid timeouts since walk is already pretty slow
    agave.refresh()
    all_targets = walk(source,
                       job_uuid=job_uuid,
                       dotfiles=True,
                       recurse=True,
                       agave=agave)
    elapsed_walk = seconds() - start_time

    msg = 'Found {0} file(s) in {1}s'.format(len(all_targets), elapsed_walk)
    logger.debug(msg)
    if progress:
        print_stderr(msg)

    # Extract absolute names
    # Under jobs, paths all begin with /
    paths = [f['path'] for f in all_targets]

    # Tapis Jobs returns a spurious "null/" at the start of
    # each file's path. This is a temporary workaround.
    paths = [re.sub('null/', '/', p) for p in paths]
    sizes = [f['length'] for f in all_targets]
    mods = [datestring_to_epoch(f['lastModified']) for f in all_targets]

    # Create local destination paths
    dirs = [os.path.dirname(p) for p in paths]
    make_dirs = [
        os.path.join(dest_dir, relpath(p)) for p in dirs
        if p not in ('/', './')
    ]
    # Create destinations
    for dir in make_dirs:
        makedirs(dir, exist_ok=True)

    # Local filenames including destination directory
    rel_paths = [os.path.join(dest_dir, relpath(p)) for p in paths]

    downloads = [list(a) for a in zip(paths, sizes, mods, rel_paths)]
    start_time_all = seconds()
    # Try to avoid timeouts since walk is already pretty slow
    agave.refresh()
    for src, size, mod, dest in downloads:
        if progress:
            print_stderr('Downloading {0}...'.format(os.path.basename(src)))
        try:
            # TODO - refresh token is size > threshold
            _download(src,
                      job_uuid,
                      size=size,
                      timestamp=mod,
                      dest=dest,
                      includes=includes,
                      excludes=excludes,
                      atomic=atomic,
                      force=force,
                      sync=sync,
                      agave=agave)
            downloaded.append(src)
        except FileExcludedError as fexc:
            errors.append(fexc)
            skipped.append(src)
        except OutputFileExistsError as ofe:
            if sync or force:
                skipped.append(src)
            errors.append(ofe)
        except Exception as exc:
            errors.append(exc)

    elapsed_download = seconds() - start_time_all
    msg = 'Downloaded {0} files in {1}s'.format(len(paths), elapsed_download)
    logger.debug(msg)
    if progress:
        print_stderr(msg)

    return downloaded, skipped, errors, elapsed_walk + elapsed_download
