import argparse
import logging

from .daemon import run_daemon
from .cli_healthcheck import add_healthcheck_subcommand, run_healthcheck_from_args


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the dx-daemon process.")
    subparsers = parser.add_subparsers(dest="command")

    daemon_parser = subparsers.add_parser("daemon", help="Run heartbeat daemon loop.")
    daemon_parser.add_argument(
        "--interval",
        type=float,
        default=5.0,
        help="Heartbeat interval in seconds (default: 5.0).",
    )
    daemon_parser.add_argument(
        "--max-iterations",
        type=int,
        default=None,
        help="Optional number of iterations before exiting.",
    )
    add_healthcheck_subcommand(subparsers)

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Log verbosity (default: INFO).",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )

    if args.command == "healthcheck":
        run_healthcheck_from_args(args=args, parser=parser)
        return

    interval = getattr(args, "interval", 5.0)
    max_iterations = getattr(args, "max_iterations", None)

    if interval <= 0:
        parser.error("--interval must be > 0")
    if max_iterations is not None and max_iterations <= 0:
        parser.error("--max-iterations must be > 0")

    run_daemon(interval_seconds=interval, max_iterations=max_iterations)


if __name__ == "__main__":
    main()
