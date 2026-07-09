import logging
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Dict, Optional


LOGGER = logging.getLogger("dx_daemon.healthcheck")


@dataclass
class HealthCheckResult:
    url: str
    status_code: Optional[int]
    ok: bool
    latency_ms: float
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        return {
            "url": self.url,
            "status_code": self.status_code,
            "ok": self.ok,
            "latency_ms": round(self.latency_ms, 2),
            "error": self.error,
        }


def check_url_once(url: str, timeout_seconds: float = 5.0) -> HealthCheckResult:
    started = time.perf_counter()

    try:
        request = urllib.request.Request(url=url, method="GET")
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            status_code = response.getcode()
            ok = 200 <= status_code < 400
            latency_ms = (time.perf_counter() - started) * 1000
            return HealthCheckResult(
                url=url,
                status_code=status_code,
                ok=ok,
                latency_ms=latency_ms,
            )
    except urllib.error.HTTPError as exc:
        latency_ms = (time.perf_counter() - started) * 1000
        return HealthCheckResult(
            url=url,
            status_code=exc.code,
            ok=False,
            latency_ms=latency_ms,
            error=str(exc),
        )
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        latency_ms = (time.perf_counter() - started) * 1000
        return HealthCheckResult(
            url=url,
            status_code=None,
            ok=False,
            latency_ms=latency_ms,
            error=str(exc),
        )


def monitor_url(
    url: str,
    interval_seconds: float,
    timeout_seconds: float = 5.0,
    max_iterations: Optional[int] = None,
) -> None:
    if interval_seconds <= 0:
        raise ValueError("interval_seconds must be > 0")

    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be > 0")

    if max_iterations is not None and max_iterations <= 0:
        raise ValueError("max_iterations must be > 0 when provided")

    iteration = 0
    LOGGER.info(
        "Starting endpoint monitor. url=%s interval=%s timeout=%s max_iterations=%s",
        url,
        interval_seconds,
        timeout_seconds,
        max_iterations,
    )

    while True:
        iteration += 1
        result = check_url_once(url=url, timeout_seconds=timeout_seconds)

        if result.ok:
            LOGGER.info("Healthcheck pass #%s: %s", iteration, result.to_dict())
        else:
            LOGGER.warning("Healthcheck fail #%s: %s", iteration, result.to_dict())

        if max_iterations is not None and iteration >= max_iterations:
            LOGGER.info("Endpoint monitor finished after %s iterations.", iteration)
            break

        time.sleep(interval_seconds)
