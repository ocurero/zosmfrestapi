### WARNING, this repository is a read-only mirror!
*See [sourcehut](https://sr.ht/~ocurero/zosmfrestapi/) for PR and latest news*

# A Python wrapper for the z/OSMF REST API

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![builds.sr.ht status](https://builds.sr.ht/~ocurero/zosmfrestapi/commits/main/.build.yml.svg)](https://builds.sr.ht/~ocurero/zosmfrestapi/commits/main/.build.yml?)
[![100% coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://builds.sr.ht/~ocurero/zosmfrestapi/commits/main/.build.yml?)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![z/OS](https://img.shields.io/badge/works%20on-z/OS-8A2BE2)

* Website: <https://sr.ht/~ocurero/zosmfrestapi/>
* Repository: <https://git.sr.ht/~ocurero/zosmfrestapi>
* Changelog: <https://git.sr.ht/~ocurero/zosmfrestapi/tree/main/item/CHANGELOG.md>

Key features:
* **Pure Python**: Package and its dependencies are 100% pure Python (no C extensions required).
* **Cross-platform**: Works on Windows, Linux, macOS, and z/OS UNIX System Services.
* **Flexible authentication**: Supports user/password, LTPA and JWT tokens, and mutual TLS (mTLS).
* **Proxy ready**: Full support for standard HTTP/HTTPS proxies as well as authenticated proxies.

![ZosmfClient demo](../docs/ZosmfClient.gif)


Install
-------

**zosmfrestapi** requires Python 3.12 or newer and access to a z/OSMF server.

Install the package from PyPI:

```console
python -m pip install zosmfrestapi
```

If you have downloaded or cloned the source code, run this from the project's
root folder instead:

```console
python -m pip install .
```

## Quickstart

```python

from zosmfrestapi import ZosmfClient

with ZosmfClient(server, username="demouser", password="itsasecret") as client:
    for instance in client.list_swis():
        print(f"{instance.name} ({instance.system})")
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

## Clients

The library provides two client implementations:

* **`ZosmfClient`**: The standard synchronous client for communicating with z/OSMF using username/password, tokens, or standard TLS certificate files.
* **`ZosmfZcryptoClient`**: A specialized client for z/OS environments that extracts mutual TLS (mTLS) client certificates directly from SAF key rings (RACF, ACF2, Top Secret).

### Platform Support

| Client | Linux | macOS | Windows | z/OS USS |
| --- | :---: | :---: | :---: | :---: |
| `ZosmfClient` | ✅ | ✅ | ✅ | ✅ |
| `ZosmfZcryptoClient` | ❌ | ❌ | ❌ | ✅ |

### Using `ZosmfZcryptoClient` on z/OS

![ZosmfZcryptoClient demo](../docs/ZosmfZcryptoClient.gif)

`ZosmfZcryptoClient` retrieves client certificates and private keys directly from a SAF key ring, exporting temporary PEM files and configuring mutual TLS transparently. When using a key ring owned by the current user, specify the ring name as "name". When using a key ring owned by another user, specify the ring name as "userid/name":

```python
from zosmfrestapi import ZosmfZcryptoClient

with ZosmfZcryptoClient(
    "https://zosmf.example:443",
    keyring="userid/name",
    label="zOSMF Client Certificate",
) as client:
    systems = client.get_systems()
```

Install the optional `zcrypto` extra:

```console
python -m pip install "zosmfrestapi[zcrypto]"
```

> [!WARNING]
> The `zcrypto` extra requires `py_zcrypto`, a C extension that compiles against z/OS System SSL C headers. Therefore, it can **only** be installed and executed on **z/OS** systems. Attempting to install or use `ZosmfZcryptoClient` on Linux, macOS, or Windows will raise a `RuntimeError`.



## Authentication and TLS

The client uses the server's normal TLS certificate checks by default. Keep
those checks enabled for routine use. The HTTP transport is HTTPX2; HTTPX2 uses `truststore`
to integrate operating-system certificate stores when it creates its default TLS context.
zosmfrestapi currently passes its own context, created with Python's
`ssl.create_default_context()`, so the certificates available to Python are used.
If the z/OSMF server's CA is no trusted in that environment, pass its certificate file
with `cafile` below.

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

The `insecure=True` option disables TLS certificate verification; use it only for temporary
diagnostics, never as a production fix. It cannot be combined with `cert` or `cafile`.

## Supported APIs

| API Category | Description | Key Methods (examples) |
| --- | --- | --- |
| **Authentication** | Basic Auth, LTPA / JWT tokens session login | `authenticate()` |
| **Topology** | Query systems and sysplex groups defined in z/OSMF | `get_groups()`, `get_systems()` |
| **Datasets** | Sequential and partitioned dataset retrieval | `read_dataset()` |
| **Software Management** | SMP/E software instances, CSI queries, and datasets | `list_swis()`, `get_swi_by_name()`, `query_csi_by_name()` |
| **Software Updates** | Search, inspect, start, monitor, and cancel update processes | `search_sw_updates_by_name()`, `start_sw_update_by_name()`, `check_sw_update_status()` |
| **Workflows** | List, create, inspect, execute, monitor, and archive workflows | `get_workflows()`, `create_workflow()`, `start_workflow()`, `wait_for_workflow()` |

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

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on development, testing, and submitting patches.

## Issues and Feedback

If you encounter any bugs or have feature requests, please report them on the [SourceHut issue tracker](https://todo.sr.ht/~ocurero/zosmfrestapi).

## License

The MIT License. See [LICENSE](../LICENSE).

## Trademarks

IBM, the IBM logo, z/OS, MVS, and Z/OSMF are trademarks or are
registered trademarks of International Business Machines Corporation,
registered in many jurisdictions worldwide.  Other product and service
names might be trademarks of IBM or other companies. A current list
of IBM trademarks is available at <https://www.ibm.com/legal/copytrade>.

This project is an independent community effort. It is not affiliated
with, endorsed by, or sponsored by IBM.
