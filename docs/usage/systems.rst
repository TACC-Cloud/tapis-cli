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

Manage access by other users to Tapis systems that you control.

.. autoprogram-cliff:: tapis.cli
   :command: systems roles *


***************
Search Commands
***************

Search for Tapis Systems by several criteria. Please consult
``tapis systems search -h`` for guidance.

***************
Queues Commands
***************

View and interact with queues on a Tapis execution system.

.. autoprogram-cliff:: tapis.cli
   :command: systems queues *

***********************
Administrative Commands
***********************

Manage global settings for a Tapis system.

.. autoprogram-cliff:: tapis.cli
   :command: systems publish

.. autoprogram-cliff:: tapis.cli
   :command: systems unpublish

