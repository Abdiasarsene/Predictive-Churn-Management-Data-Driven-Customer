# tests/test_models_loaders.py
import os
import sys
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.utils.minio_connection_checker import check_minio_connection
from api.models_loaders.models_loader import load_joblib_model, load_bentoml_model
from models_loaders.mlflow_model_loader import MLflowModelLoader

# ===== Logging setup =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== TEST 1: MinIO connection =====
def test_minio_connection():
    """Check that MinIO connection works."""
    if not check_minio_connection():
        logger.warning("⚠️ MinIO connection failed.")
        assert False, "MinIO connection failed"
    else:
        logger.info("✅ MinIO connection OK.")
        assert True

# ===== TEST 2: Joblib loader =====
def test_joblib_loader():
    """Try loading a Joblib model from MinIO."""
    if not check_minio_connection():
        logger.warning("⚠️ Skipping Joblib test — MinIO not accessible.")
        return
    try:
        model = load_joblib_model("example_model.pkl")
        assert model is not None, "❌ Joblib model returned None"
        logger.info("✅ Joblib model loaded successfully.")
    except Exception as e:
        logger.error(f"❌ Joblib loader error: {e}")
        assert False, str(e)

# ===== TEST 3: BentoML loader =====
def test_bentoml_loader():
    """Try loading a BentoML model from MinIO."""
    if not check_minio_connection():
        logger.warning("⚠️ Skipping BentoML test — MinIO not accessible.")
        return
    try:
        model = load_bentoml_model("bento_example")
        assert model is not None, "❌ BentoML model returned None"
        logger.info("✅ BentoML model loaded successfully.")
    except Exception as e:
        logger.error(f"❌ BentoML loader error: {e}")
        assert False, str(e)

# ===== TEST 4: MLflow loader =====
def test_mlflow_loader():
    """Try loading a model from MLflow."""
    try:
        loader = MLflowModelLoader("Churn-Experiment")
        model = loader.load_model_by_name("churn_best_model")
        assert model is not None, "❌ MLflow model returned None"
        logger.info("✅ MLflow model loaded successfully.")
    except Exception as e:
        logger.error(f"❌ MLflow loader error: {e}")
        assert False, str(e)
