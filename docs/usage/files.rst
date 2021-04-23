#####
Files
#####

Support for the core Tapis file management is provided by the **files**
command set. New, and of note, is support for wildcard include and exclude
filters when uploading and downloading, as well as a "sync" mode for downloads
that only retrieves files from Tapis if they are different from their local
copy.

****************
General Commands
****************

.. autoprogram-cliff:: tapis.cli
   :command: files list

.. autoprogram-cliff:: tapis.cli
   :command: files show

.. autoprogram-cliff:: tapis.cli
   :command: files history

.. autoprogram-cliff:: tapis.cli
   :command: files mkdir

.. autoprogram-cliff:: tapis.cli
   :command: files copy

.. autoprogram-cliff:: tapis.cli
   :command: files move

.. autoprogram-cliff:: tapis.cli
   :command: files delete

.. autoprogram-cliff:: tapis.cli
   :command: files upload

.. autoprogram-cliff:: tapis.cli
   :command: files download

****************
Sharing Commands
****************

Manage access by other users to Tapis files and folders that you control.

.. autoprogram-cliff:: tapis.cli
   :command: files pems *

