# Modules required imported
import logging
import traceback 
import asyncio
from fastapi import FastAPI

from .model_loader import load_mlflow_model, load_bentoml_model
from .config import settings

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== SETTING ======
model = None 
model_type = None

# ====== LOADED MODELS ======
def get_model():
    return model, model_type

def register_startup_event(app: FastAPI):
    @app.on_event("startup")
    async def startup_event():
        logger.info("🚀 API Starting")
        global model, model_type
        
        # Mlflow Loading
        try:
            logger.info("🔃 MLflow Model Loaded")
            model = await asyncio.wait_for(asyncio.to_thread(load_mlflow_model, settings.mlflow_model), timeout=10.0)
            model_type = "MLflow"
            logger.info("🟢 MLflow model loaded")
        except Exception as e: 
            logger.warning(f"❌ Mlflow failed : {str(e)}")
            logger.debug(f"🟢 Complete Traceback : {traceback.format_exc()}")
            
            # BentoML fallback loaded
            try:
                logger.info("🔃 BentoML takes a place")
                model = load_bentoml_model(settings.bentoml_model)
                model_type = "BentoML"
                logger.info("✅ BentoML fallback succeeded")
            except Exception as bentoml_error:
                logger.critical(f"❌ BentoML failed : {str(bentoml_error)}")
                logger.debug(f"🟢 Complete traceback : {traceback.format_exc()}")
                raise RuntimeError(f"All models loaded failed : {e} / {bentoml_error}")