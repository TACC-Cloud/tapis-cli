import os
from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import (ServiceIdentifier, AgaveURI,
                                               LocalFilePath,
                                               OptionNotImplemented)
from tapis_cli.utils import (datestring_to_epoch, humanize_bytes, relpath,
                             abspath, print_stderr)

from . import API_NAME, SERVICE_VERSION
from .models import File
from .formatters import FilesFormatOne
from .helpers.upload import upload
from .helpers.walk import walk
from .helpers.stat import isdir, isfile, exists
from .helpers.manage import makedirs
from .mixins import (ExcludeFiles, FilesCallbackURI, IncludeFiles,
                     OverwritePolicy, ReportProgress)

__all__ = ['FilesUpload']


class FilesUpload(FilesFormatOne, AgaveURI, LocalFilePath, ExcludeFiles,
                  IncludeFiles, FilesCallbackURI, OverwritePolicy,
                  ReportProgress):

    HELP_STRING = 'Upload from local host to Tapis'
    LEGACY_COMMMAND_STRING = 'files-upload'

    def get_parser(self, prog_name):
        parser = super(FilesUpload, self).get_parser(prog_name)
        # Positionals:
        #
        # CLI expects <agave_uri> <file_path> so the user can up-arrow
        # in the terminal to change the uploaded file path
        parser = AgaveURI.extend_parser(self, parser)
        parser = LocalFilePath.extend_parser(self, parser)
        # Arguments:
        #
        # parser = IncludeFiles.extend_parser(self, parser)
        parser = ExcludeFiles.extend_parser(self, parser)
        parser = OverwritePolicy.extend_parser(self, parser)
        parser = FilesCallbackURI.extend_parser(self, parser)
        parser = ReportProgress.extend_parser(self, parser)
        # --sync : wait for all files to complete staging
        return parser

    def _remote_walk(self, remote_file_path, remote_system_id):
        records = walk(remote_file_path,
                       remote_system_id,
                       agave=self.tapis_client)
        paths = [relpath(r['path']) for r in records]
        sizes = [r['length'] for r in records]
        mods = [datestring_to_epoch(r['lastModified']) for r in records]
        remote_contents = [list(c) for c in zip(paths, sizes, mods)]
        return remote_contents

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.update_payload(parsed_args)

        # Catch unimplemented options
        if parsed_args.sync:
            raise OptionNotImplemented('--sync is not implemented')
        if parsed_args.overwrite:
            raise OptionNotImplemented('--force is not implemented')
        if parsed_args.files_callback_uri:
            raise OptionNotImplemented('--callback is not implemented')

        local_file_path = parsed_args.local_file_path
        (storage_system,
         remote_file_path) = self.parse_url(parsed_args.agave_uri)

        uploaded, skipped, exceptions, ul_bytes, elapsed = upload(
            local_file_path,
            storage_system,
            remote_file_path,
        # includes=parsed_args.include_files,
            excludes=parsed_args.exclude_files,
            force=parsed_args.overwrite,
            sync=parsed_args.sync,
            progress=parsed_args.progress,
            atomic=False,
            agave=self.tapis_client)

        headers = [
            'uploaded', 'skipped', 'messages', 'bytes_transferred',
            'elapsed_sec'
        ]
        if parsed_args.formatter in ('json', 'yaml'):
            data = [
                uploaded, skipped, [str(e) for e in exceptions], ul_bytes,
                elapsed
            ]
        else:
            data = [
                len(uploaded),
                len(skipped),
                len(exceptions),
                humanize_bytes(ul_bytes), elapsed
            ]
        return (tuple(headers), tuple(data))


# Implement sync or force mode
#
# walk local directory
# walk remote directory AgaveURI
# foreach file do upload
#   cache remote destination, expected size in "uploaded"
# iterate (up to N times or with some kind of exponential backoff)
#  for cf in "uploaded"
#   compare size of local and remote in bytes
#   compare modification times (remote should be newer)
#   remove cf from "uploaded" if appears to be done
# report out
#   uploaded
#   skipped
#   warnings
#   data (bytes)
#   elapsed (sec)
