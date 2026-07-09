import argparse

from .healthcheck import monitor_url


def add_healthcheck_subcommand(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "healthcheck",
        help="Continuously monitor an HTTP endpoint and log status/latency.",
    )
    parser.add_argument("--url", required=True, help="URL to monitor.")
    parser.add_argument(
        "--interval",
        type=float,
        default=10.0,
        help="Seconds between checks (default: 10.0).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="HTTP timeout per request in seconds (default: 5.0).",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=None,
        help="Optional number of checks before exiting.",
    )


def run_healthcheck_from_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    if args.interval <= 0:
        parser.error("--interval must be > 0")
    if args.timeout <= 0:
        parser.error("--timeout must be > 0")
    if args.max_iterations is not None and args.max_iterations <= 0:
        parser.error("--max-iterations must be > 0")

    monitor_url(
        url=args.url,
        interval_seconds=args.interval,
        timeout_seconds=args.timeout,
        max_iterations=args.max_iterations,
    )
