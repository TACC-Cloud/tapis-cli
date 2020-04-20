################
Template Support
################

Tapis app, job, and system definitions (as well as metadata records) are commonly 
defined as JSON documents files. Sharing them files can be challenging 
(for instance, as part of collaborative development), since they can 
contain user-specific values. One way to deal with this is to automate 
find-and-replace workflows for files, but another is to use variables. Inspired 
by this real-world use case, we have introduced support for template 
variables throughout the Tapis CLI. 

Let us consider an example. A group of collabortators each has 
a private copy of a Tapis app for counting chickens, where the app identifier follows the 
naming convention ``chicken-counter-[username]-1.0.0``. They want to standardize on one 
set of parameters for a specific set of counting experiments they are doing. Without 
templating, each would maintain their parameter set in a standalone job file. For user 
**ellen** that file might look like so:

.. code-block:: json

    {
        "appId": "chicken-counter-ellen-1.0.0",
        "archiveSystem": "data-tacc-work-ellen",
        "maxRunTime": "01:00:00",
        "inputs": {
            "chix_img": "agave://data-tacc-cloud/images/too_many_chickens.png"
        },
        "name": "chicken-count",
        "parameters": {
            "beak_threshold": 10.0,
            "wing_threshold": -6.33
        }
    }

If the group leader Francesca decides that ``wing_threshold`` needs to be -8.00, 
everyone will need to edit a copy of the job file. If the group gets a master parameter 
file from the group leader, that means each member will need to replace refernces to 
Francesca's username with their own. Note also that the job **name** 
is static, which could get annoying. Wouldn't it be nice if we could change it 
for each instance of job that is run? 

A version of the file using Tapis CLI templating might look like:

.. code-block:: json

    {
        "appId": "chicken-counter-{{ username }}-1.0.0",
        "archiveSystem": "data-tacc-work-{{ username }}",
        "maxRunTime": "01:00:00",
        "inputs": {
            "chix_img": "agave://data-tacc-cloud/images/too_many_chickens.png"
        },
        "name": "chicken-count-{{ iso8601_basic_short }}",
        "parameters": {
            "beak_threshold": 10.0,
            "wing_threshold": -6.33
        }
    }

Submitting this file to the Tapis jobs service using ``tapis jobs submit`` 
would result in a job request being to the proper app ID and 
``{{ iso8601_basic_short }}`` is be replaced with an IS0-8601 date stamp
 ``YYYMMDDTHHmmss``. 
 
Nifty, eh? There's much more that can be done. The system supports dozens of 
built-in and run-time variables, and can be extended by the end user without coding. 
Also, since the system is built using Python's Jinja2 module, any Jinja syntax can 
be used, including conditionals and iterators. 

*********
Variables
*********

There are two classes of variables supported by the template system: 
"core" variables and "project" variables. Core variables are provided 
by the CLI with no options for user configuration, while project 
variables are set via a file in *.ini* format. 

Core variables
==============

These are global variables representing the state and 
environment of the CLI itself. They are intended for use in any app, 
job, system, or metadata definition without additional configuration. 
You can find the name and value of core variables via the command 
``tapis info vals list``. Core variables are snake-cased with no 
dot notation. Examples include ``first_name``, ``fqdn`, 
``git_remote``, and ``username``.

Project Variables
=================

Sometimes, one needs to scope variables to a specific context (i.e. 
only within the build directory for an app). This use case is 
enabled by use of a named *.ini* file. Project variables can be 
identified by use of dot notation in their name. Examples include 
``app.name`` and ``docker.tag``. 

Naming
------

The only supported name for a project variables file is ``project.ini`` 
although ``app.ini`` and ``reactor.ini`` are allowed for backwards 
compatibility with previous versions of the templating system. The 
rationale is that other build systems and applications use the ini 
file format, so we must constrain ourselves to using one name.

Search Path
-----------

If a path is specified using the ``--ini`` option, Tapis CLI looks 
at that location for a project variable file. Note that the file 
**must** be exist and be readable if it is manually specified. If 
no path to an ini file is provided, the CLI looks in the current 
working directory for a file named ``project.ini``. If one is found, 
it must be readable. If no variable file is provided, project 
variables are not made available to the templating system. 

Ini File Schema
---------------

A Tapis CLI ini file contains one or more stanzas: 

    - app : variables pertaining to a Tapis app
    - actor : variables pertaining to a Tapis actor
    - env : general-purpose environment variables
    - git : variables that pertain to a git repository
    - job : variables pertaining to a Tapis job
    - system : variables pertaining to a Tapis system

Within each stanza are named variables. Any variable name included 
in the default ini file (``tapis info vars init``) should be 
considered reserved for use by CLI workflows such as 
``tapis apps deploy`` and ``tapis jobs template``. You are free to 
add additional variables under these sections, with the caveat 
that future updates to the CLI might conflict with them. A better 
solution for defining custom variables is to add them to ``env`` 
as that section is reserved for user- or program-defined data. 

Below is an example ``project.ini`` file. 

.. code-block::

    [app]
    name =
    version =
    bundle =
    deployment_path =
    deployment_system =
    execution_system =

    [actor]
    name =
    description =
    alias =
    stateless = True
    hint =
    privileged = False
    use_uid = True
    workers =

    [docker]
    dockerfile = Dockerfile
    username =
    organization =
    repository =
    tag =
    build_args =
    use_commit_hash = False

    [env]

    [git]
    branch = master
    remote =

    [job]

    [system]
    ssh_private_key = ~/.ssh/id_rsa

**************
Usage Examples
**************

*Coming soon*

*****************
Technical Details
*****************

Tapis CLI uses _Jinja2 to power its template system. Most if not all Jinja 
constructs and syntax should be supported. Please file an _issue if you 
discover that is not the case. 

Tapis CLI uses _Configparser to parse and write ini files. All configparser 
functions, including interpolation (allowing for additional templating 
behavior!), should be available. Please file an _issue if you 
discover that is not the case. 

.. _Configparser: https://docs.python.org/3/library/configparser.html

.. _Jinja2: https://palletsprojects.com/p/jinja/

.. _issue: https://github.com/TACC-Cloud/tapis-cli/issues

