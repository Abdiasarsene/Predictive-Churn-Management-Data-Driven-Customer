# api/monitors/api_metric/otel_metrics.py

from opentelemetry import metrics

meter = metrics.get_meter("fastapi-api-metrics")

# 1️⃣ Latence
request_latency = meter.create_histogram(
    name="api_request_latency_seconds",
    description="API latency",
    unit="s"
)

# 2️⃣ Volume
request_count = meter.create_counter(
    name="api_requests_total",
    description="Total API requests"
)