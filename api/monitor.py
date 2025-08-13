# Modules required imported 
from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client  import Counter, Histogram
import time 
import logging
import traceback

# ======= LOGGING =======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== PROMETHEUS METRICS ======
# 1. Model inference count
model_inference_count = Counter(
    "ml_model_inference_total",
    "Inference count realized per model"
)

# 2. Failed request count 
failed_request_count = Counter(
    "failed_requests_total",
    "Total of request failed"
)

# 3. Total of successful request
successful_request_count = Counter(
    "successful_request_total",
    "Total of successufl reequest"
)

# 4. Request of duration
request_duration = Histogram(
    "request_duration_seconds",
    "Request of duration"
)

# ====== FASTAPI SERVER FOR ADDIND ======
def add_monitoring(app:FastAPI):
    try:
        instrumentator = Instrumentator()
        instrumentator.instrument(app).expose(app, endpoint="/metrics")
        logger.info("✅ Prometheus monitoring activated on /metrics")
    except Exception as e:
        logger.error(f"❌ Error detected : {str(e)}")
        logger.debug(f"🟢 Complete traceback : {traceback.format_exc()}")

# ======= MANUAL METRICS OF MIDDLEWARE ======
async def metrics_middleware(request:Request, call_next):
    start = time.time()
    try:
        response = await call_next(request)
        successful_request_count.inc()
        return response
    except Exception:
        failed_request_count.inc()
        raise
    finally:
        duration = time.time() - start
        request_duration.observe(duration)

# ====== CODE TO USE FOR COUNTING ======
def increment_inference_count():
    try:
        model_inference_count.inc()
        logger.debug("🔃 Incrementation of model_inference_count")
    except Exception as e:
        logger.error(f"❌ Error detected : {str(e)}")
        logger.debug(f"🟢 Complete traceback : {traceback.format_exc()}")