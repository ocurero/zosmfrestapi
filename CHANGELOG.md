# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-11-14

### Added
- **Terminal Demo Recordings**: Added VHS recording tapes and rendered terminal GIFs (`docs/ZosmfClient.gif`, `docs/ZosmfZcryptoClient.gif`) demonstrating `ZosmfClient` and `ZosmfZcryptoClient`.
- **Enhanced Documentation**: Updated `README.md` and `CONTRIBUTING.md` with demo recordings, platform support matrix, client comparisons, supported APIs overview, and full documentation of Poe tasks and project architecture.
- **Dedicated Common Exceptions Module**: Created `zosmfrestapi.exceptions.commons` containing base exceptions (`ZosmfError`, `ZosmfAuthError`).
- **Models Namespace Exports**: Added public exports in `zosmfrestapi.models` for cleaner domain model imports.

### Changed
- **Streamlined Top-Level Exports**: Cleaned up `zosmfrestapi/__init__.py` to export only the client classes (`ZosmfClient`, `ZosmfZcryptoClient`), avoiding namespace pollution. Models and exceptions are now imported from their respective submodules (`zosmfrestapi.models` and `zosmfrestapi.exceptions`).
- **Internal Utilities**: Renamed public `zosmfrestapi/utils.py` to private `zosmfrestapi/_utils.py` and converted `_parse_datetime` to `parse_datetime`.
- **Granular Poe Tasks**: Restructured `poethepoet` tasks into logical groups (`quality` and `testing`):
  - `quality`: Runs `black`, `flake8`, `mypy`, and `pyright`.
  - `client_tests`: Runs core client test suite with coverage isolation (omitting `zcrypto`).
  - `zcrypto_tests`: Runs zcrypto test suite independently with targeted coverage.
  - `tests` and `check`: Composite tasks running all test suites and quality gates.
- **CI Pipeline Optimization**: Updated `.build.yml` to run quality checks and test suites in separate steps with environment isolation for optional `zcrypto-dev` dependencies.

## [0.2.1] - 2026-11-12

### Added
- **CSRF Protection Header**: Added default `X-CSRF-ZOSMF-HEADER` header to all HTTP requests, required by z/OSMF REST endpoints to prevent CSRF attacks.
- **User-Agent Header**: Added `User-Agent: zosmfrestapi/<version>` header to identify client requests.

### Changed
- Switched to `poetry-dynamic-versioning` for automatic package versioning from Git tags.
- Fixed documentation links in README to use absolute SourceHut repository URLs.

## [0.2.0] - 2026-11-11

### Added
- **SAF Key Ring Support (`ZosmfZcryptoClient`)**: Added support for mutual TLS (mTLS) authentication using client certificates stored directly in SAF key rings on z/OS via the optional `py_zcrypto` dependency (`pip install "zosmfrestapi[zcrypto]"`).
- **Encrypted Private Key Support**: Added `key_password` argument to `ZosmfClient` and base services to support password-protected private keys in mTLS authentication.
- **PEP 561 Compliance**: Added `py.typed` marker file to provide inline type hint annotations for type checkers.
- **Development Tooling**: Integrated `poethepoet`, `flake8`, `mypy`, and `pyright` for linting, type-checking, and task running (`poe check`, `poe lint`, `poe format`).
- **Contributing Guidelines**: Added `CONTRIBUTING.md`.

### Changed
- Refactored authentication and client tests, introducing dedicated unit tests for `ZosmfClient`, `ZosmfZcryptoClient`, and improved mock fixtures.
- Updated line length formatting configuration from 88 to 96 characters across tools (`black`, `flake8`).
- Cleaned up build CI pipeline (`.build.yml`) and removed tracked `poetry.lock`.

## [0.1.0] - 2026-11-06

### Added
- Initial release of `zosmfrestapi`.
- Synchronous client (`ZosmfClient`) for the z/OSMF REST API.
- Support for multiple authentication methods: Basic Auth (username/password), LTPA tokens, JWT tokens, and mutual TLS (client certificates).
- Support for HTTP and authenticated proxies.
- Services for Datasets, Topology, Workflows, Software Management, and Software Update processes.
