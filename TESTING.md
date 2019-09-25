# Overview

Tapis CLI implements a (hopefully) consistent grammar and syntax: `tapis
<service> <entity> <action>`. In cases where there's nested
functionality (such as with permissions), the command structure is
`tapis <service> <entity> <sub-entity> <action>`.

  - Search and discovery actions:
      - list - generic list of known entities
      - search - parameterized search of known entities
      - show - display full record for one known entity

  - File management:
    - download - fetch Tapis remote asset(s) to local storage
    - upload - send asset(s) to Tapis from local storage

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
exercise it like you would the legacy CLI. But, specific new features
that testers can help review on are laid out below by service.

## Known Issues

The following are **known issues** and will be addressed in future work periods:

> 1.  Python 2.7.x is not supported (but will be)
> 2.  ~~No **files** commands are implemented~~
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

20-09-2019 | The CLI is installable from git checkout
  - It must be installable in **editable** mode (`pip install -e
    .`)
  - It must be installable in a virtual environment
  - It must be installable using setuptools (`python setup.py
    install`)
  - It must be installable under Python 3.5, 3.6, and 3.7
    (Python 2.7 support is forthcoming)

Please test the CLI under your favorite Python enviroment
management practices so we can make sure it's relatively robust for
the end user communities that will use it.

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

## Configuration

20-09-2019 |The CLI uses .env files and environment variables to configuring
some persistent settings. This will be described in more detail in
future testing sessions.

## Auth

27-09-2019 | No changes

20-09-2019 | This release marks debut of a simplified authentication workflow
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

27-09-2019 | No changes

20-09-2019 | Feel free to exercise the entire *apps* lifecycle save for cloning. Creation,
updating, publishing, search & discovery, and sharing are all implemented.

## Jobs

27-09-2019 | Implementations of the legacy `jobs-output-list` and `jobs-output-get` commands
are now available. Note the added flexibility in the `tapis jobs outputs download`
command:
* Download to the current directory via `--cwd` option
* Force overwrite of local files with `--force`
* Overwrite local files only of different with `--sync`
* Report progress to STDERR with `--progress`
* Specify remote files to skip with the `--exclude` option

The following downloads outputs from a designated job to the current working
directory, ignoring any files that seem to have already been downloaded. The
command reports a table, as shown below.

```shell
tapis jobs outputs download 9e74b852-0e1f-4363-8c09-5ab9f5299797-007 --cwd --sync
+-------------+-------+
| Field       | Value |
+-------------+-------+
| downloaded  | 4     |
| skipped     | 1     |
| warnings    | 0     |
| elapsed_sec | 5     |
+-------------+-------+
```

The `-v` verbose view enumerates each the outcome of each attempted download.

```json
{
  "downloaded": [],
  "skipped": [
    "/20190221t174839.err",
    "/20190221t174839.out",
    "/20190221t174839.pid",
    "/wc-sample.txt",
    "/wc_out/output.txt"
  ],
  "warnings": [],
  "elapsed_sec": 1
}
```

20-09-2019 | Key Aloe *jobs* functions are implemented save for permission management,
hide, and unhide. One interesting new feature of `tapis jobs show` is the `-T`
option, which will translate the verbose Aloe jobs output into a JSON
request document that can be used to submit a similar job.

## Files

27-09-2017 | File listing, inspection, and downloads (including recursive) are now implemented.

## Systems

27-09-2019 | No changes

20-09-2019 | Core Tapis *systems* functions are implemented. Queue management is still missing as
is the ability to atomically update a system's login inforamation.

## Metadata

27-09-2019 | No changes

20-09-2019 | Metadata search and list are implemented. Creation and update of metadata
records is not implemented, nor are permissions or metadata JSON schemas.

## Profiles

27-09-2019 | No changes

20-09-2019 | Viewing of another user's profile as well as that of the currently logged-in
user is supported. List and search are not implemented at present.

## Notifications

27-09-2019 | No changes

20-09-2019 | No notifications commands are ready to test

## Postits

27-09-2019 | No changes

20-09-2019 | No postits commands are ready to test

