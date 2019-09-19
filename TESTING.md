# Overview

Tapis CLI implements a (hopefully) consistent grammar and syntax: `tapis
<service> <entity> <action>`. In cases where there's nested
functionality (such as with permissions), the command structure is
`tapis <service> <entity> <sub-entity> <action>`.

  - Search and discovery actions:

      - list - generic list of known entities
      - search - parameterized search of known entities
      - show - display full record for one known entity

  - Management actions:

      - create - create a new entity
      - update - update an existing entity by identifier
      - delete - delete an entity by identifier
      - disable - temporarily remove a resource from use
      - enable - restore a resource to use
      - publish - make a resource publicly usable
      - unpublish - remove a resource from public use

  - Permissions and roles:

      - list - list entitlements for entity by identifier
      - show - display a specific entitlement by identifier and username
      - grant - assign a role or permission for a username to an entity
      - revoke - remove role or permission for a username from an entity
      - drop - remove all granted roles/permissions from an entity

# What To Test

This tool is designed to completely (and quickly - by Q42019) replace
our legacy Bash tooling. So, our general request is to get in there an
exercise it like you would the legacy CLI. But, there are some specific
points that testers are encouraged to visit upon, which are laid out,
organized by service, below.

## Known Issues

First of all, the following are **known issues** and will be addressed
soon:

> 1.  Python 2.7.x is not supported (but will be)
> 2.  No **files** commands are implemented
> 3.  No **actors** or **tacclab** commands are implemented
> 4.  The **watch** function from the old jobs-submit is gone and will
>     never return
> 5.  Impersonation token issuance is not yet implemented
> 6.  The beloved `auth switch` is not yet implemented
> 7.  Metadata schema and record management commands are not yet
>     implemented
> 8.  No **notifications** commands are implemented
> 9.  The module is not yet available on PyPi
> 10. Documentation builds are broken
> 11. Creation of the Bash autocomplete config is broken
> 12. Search on dates is broken
> 12. Search on booleans can be broken (try `--boolean eq true`)

## Installation

  -   - The CLI must be installable from git checkout.

          - It must be installable in **editable** mode (`pip install -e
            .`)
          - It must be installable in a virtual environment
          - It must be installable using setuptools (`python setup.py
            install`)
          - It must be installable under Python 3.5, 3.6, and 3.7
            (Python 2.7 support is forthcoming)

## Configuration

## General CLI Capabilities

  - The name of every command must be intuitive and aligned with its
    function and (where possible) directly congruent with the underlying
    API functionality. I realize this is a matter of opinion, but its
    still a hard requirement.
  - Every command must have descriptive and accurate help text. This
    includes the command description and all options.
  - All commands must display a JSON response when run using the `-v`
    flag
  - Commands that list multiple records must implement `--limit` and
    `--offset` and those arguments should work as indicated
  - Commands that display a specific record follow the form `tapis <api>
    show <identifier>`. The name and description for each API's
    identifier must be correct. For instance, the name and description
    for Apps are `<app_id>` and `App identifer`, respectively
  - Commands that access Tapis APIs must support specification of access
    token via `-z` or `--token`. A valid token should always work, even
    if its an impersonation token. Invalid tokens should fail.
  - Commands that access Tapis APIs must allow base URL to be overridden
    via the `-H` option
  - The CLI must fail gracefully when networking is not available

## Auth

This release marks debut of a simplified authentication workflow
targeted at end users. In the new approach, one host-specific client is
generated and maintained for each combination of tenant and username. To
initialize a host to use Tapis, simply run the `tapis auth init`
command. Re-running it without changing tenant or username will simply
display the current auth context. Changing either of those values, or
specifying `--interactive` mode will re-initialize the host to use the
new tenant/username combination.

The `tapis auth show` command will display the current auth state, without
taking any action to update the Oauth token.

Token management should be much less manual than it has become in recent
months with the Bash CLI, in that you should almost never have to
manually create or refresh or a token. Should you need to do so, the
commands for doing so are `tapis auth tokens create` and `tapis auth
tokens refresh`

Switching between profiles ( `tapis auth switch`) is not currently
supported.

## Apps

Feel free to exercise the entire *apps* lifecycle. Creation, updating, publishing,
search & discovery, and sharing are all implemented.

## Jobs

All key Aloe *jobs* functions are implemented save for permission management,
hide, and unhide. One interesting new feature of `tapis jobs show` is the `-T`
option, which will translate the verbose Aloe jobs output into a JSON
request document that can be used to submit a similar job.

## Systems

Core Tapis *systems* functions are implemented. Queue management is still missing as
is the ability to atomically update a system's login inforamation.

## Metadata

Metadata search and list are implemented. Creation and update of metadata
records is not implemented, nor are permissions or metadata JSON schemas.

## Profiles

