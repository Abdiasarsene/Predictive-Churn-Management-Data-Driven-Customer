# tests/test_mlflow_model_loader.py
from connectors.minio_connection_checker import MinIOConnectionChecker
from api.models_loaders.mlflow_model_loader import MLflowModelLoader

def test_mlflow_model_loading():
    # 1️⃣ Vérifier la connexion MinIO et les préfixes
    minio_checker = MinIOConnectionChecker()
    connection_ok = minio_checker.check_connection()
    assert connection_ok, "MinIO connection or prefixes check failed"

    # 2️⃣ Charger le modèle MLflow
    experiment_name = "OtherModels_MinIO"
    run_name = "random_forest"

    loader = MLflowModelLoader(experiment_name)
    model = loader.load_model_by_name(run_name)

    assert model is not None, "MLflow model should be loaded successfully"
    print("✅ MinIO connection and MLflow model loading test passed")

if __name__ == "__main__":
    test_mlflow_model_loading()