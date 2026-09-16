# dx-daemon

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
pip install -e .
```

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

## Next ideas

- Add a real background service mode (launchd/systemd)
- Add health checks and metrics
- Add integration hooks for DX APIs and job runners
