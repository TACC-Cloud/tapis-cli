Apps
====

Support for the core Tapis applications life cycle is provided by the **apps**
command set. Extensions to this lifecycle featured in some Tapis tenants,
such as ``apps init`` and ``apps deploy`` will be added in a future release.

Commands
--------

.. autoprogram-cliff:: tapis.cli
   :command: apps list

.. autoprogram-cliff:: tapis.cli
   :command: apps show

.. autoprogram-cliff:: tapis.cli
   :command: apps history

.. autoprogram-cliff:: tapis.cli
   :command: apps create

.. autoprogram-cliff:: tapis.cli
   :command: apps update

.. autoprogram-cliff:: tapis.cli
   :command: apps clone

.. autoprogram-cliff:: tapis.cli
   :command: apps disable

.. autoprogram-cliff:: tapis.cli
   :command: apps enable


Permissions
-----------

.. autoprogram-cliff:: tapis.cli
   :command: apps pems *

Search
------

It is possible to search for tapis Apps by several criteria. Please consult
``tapis apps search -h`` for guidance.

Administrative
--------------

.. autoprogram-cliff:: tapis.cli
   :command: apps publish

.. autoprogram-cliff:: tapis.cli
   :command: apps unpublish

Usage Examples
--------------

*Coming soon*
