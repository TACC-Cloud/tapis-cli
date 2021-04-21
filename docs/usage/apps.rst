####
Apps
####

Support for the core Tapis applications life cycle is provided by the **apps**
command set. Extensions to the core API commands, such as ``apps init`` 
and ``apps deploy`` are also included.

*******
General
*******

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

********
Projects
********

.. autoprogram-cliff:: tapis.cli
   :command: apps init

.. autoprogram-cliff:: tapis.cli
   :command: apps deploy

*******
Sharing
*******

.. autoprogram-cliff:: tapis.cli
   :command: apps pems *

******
Search
******

It is possible to search for tapis Apps by several criteria. Please consult
``tapis apps search -h`` for guidance.

**************
Administration
**************

.. autoprogram-cliff:: tapis.cli
   :command: apps publish

.. autoprogram-cliff:: tapis.cli
   :command: apps unpublish

**************
Usage Examples
**************

*Coming soon*
