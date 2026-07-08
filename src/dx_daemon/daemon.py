import logging
import signal
import time
from dataclasses import dataclass
from typing import Optional


LOGGER = logging.getLogger("dx_daemon")


@dataclass
class DaemonState:
    running: bool = True


def run_daemon(interval_seconds: float, max_iterations: Optional[int] = None) -> None:
    """Run the daemon loop until interrupted or until max iterations are reached."""
    state = DaemonState()
    iterations = 0

    def _stop(_signum: int, _frame: object) -> None:
        LOGGER.info("Shutdown signal received. Stopping daemon.")
        state.running = False

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    LOGGER.info("Daemon started. interval=%ss max_iterations=%s", interval_seconds, max_iterations)

    while state.running:
        iterations += 1
        LOGGER.info("Heartbeat #%s", iterations)

        if max_iterations is not None and iterations >= max_iterations:
            LOGGER.info("Reached max iterations. Exiting.")
            break

        time.sleep(interval_seconds)

    LOGGER.info("Daemon stopped.")
