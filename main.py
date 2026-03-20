# main.py
import logging
from fastapi import FastAPI
from src.routers.routes import router as predict_router
from src.utils.secure import apply_security_middleware
from src.monitors.api_metric.otel_instrumentation import setup_otel
from src.events.event import register_startup_event
from src.utils.config import settings
from src.routers.metrics_router import router as metrics_router

# ====== LOGGER ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description=settings.api_description
    )

    # Middleware sécurité
    apply_security_middleware(app)
    logger.info("🔐 Security middleware applied")

    # Observabilité OTEL
    setup_otel(app)
    logger.info("📊 OTEL instrumentation configured")

    # Startup events
    register_startup_event(app)
    logger.info("⚡ Startup events registered")

    # Routes
    app.include_router(predict_router)
    logger.info("📦 API routes included")

    # Metrics
    app.include_router(metrics_router)
    logger.info("📦 Metrics included")

    logger.info("✅ FastAPI application created and fully configured")
    return app

# ====== APP INSTANCE ======
app = create_app()