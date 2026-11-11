# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - Unreleased

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
