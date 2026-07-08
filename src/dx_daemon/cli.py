import argparse
import logging

from .daemon import run_daemon


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the dx-daemon process.")
    parser.add_argument(
        "--interval",
        type=float,
        default=5.0,
        help="Heartbeat interval in seconds (default: 5.0).",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=None,
        help="Optional number of iterations before exiting.",
    )
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

    if args.interval <= 0:
        parser.error("--interval must be > 0")

    if args.max_iterations is not None and args.max_iterations <= 0:
        parser.error("--max-iterations must be > 0")

    run_daemon(interval_seconds=args.interval, max_iterations=args.max_iterations)


if __name__ == "__main__":
    main()
