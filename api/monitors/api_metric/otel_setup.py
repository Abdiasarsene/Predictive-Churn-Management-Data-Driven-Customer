from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader

def setup_metrics():
    prometheus_reader = PrometheusMetricReader()

    provider = MeterProvider(
        metric_readers=[prometheus_reader]
    )

    metrics.set_meter_provider(provider)