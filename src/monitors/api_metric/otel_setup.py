from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

def setup_metrics():
    # Exporter OTLP (vers Collector)
    exporter = OTLPMetricExporter(endpoint="http://otel-collector:4318/v1/metrics")
    reader = PeriodicExportingMetricReader(exporter)

    provider = MeterProvider(metric_readers=[reader])
    metrics.set_meter_provider(provider)

    # Exemple de compteur
    meter = metrics.get_meter("fastapi-api-meter")
    counter = meter.create_counter("requests_total")
    counter.add(1, {"route": "/startup"})