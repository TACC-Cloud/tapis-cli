#############
Release Notes
#############

Read below how Tapis CLI has improved over time. We follow semantic versioning,
so you can safely assume that upgrades across point.point releases will not
require you to change your existing workflows or usage patterns. The exception
to this is when we add entirely new commands or functions (such as
integration with GitHub or the like).

**************************
1.0.0 Alpha 3 (02-14-2020)
**************************

Added
-----

    - Support for ``tapis apps init`` command using CookieCutter templates
    - Support for the ``tapis apps deploy`` command using projects
    - Support for template variables inside submitted JSON docs
    - Support for project-specific configuration files
    - A first-run screen now captures AUP, COC, and user data collection consent
    - The ``tapis auth init`` command now captures details about the user's preferred container registry and git server
    - The ``files download`` command now supports ``--include`` as well as ``--exclude``
    - Support for canceling an in-progress job via ``tapis jobs cancel``

Changed
-------

    - Consolidated status, version info under ``info`` subcommand
    - Renamed ``settings`` commmand to config for brevity
    - Renamed ``metadata`` command to ``meta`` for brevity
    - Fixes to ``files download`` to handle single-file downloads to ``.`` directory
    - Rebuilt and restructured docs for clarity and completeness

Removed
-------

    - Nothing

