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

*******
Sharing
*******

Manage access by other users to Tapis apps that you control.

.. autoprogram-cliff:: tapis.cli
   :command: apps pems *

******
Search
******

Search for tapis Apps by any of several criteria. Please consult
``tapis apps search -h`` for guidance.

**************
Administration
**************

Manage global settings for a Tapis app.

.. autoprogram-cliff:: tapis.cli
   :command: apps publish

.. autoprogram-cliff:: tapis.cli
   :command: apps unpublish

********
Projects
********

Create and deploy new apps from a configuration-driven template. 

.. autoprogram-cliff:: tapis.cli
   :command: apps init

.. autoprogram-cliff:: tapis.cli
   :command: apps deploy