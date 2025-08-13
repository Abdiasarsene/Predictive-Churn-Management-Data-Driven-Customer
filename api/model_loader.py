# Modules Required Imported
import bentoml
import logging
import mlflow
import traceback
from .config import settings

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== MLFLOW MODEL LOADER ======
def load_mlflow_model(path):
    try: 
        # Initialization with mlflow tracking uri
        mlflow.set_tracking_uri(settings.tracking_uri)
        logger.info(f"Tracking Used : {settings.tracking_uri}")
        
        # MLflow loaded
        model = mlflow.pyfunc.load_model(path)
        if model is None: 
            raise RuntimeError("⚠️ MLflow failed")
        logger.info("Model Loaded Successfully")
        return model
    
    except Exception as e: 
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.debug(f"Complete Traceback : {traceback.format_exc()}")
        raise RuntimeError("⚠️ MLflow failed") from e

# ====== BENTOML MODEL LOADER ======
def load_bentoml_model(tag):
    try: 
        # BentoML loaded
        logger.info("🔃 BentoML's starting loading")
        model = bentoml.sklearn.load_model(tag)
        if model is None: 
            raise RuntimeError("⚠️ BentoML fallback failed")
        return model
    
    except Exception as e: 
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.debug(f"🟢 Complete tracebakc : {traceback.format_exc()}")
        raise RuntimeError("⚠️ BentoML failed ") from e