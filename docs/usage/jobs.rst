Jobs
====

Support for the core Tapis jobs life cycle is provided by the **jobs**
command set. New, and of note, is support for wildcard include and exclude
filters when downloading job outputs, as well as a "sync" mode that only
retrieves files from Tapis if they are different from their local copy.

.. autoprogram-cliff:: tapis.cli
   :command: jobs list

.. autoprogram-cliff:: tapis.cli
   :command: jobs show

.. autoprogram-cliff:: tapis.cli
   :command: jobs submit

.. autoprogram-cliff:: tapis.cli
   :command: jobs status

.. autoprogram-cliff:: tapis.cli
   :command: jobs history

.. autoprogram-cliff:: tapis.cli
   :command: jobs resubmit

.. autoprogram-cliff:: tapis.cli
   :command: jobs hide

.. autoprogram-cliff:: tapis.cli
   :command: jobs unhide

Outputs
-------

.. autoprogram-cliff:: tapis.cli
   :command: jobs outputs *

Permissions
-----------

.. autoprogram-cliff:: tapis.cli
   :command: jobs pems *

Search
------

It is possible to search for tapis Jobs by several criteria. Please consult
``tapis jobs search -h`` for guidance.

Usage Examples
--------------

*Coming soon*
