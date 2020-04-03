Jobs
====

Support for the core Tapis jobs life cycle is provided by the **jobs**
command set. New, and of note, is support for wildcard include and exclude
filters when downloading job outputs, as well as a "sync" mode that only
retrieves files from Tapis if they are different from their local copy.

****************
General Commands
****************

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
   :command: jobs cancel

.. autoprogram-cliff:: tapis.cli
   :command: jobs resubmit

.. autoprogram-cliff:: tapis.cli
   :command: jobs hide

.. autoprogram-cliff:: tapis.cli
   :command: jobs unhide

***************
Output Commands
***************

.. autoprogram-cliff:: tapis.cli
   :command: jobs outputs *

****************
Sharing Commands
****************

.. autoprogram-cliff:: tapis.cli
   :command: jobs pems *

***************
Search Commands
***************

It is possible to search for tapis Jobs by several criteria. Please consult
``tapis jobs search -h`` for guidance.

**************
Templated Jobs
**************

The ``jobs init`` command can populate a job definition for the designated Tapis app. It can 
run automatically, relying on default values provided by the app, or interactively, which allows 
the user to specify each value. 

.. autoprogram-cliff:: tapis.cli
   :command: jobs init

**************
Usage Examples
**************

*Coming soon*
