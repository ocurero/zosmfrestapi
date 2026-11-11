# Contributing to zosmfrestapi

Thank you for your interest in contributing to **zosmfrestapi**! This guide explains how to set up the development environment, run checks and tests, and propose changes via SourceHut (sr.ht).

---

## Prerequisites

- **Python**: `>= 3.12`
- **[Poetry](https://python-poetry.org/)**: Dependency and environment manager
- Access to a **z/OSMF server** (optional for unit tests, as tests use recorded cassettes with `pytest-recording` / `vcrpy`)

---

## Development Setup

1. **Clone the repository**:

   ```bash
   git clone https://git.sr.ht/~ocurero/zosmfrestapi
   cd zosmfrestapi
   ```

2. **Install dependencies and development tools**:

   ```bash
   poetry install --all-groups
   ```

   This installs:
   - Core runtime dependencies (`httpx2`, `pendulum`, `dacite`).
   - Development dependency groups (`dev` with `pytest`, `black`, `flake8`, `mypy`, `poethepoet`, and `zcrypto-dev` with `cryptography`).

   > **Note on `zcrypto`:** The optional extra `zcrypto` (`py_zcrypto`) requires z/OS C headers (`gskcms.h`) and is only installable on z/OS. On Linux, macOS, and Windows, mock fixtures are provided by `zcrypto-dev` (`cryptography`) so unit tests run and pass without needing `py_zcrypto`.

---

## Running Quality Checks and Tests

The project uses [Poe the Poet](https://github.com/nat-n/poethepoet) to manage common tasks defined in [pyproject.toml](file:///home/oscar/dev/projects/zosmfrestapi/pyproject.toml).

### The `check` Command

Before submitting any patch or pull request, you **must** ensure that all quality gates pass by running:

```bash
poetry run poe check
```

This command runs sequentially:
1. `black --check .` — Verifies code formatting (line length 96).
2. `flake8 zosmfrestapi` — Lints the library code.
3. `pyright --warnings` — Static type checker.
4. `mypy zosmfrestapi` — Additional strict type checking.
5. `pytest` — Runs the test suite and verifies **100% test coverage** (`--cov-fail-under=100`).

### Individual Commands

You can also run individual tasks:

- **Format code**:
  ```bash
  poetry run poe format
  ```
- **Lint check**:
  ```bash
  poetry run poe lint
  ```
- **Run tests only**:
  ```bash
  poetry run poe test
  ```
  *(or directly: `poetry run pytest`)*

---

## Code Style & Guidelines

- **Formatting**: We use [Black](https://github.com/psf/black) with a maximum line length of `96` characters.
- **Linting**: Follow PEP 8 via `flake8`.
- **Test Coverage**: We enforce **100% test coverage** across the codebase. Any new features or bug fixes must include corresponding tests.
- **Cassettes**: Integration tests against z/OSMF use `pytest-recording`. If modifying existing tests, cassette playback is enforced by default (`--record-mode=none`).

---

## Project Structure

```
zosmfrestapi/
├── zosmfrestapi/
│   ├── exceptions/        # Domain-specific exceptions
│   ├── models/            # Dataclasses & response models (via dacite)
│   ├── services/          # Endpoint service implementations
│   ├── testing/           # Test helpers and fixtures
│   ├── client.py          # ZosmfClient main entry point
│   ├── utils.py           # Helper utilities
│   ├── zcrypto.py         # Cryptographic helpers
│   └── zcrypto_client.py  # ZosmfZcryptoClient entry point
├── tests/
│   ├── cassettes/         # Recorded HTTP interactions for tests
│   ├── conftest.py        # Pytest configuration and shared fixtures
│   └── test_*.py          # Test suites
├── .build.yml             # SourceHut builds CI definition
├── pyproject.toml         # Dependencies, optional extras (zcrypto), tools, and poe tasks
└── README.md
```

---

## Submitting Changes (SourceHut Workflow)

The project repository and CI are hosted on [SourceHut](https://sr.ht/~ocurero/zosmfrestapi/). SourceHut supports patch submission via email as well as Git pull requests.

### Option 1: SourceHut Web / Git PR (Recommended)

1. **Fork or push to your own Git repository** (on SourceHut or any publicly accessible Git remote):
   ```bash
   # Example: push your branch to your own personal SourceHut repo
   git remote add myfork git@git.sr.ht:~yourusername/zosmfrestapi
   git push myfork your-feature-branch
   ```

2. **Submit a Pull Request on SourceHut**:
   - Go to the repository on SourceHut: [https://sr.ht/~ocurero/zosmfrestapi/](https://sr.ht/~ocurero/zosmfrestapi/)
   - Navigate to the **Send pull request** / **Submit PR** section.
   - Enter your public Git clone URL and branch name.
   - Summarize your changes and submit.

### Option 2: Patch submission via email (git send-email)

If you prefer the standard email patch workflow:

1. **Prepare your commits** (focused, logical, and passing `poetry run poe check`).
2. **Format patches**:
   ```bash
   git format-patch origin/main
   ```
3. **Send patches to the maintainer / mailing list**:
   ```bash
   git send-email --to="dev@curero.es" 0001-*.patch
   ```

---

## Reporting Issues

Found a bug or need a feature? You can open a ticket on the SourceHut tracker or send an email to [dev@curero.es](mailto:dev@curero.es).
