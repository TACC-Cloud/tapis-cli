########
Profiles
########

Support for showing or searching user profiles is implemented, contigent on the
configuration and access policy of the current Tapis tenant.

****************
General Commands
****************

.. autoprogram-cliff:: tapis.cli
   :command: profiles show

.. autoprogram-cliff:: tapis.cli
   :command: profiles show self

***************
Search Commands
***************

Search for Tapis profiles by any of several criteria. Please consult
``tapis profiles search -h`` for guidance.
