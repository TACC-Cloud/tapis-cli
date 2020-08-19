#######
Systems
#######

Support for the Tapis resource management **systems** is provided by 
the **systems** command set. Helper workflows (such as assistance 
with SSH keys and testing newly created systems) will be added in 
coming releases.

****************
General Commands
****************

.. autoprogram-cliff:: tapis.cli
   :command: systems list

.. autoprogram-cliff:: tapis.cli
   :command: systems show

.. autoprogram-cliff:: tapis.cli
   :command: systems history

.. autoprogram-cliff:: tapis.cli
   :command: systems create

.. autoprogram-cliff:: tapis.cli
   :command: systems update

.. autoprogram-cliff:: tapis.cli
   :command: systems disable

.. autoprogram-cliff:: tapis.cli
   :command: systems enable

****************
Sharing Commands
****************

.. autoprogram-cliff:: tapis.cli
   :command: systems roles *


***************
Search Commands
***************

It is possible to search for tapis Systems by several criteria. Please consult
``tapis systems search -h`` for guidance.

***************
Queues Commands
***************

.. autoprogram-cliff:: tapis.cli
   :command: systems queues *

***********************
Administrative Commands
***********************

.. autoprogram-cliff:: tapis.cli
   :command: systems publish

.. autoprogram-cliff:: tapis.cli
   :command: systems unpublish

**************
Usage Examples
**************

*Coming soon*

