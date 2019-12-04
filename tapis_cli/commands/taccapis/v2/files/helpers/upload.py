import fnmatch
import logging
import os
import sys
import traceback

from tapis_cli.utils import (datestring_to_epoch, humanize_bytes, relpath,
                             abspath, print_stderr, seconds, fnmatches)

from .error import (read_tapis_http_error, handle_http_error,
                    TapisOperationFailed, AgaveError, HTTPError,
                    FileExcludedError)
from .manage import makedirs

logging.getLogger(__name__).setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

__all__ = ['upload']


def _check_write(file_name,
                 system_id,
                 size,
                 timestamp,
                 force=False,
                 sync=False,
                 agave=None):
    """Placeholder to check if we should write remote
    """
    return True


def _upload(local_file_path,
            system_id,
            destination='/',
            includes=None,
            excludes=[],
            size=None,
            timestamp=None,
            block_size=4096,
            atomic=False,
            force=False,
            sync=False,
            agave=None):
    """Private wrapper for doing a file upload to Tapis
    """
    # If includes is specified, check filename against it
    if not fnmatches(local_file_path, includes):
        raise FileExcludedError(
            '{0} did not match --include filter'.format(local_file_path))

    # Check filename is in the excludes list
    if fnmatches(local_file_path, excludes):
        raise FileExcludedError(
            '{0} matched --exclude filter'.format(local_file_path))

    # Check size and modtime of remote vs overwrite policy
    # For eventual implementation of --sync and --force
    if not _check_write(
            local_file_path, system_id, size, timestamp, force=force,
            sync=sync):
        raise FileExistsError(
            'Remote {0} exists and was not different from local.'.format(
                local_file_path))

    try:
        agave.files.importData(systemId=system_id,
                               filePath=destination,
                               fileToUpload=open(local_file_path, 'rb'))
    except HTTPError as h:
        handle_http_error(h)
    except (OSError, IOError) as err:
        logger.error(str(err))
        raise
    except Exception as exc:
        traceback.print_exc(file=sys.stdout)
        raise TapisOperationFailed("Upload failed: {0}}".format(exc))

    return True


def _local_walk(local_file_path):
    """Walk local directory to find candidate uploads

    Returns list of (path, size, epoch)
    """
    to_upload = []
    if not os.path.exists(local_file_path):
        raise IOError('{0} not found'.format(local_file_path))
    else:
        if os.path.isfile(local_file_path):
            to_upload.append(
                (local_file_path, os.path.getsize(local_file_path),
                 os.path.getmtime(local_file_path)))
        elif os.path.isdir(local_file_path):
            directories = False
            dotfiles = False
            for root, _, filenames in os.walk(local_file_path):
                for filename in filenames:
                    if not filename.startswith('.') or dotfiles:
                        full_path = os.path.join(root, filename)
                        to_upload.append(
                            (full_path, os.path.getsize(full_path),
                             os.path.getmtime(full_path)))
                if directories and root not in to_upload:
                    to_upload.append((root, 0, os.path.getmtime(root)))
    to_upload = [list(t) for t in to_upload]
    return to_upload


def upload(local_file_path,
           system_id,
           destination='/',
           excludes=None,
           includes=None,
           force=False,
           sync=False,
           atomic=False,
           progress=True,
           agave=None):

    (uploaded, skipped, errors, ul_bytes, runtime) = ([], [], [], 0, None)

    if excludes is None:
        excludes = []

    # Compile files to be uploaded
    if progress:
        print_stderr('Finding file(s) to upload...')
    start_time = seconds()
    upload_files = _local_walk(local_file_path)
    elapsed_walk = seconds() - start_time
    msg = 'Found {0} file(s) in {1}s'.format(len(upload_files), elapsed_walk)
    logger.debug(msg)
    if progress:
        print_stderr(msg)

    # Filter out excludes
    # TODO - make sure abs and relpaths are supported
    # TODO - support some kind of wildcard match
    # upload_files = [f for f in upload_files_all if f[0] not in excludes]
    # if progress:
    #     print_stderr('Excluding {0} file(s)'.format(
    #         len(upload_files_all) - len(upload_files)))

    # Compute which, if any, remote directories might need to be created
    # Note that these directory names will be relative to the destination path
    if os.path.isfile(local_file_path):
        dir_parent = os.path.dirname(local_file_path)
        dir_basename = '.'
    else:
        dir_parent = os.path.dirname(local_file_path)
        dir_basename = os.path.basename(local_file_path)
    local_dirs = [
        relpath(os.path.dirname(f[0]).replace(dir_parent, ''))
        for f in upload_files
    ]
    # Before adding the grandparent to set of created dirs, add the destinations to each upload record
    for idx, uf in enumerate(upload_files):
        upload_files[idx].append(os.path.join(destination, local_dirs[idx]))

    # Remove duplicates as each member of create_dirs represents
    # at least one API call
    local_dirs.insert(0, dir_basename)
    create_dirs = []
    for d in local_dirs:
        if d not in create_dirs and d not in ('.', ''):
            create_dirs.append(d)

    # Create the remote directories
    # Do this ahead of time (and manually) to avoid relying on Tapis' files
    # since that service's path handling behavior can be tricky
    for rdir in create_dirs:
        if progress:
            print_stderr('Creating remote directory "{0}"...'.format(rdir))
        makedirs(relpath(rdir),
                 system_id=system_id,
                 destination=abspath(destination),
                 agave=agave)

    # Do the actual uploads
    start_time_all = seconds()
    for ufile in upload_files:
        if progress:
            print_stderr('Uploading {0}...'.format(ufile[0]))
        try:
            _upload(ufile[0],
                    system_id,
                    destination=ufile[3],
                    size=ufile[1],
                    timestamp=ufile[2],
                    includes=includes,
                    excludes=excludes,
                    force=force,
                    sync=sync,
                    agave=agave)
            # TRack uploaded files
            uploaded.append(ufile[0])
            # Track cumulative data size
            ul_bytes = ul_bytes + ufile[1]
        # TODO - implement a separate exception for FileExcluded
        except FileExcludedError as fexc:
            errors.append(fexc)
            skipped.append(ufile[0])
        except FileExistsError as fxerr:
            if sync or force:
                skipped.append(ufile[0])
            else:
                errors.append(fxerr)
        except Exception as exc:
            errors.append(exc)

    elapsed_download = seconds() - start_time_all
    msg = 'Uploaded {0} files in {1}s'.format(len(uploaded), elapsed_download)
    logger.debug(msg)
    if progress:
        print_stderr(msg)

    return uploaded, skipped, errors, ul_bytes, elapsed_download
