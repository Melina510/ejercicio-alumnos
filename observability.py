import os
import time
from collections.abc import Callable

from fastapi import Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware


REQUEST_COUNT = Counter(
    "worldcup_http_requests_total",
    "Total HTTP requests handled by the simulator API.",
    ["method", "path", "status"],
)
REQUEST_LATENCY = Histogram(
    "worldcup_http_request_duration_seconds",
    "HTTP request latency in seconds.",
    ["method", "path"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
)
SIMULATION_RUNS = Counter(
    "worldcup_simulation_runs_total",
    "Total simulation runs.",
    ["status"],
)
SIMULATION_LATENCY = Histogram(
    "worldcup_simulation_duration_seconds",
    "Simulation runtime in seconds.",
    buckets=(0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10, 30),
)
INCIDENTS = Counter(
    "worldcup_incidents_total",
    "Synthetic incident activations detected by the simulator.",
    ["type"],
)


class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start = time.perf_counter()
        path = request.url.path

        if path == "/prometheus":
            return await call_next(request)

        try:
            response = await call_next(request)
            status = response.status_code
            return response
        except Exception:
            status = 500
            raise
        finally:
            elapsed = time.perf_counter() - start
            REQUEST_COUNT.labels(request.method, path, str(status)).inc()
            REQUEST_LATENCY.labels(request.method, path).observe(elapsed)


def metrics_response() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


def incident_mode_enabled() -> bool:
    return os.getenv("SIMULATOR_INCIDENT_MODE", "false").lower() in {"1", "true", "yes", "on"}
