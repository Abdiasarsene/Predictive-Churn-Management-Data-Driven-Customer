# monitoring/api/otel_instrumentation.py
from starlette.middleware.base import BaseHTTPMiddleware
from .otel_metrics import request_count, request_latency
from time import time

class OTelMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time()
        response = await call_next(request)

        # métriques API
        request_count.add(1)
        request_latency.record(time() - start)

        return response

def setup_otel(app):
    app.add_middleware(OTelMiddleware)