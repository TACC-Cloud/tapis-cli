############
The Ini File
############

A project's ini file may contain several sections, each with a handful 
of defined option names. Option/value pairs may be commented out using 
a leading ``;`` semicolon. Values that define paths are assumed to be 
relative to the project directory, unless specified as absolute. 
Mandatory variables are denoted in bold text. 

********
Sections
********

App
===

This section contains variables to configure an *app* project.

+-------------------+---------------------------------------------------+
| Option            | Function                                          |
+-------------------+---------------------------------------------------+
| **name**             | App name                                                                          |
+-------------------+---------------------------------------------------+
| **label**              | App human-readable label                                              |
+-------------------+---------------------------------------------------+
| **description**  | App short description                                                      |
+-------------------+---------------------------------------------------+
| **version**         | App version                                                                        |
+-------------------+---------------------------------------------------+
| bundle            | Directory containing application assets (bundle)  |
+-------------------+---------------------------------------------------+
| execution_system  | Tapis execution system for the application        |
+-------------------+---------------------------------------------------+
| deployment_system | Tapis storage system hosting application assets   |
+-------------------+---------------------------------------------------+
| deployment_path   | Path on deployment system where assets are stored |
+-------------------+---------------------------------------------------+

Actor
=====

This section contains variables to configure an *actor* project.

Docker
======

This section contains variables that define Linux container image and 
registry settings for the project. There is an implicit assumption that 
a project corresponds to a single container repo. 

+-----------------+-------------------------------------+
| Option          | Function                                                         |
+-----------------+-------------------------------------+
| dockerfile      | Docker image build file                               |
+-----------------+-------------------------------------+
| **namespace**   | Registry username or organization   |
+-----------------+-------------------------------------+
| **repo**        | Container image repo name                      |
+-----------------+-------------------------------------+
| **tag**           | Container image tag                                   |
+-----------------+-------------------------------------+
| build_args      | Build arguments for container image |
+-----------------+-------------------------------------+
| use_commit_hash | Use current commit hash as tag      |
+-----------------+-------------------------------------+

Env
===

This is a special section where you, the end-user, can add custom 
option-value pairs for use by the CLI templating engine. Option 
names must be alphanumeric strings ``[a-z0-9_]``.

Good option names:

    * slot
    * rock_and_roll
    * value123

Bad option names:

    * _foo
    * option.name
    * ThisOption
    
Values must be simple scalars and it should be assumed they will be 
interpreted as strings.

Using Env in a File
-------------------

Here is an example of including a custom option ``value123`` and using it 
to populate contents of a JSON document. The expected outcome is that 
the key ``parameter1`` will get a value of ``2048`` when the JSON 
document is interpreted by the CLI. 

.. code-block:: 
   :caption: ini file

    [env]
    value123 = 2048

.. code-block:: json
   :caption: json template

    {"parameter1": "{{ env.value123 }}"}

.. code-block:: json
   :caption: rendered json

    {"parameter1": "2048"}


Git
===

This section contains variables that define local and remote Git  
settings for the project. We assume that  a project corresponds 
to a single git repository.  

Grants
======

This section defines roles to be granted to apps, actors, jobs, 
metadata, or systems defined by the project. Only specific, 
designated roles (read, execute, update) are comprehended by this 
part of the projects system.  

Job
===

This section contains variables for use in defining *job* or *message* 
files for use with the project. 

System
======

This section contains variables for use specifically in an *system* project.