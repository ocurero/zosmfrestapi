A Python wrapper for the z/OSMF© REST API
=========================================

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active) [![builds.sr.ht status](https://builds.sr.ht/~ocurero/zosmfrestapi/commits/main/.build.yml.svg)](https://builds.sr.ht/~ocurero/zosmfrestapi/commits/main/.build.yml?) ![z/OS](https://img.shields.io/badge/works%20on-z/OS-8A2BE2)

* Open Source: MIT License.
* Website: <https://sr.ht/~ocurero/zosmfrestapi/>
* Pypi: <https://pypi.org/project/zosmfrestapi/>


Install
-------

**zosmfrestapi** requires Python 3.12 or newer and access to a z/OSMF server.
You can check your Python version with:

```console
python --version
```

It is a good idea to use a virtual environment so this package does not affect
other Python projects. From a terminal, create and activate one in your project
folder:

```console
# Windows (PowerShell)
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1

# macOS or Linux
python3 -m venv .venv
source .venv/bin/activate
```

Then install the package from PyPI:

```console
python -m pip install zosmfrestapi
```

If you have downloaded or cloned the source code, run this from the project's
root folder instead:

```console
python -m pip install .
```

## First request

Save this as `example.py` and run it with `python example.py`. Enter the base
URL of your z/OSMF server when prompted (for example,
`https://zosmf.example.com:443`). The URL should include `https://` and any
required port, but not an API path such as `/zosmf`.

The password is requested without displaying it and is not stored in the
script. Replace the sample operation with one your z/OSMF user is authorized to
perform.

```python
from getpass import getpass

from zosmfrestapi import ZosmfClient, ZosmfError

server = input("z/OSMF server URL: ").strip().rstrip("/")
username = input("User ID: ").strip()
password = getpass("Password: ")

try:
    with ZosmfClient(server, username=username, password=password) as client:
    for instance in client.list_swis():
        print(f"{instance.name} ({instance.system})")
except ZosmfError as error:
    print(f"The z/OSMF request failed: {error}")
```

The `with` block closes the network connection automatically, even if a request
fails. `list_swis()` returns Python objects; the example prints each software
instance's name and system. You can also query systems or read a data set. Put
these calls inside the `with` block shown above, before it ends:

```python
systems = client.get_systems()
contents = client.read_dataset("USER.DATASET")
```

These calls must be made inside the `with` block, before the client is closed.
For a partitioned data set member, use a name such as
`USER.PDS(MEMBER)`.

## Authentication and TLS

The client uses the server's normal TLS certificate checks by default. Keep
those checks enabled for routine use. The HTTP transport is HTTPX2, a fork of
HTTPX; HTTPX2 uses `truststore` to integrate operating-system certificate
stores when it creates its default TLS context. This package currently passes
its own context, created with Python's `ssl.create_default_context()`, so the
certificates available to Python are used. If the z/OSMF server's CA is not
trusted in that environment, pass its certificate file with `cafile` below.

| Situation | Client option |
| --- | --- |
| User ID and password | `username="...", password="..."` |
| Client certificate and key in separate files | `cert=("client.crt", "client.key")` |
| Client certificate and key in one PEM file | `cert="client.pem"` |
| Internal certificate authority | `cafile="company-ca.pem"` |
| Existing LTPA or JWT token | `ltpa_token="..."` or `jwt_token="..."` |
| Network proxy | `proxy="http://proxy.example.com:8080"` |

For example, to trust an internal certificate authority, pass `cafile` when
creating the client:

```python
with ZosmfClient(server, username=username, password=password,
                 cafile="company-ca.pem") as client:
    systems = client.get_systems()
```

Avoid putting passwords or tokens directly in scripts, committing them to
version control, or sharing them in logs. The `insecure=True` option disables
TLS certificate verification; use it only for temporary diagnostics, never as
a production fix. It cannot be combined with `cert` or `cafile`.

## What you can do

The client provides synchronous methods for:

* Authentication (`authenticate`).
* z/OSMF groups and systems (`get_groups`, `get_systems`).
* Data sets (`read_dataset`).
* Software instances and SMP/E information (`list_swis`, `get_swi_by_name`,
    `get_swi_by_uuid`, and related query methods).
* Workflows (list, inspect, create, start, wait for, cancel, and archive).
* Software updates (search, inspect, start, monitor, and cancel).

Some operations change z/OSMF state. Check the method documentation and make
sure your account has the required permissions before using them.

## Troubleshooting

* **Python version error:** install Python 3.12 or newer, then recreate the
    virtual environment with that interpreter.
* **401 / unauthorized:** check the server URL, user ID, password or token, and
    whether the account is authorized for the requested API.
* **Certificate verification error:** ask your z/OSMF administrator for the
    correct CA certificate and pass its path with `cafile`.
* **Connection or timeout error:** check that the server and port are reachable
    from your machine and that any required proxy is configured.
* **PowerShell will not activate the virtual environment:** use the Python
    executable inside `.venv\Scripts\python.exe` to run commands, or follow your
    organization's PowerShell policy guidance. Do not change the machine-wide
    execution policy just to install this package.

For the complete API, parameters, and return types, see the docstrings in the
package source and the project website.
