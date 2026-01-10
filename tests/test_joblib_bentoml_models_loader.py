# tests/test_models_loader.py
import logging
from connectors.minio_connection_checker import MinIOConnectionChecker
from api.models_loaders.models_loader import load_joblib_model, load_bentoml_model

logging.basicConfig(level=logging.INFO)

def test_model_loaders():
    """
    Test complet :
    - Vérifie la connexion MinIO
    - Tente de charger un modèle Joblib
    - Tente de charger un modèle BentoML
    """
    checker = MinIOConnectionChecker()
    assert checker.check_connection(), "❌ MinIO connection failed"

    # === JOBLIB MODEL ===
    joblib_filename = "random_forest.pkl"  # à adapter à ton cas réel
    joblib_model = load_joblib_model(joblib_filename)
    assert joblib_model is not None, "❌ Joblib model failed to load"

    # === BENTOML MODEL ===
    bentoml_model = load_bentoml_model("random_forest")
    assert bentoml_model is not None, "❌ BentoML model failed to load"


    print("✅ All models successfully loaded via MinIO!")

if __name__ == "__main__":
    test_model_loaders()