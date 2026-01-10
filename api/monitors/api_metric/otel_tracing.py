# monitoring/api/otel_tracing.py
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

tracer_provider = TracerProvider()
tracer = tracer_provider.get_tracer("fastapi-api-tracer")

# Export OTLP vers Prometheus / collector
otlp_exporter = OTLPSpanExporter()

span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)