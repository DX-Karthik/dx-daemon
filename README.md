# dx-daemon

Hello from the README update.

A lightweight Python daemon starter for DX experiments.

Repository: https://github.com/DX-Karthik/dx-daemon

## What this includes

- A small long-running daemon loop with heartbeat logging
- Graceful shutdown handling for `SIGINT` and `SIGTERM`
- A CLI with configurable interval and optional max iteration limit
- A simple project layout you can extend quickly

## Quickstart

1. Use Python 3.9+.
2. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

The `pip install --upgrade pip` step is required, not optional: the pip bundled
with stock Python 3.9 (21.2.4 on macOS) predates PEP 660 and cannot install a
`pyproject.toml`-only project in editable mode. Without it `pip install -e .`
fails with `File "setup.py" or "setup.cfg" not found`.

3. Run the heartbeat daemon:

```bash
dx-daemon daemon --interval 2
```

To run for a fixed number of iterations:

```bash
dx-daemon daemon --interval 1 --max-iterations 5
```

Monitor an HTTP endpoint:

```bash
dx-daemon healthcheck --url "https://example.com" --interval 10 --timeout 3
```

## Development

Run directly without installing:

```bash
PYTHONPATH=src python3 -m dx_daemon.cli daemon --interval 1
```

### Linting

```bash
pip install -e ".[dev]"
ruff check src/dx_daemon
ruff format src/dx_daemon
```

`ruff check --fix src/dx_daemon` auto-fixes import order and most style issues.
Config lives in `pyproject.toml`; the standalone scratch scripts under
`src/dx_daemon/` are excluded.

## Next ideas

- Add a real background service mode (launchd/systemd)
- Add health checks and metrics
- Add integration hooks for DX APIs and job runners
