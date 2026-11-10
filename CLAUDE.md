# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`dx-daemon` is a lightweight, stdlib-only Python daemon starter for DX experiments. The installable package lives in `src/dx_daemon/`; `javascript_samples/` and `ruby_samples/` are unrelated standalone DX scripts (not part of the package or its build).

## Commands

Requires Python 3.9+. No runtime dependencies (standard library only).

```bash
# Setup (the pip upgrade is required: stock Python 3.9 ships pip 21.2.4, which
# predates PEP 660 and cannot do an editable install of a pyproject-only project)
python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install -e .

# Run via installed console script
dx-daemon daemon --interval 2
dx-daemon daemon --interval 1 --max-iterations 5
dx-daemon healthcheck --url "https://example.com" --interval 10 --timeout 3

# Run without installing
PYTHONPATH=src python3 -m dx_daemon.cli daemon --interval 1
```

`--log-level {DEBUG,INFO,WARNING,ERROR}` is a top-level flag on the root parser, so it must precede the subcommand.

Linting and formatting use Ruff, configured in `pyproject.toml` and installed via the `dev` extra:

```bash
pip install -e ".[dev]"
ruff check src/dx_daemon        # add --fix to auto-fix
ruff format src/dx_daemon
```

Ruff covers only the five package files (`cli.py`, `cli_healthcheck.py`, `daemon.py`, `healthcheck.py`, `__init__.py`); the standalone scratch scripts under `src/dx_daemon/` plus `javascript_samples/` and `ruby_samples/` are listed in `extend-exclude`. `target-version = "py39"` is tied to the `requires-python` floor — do not let `UP` rules introduce 3.10+ syntax. `line-length = 100` accommodates the existing long log/signature lines.

There is no test suite configured in this repo.

## Architecture

The `dx_daemon` package is a CLI with two subcommands wired through `argparse`:

- **`cli.py`** — builds the parser and dispatches. Note the asymmetry: the `daemon` subcommand's arguments are defined inline in `build_parser()` and executed directly in `main()`, while the `healthcheck` subcommand is fully delegated (both its argument definitions and its execution) to `cli_healthcheck.py`. When adding a subcommand, follow the delegated `healthcheck` pattern rather than the inline `daemon` one.
- **`daemon.py`** — `run_daemon()` is the heartbeat loop. It installs `SIGINT`/`SIGTERM` handlers that flip a `DaemonState.running` flag for graceful shutdown, and supports an optional `max_iterations` bound for finite/testable runs.
- **`healthcheck.py`** — `check_url_once()` performs one `urllib`-based GET returning a `HealthCheckResult` dataclass (status, ok, latency, error); `monitor_url()` polls it on an interval. This is the core logic layer, decoupled from argparse.
- **`cli_healthcheck.py`** — the argparse glue for the healthcheck subcommand, separating CLI concerns from the logic in `healthcheck.py`.

Validation is duplicated by design: both `cli.py`/`cli_healthcheck.py` (via `parser.error`, for CLI users) and the core functions in `healthcheck.py` (via `raise ValueError`, for direct library callers) guard `interval`/`timeout`/`max_iterations`. Keep both in sync when changing bounds.

The package's public API is re-exported from `src/dx_daemon/__init__.py` (`run_daemon`, `check_url_once`, `monitor_url`).
