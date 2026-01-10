from fastapi import FastAPI
from api.events.model_manager import model_manager
import asyncio
from api.monitors.api_metric.otel_setup import setup_metrics

def register_startup_event(app: FastAPI):
    @app.on_event("startup")
    async def startup_event():
        setup_metrics()
        await asyncio.to_thread(model_manager.load_model)
        model, model_type = model_manager.get_model()