######
Actors
######

Support for Tapis actors (also known as Abaco actors) is is provided by the 
**actors** command set. It includes supplementary workflows for creating 
and deploying actor projects such as ``actors init`` and ``actors deploy``.

*******
General
*******

List and inspect all Actors the currently authenticated user can access.

.. autoprogram-cliff:: tapis.cli
   :command: actors list

.. autoprogram-cliff:: tapis.cli
   :command: actors show

Messaging
=========

Send a message to an Actor's mailbox, resulting in an Execution. This can 
be done asynchronously (default) or synchronously. For the latter case, it 
is possible to save the result to a file.

.. autoprogram-cliff:: tapis.cli
   :command: actors submit

.. autoprogram-cliff:: tapis.cli
   :command: actors run

Executions
==========

List and inspect Executions for a given Actor. It is also possible 
to view the logs for a specific Execution.

.. autoprogram-cliff:: tapis.cli
   :command: actors execs *

*******
Sharing
*******

Assign and manage human-readable nicknames for Actors that 
can be used in lieu of their unique IDs. 

Aliases
=======

.. autoprogram-cliff:: tapis.cli
   :command: actors aliases *

Nonces
======

Generate and manage Nonces, which are a kind of API key for 
Actors that allow them to be used without authenticating to the 
Tapis platform. 

.. autoprogram-cliff:: tapis.cli
   :command: actors nonces *

Permissions
===========

Grant and manage update and execution rights for an 
Actor to other Tapis platform users. 

.. autoprogram-cliff:: tapis.cli
   :command: actors permissions *

**************
Administration
**************

Create and manage Actors. This can be accomplished by interacting 
directly with the Abaco APIs via ``create``, ``update``, and 
``delete`` or via Tapis CLI workflows ``init`` and ``deploy``. 

.. autoprogram-cliff:: tapis.cli
   :command: actors create

.. autoprogram-cliff:: tapis.cli
   :command: actors update

.. autoprogram-cliff:: tapis.cli
   :command: actors delete

.. autoprogram-cliff:: tapis.cli
   :command: actors deploy


Workers
=======

View and manage an Actor's workers, which control the extent 
to which the Actor can scale to accomodate additional concurrent 
messages. 

.. autoprogram-cliff:: tapis.cli
   :command: actors workers *

********
Projects
********

Create and deploy new actors from a configuration-driven template. 

.. autoprogram-cliff:: tapis.cli
   :command: apps init

.. autoprogram-cliff:: tapis.cli
   :command: apps deploy
