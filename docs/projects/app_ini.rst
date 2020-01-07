########
INI File
########

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

+-------------------+---------------------------------------------------+
| Option            | Function                                          |
+-------------------+---------------------------------------------------+
| **name**          | App name                                          |
+-------------------+---------------------------------------------------+
| **version**       | App version                                       |
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

Docker
======

+-----------------+-------------------------------------+
| Option          | Function                            |
+-----------------+-------------------------------------+
| dockerfile      | Docker image build instructions     |
+-----------------+-------------------------------------+
| **namespace**   | Docker Hub username or organization |
+-----------------+-------------------------------------+
| **repo**        | Container image repo name           |
+-----------------+-------------------------------------+
| tag             | Container image tag                 |
+-----------------+-------------------------------------+
| build_args      | Build arguments for container image |
+-----------------+-------------------------------------+
| use_commit_hash | Use current commit hash as tag      |
+-----------------+-------------------------------------+

Env
===

Git
===

Grants
======

Job
===

System
======

