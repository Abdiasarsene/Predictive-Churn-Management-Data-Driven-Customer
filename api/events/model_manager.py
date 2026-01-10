# server_layer/events/model_manager.py
from api.models_loaders.mlflow_model_loader import MLflowModelLoader
from api.models_loaders.models_loader import load_bentoml_model, load_joblib_model
from api.utils.config import settings
from api.logs.efk_logger import log_event
from api.monitors.model.model_metrics import model_load_status
from api.connectors.minio_connection_checker import MinIOConnectionChecker

class ModelManager:
    def __init__(self):
        self.model = None
        self.model_type = None
        self.minio_checker = MinIOConnectionChecker()
        for mt in ["mlflow", "bentoml", "joblib"]:
            model_load_status.labels(model_type=mt).set(0) 

    def validate_connection(self):
        if not self.minio_checker.check_connection():
            log_event("critical", "MinIO connection failed")
            raise RuntimeError("Cannot connect to MinIO. Aborting model loading.")

    def load_model(self):
        # Valide la connexion MinIO avant tout
        self.validate_connection()

        # Fallback MLflow -> BentoML -> Joblib
        try:
            loader = MLflowModelLoader(settings.experiment_name)
            self.model = loader.load_model_by_name(settings.run_name)
            self.model_type = "mlflow"
            model_load_status.labels(model_type=self.model_type).set(1)
        except Exception as e_mlflow:
            log_event("warning", "MLflow load failed", error=str(e_mlflow))
            try:
                self.model = load_bentoml_model(settings.bentoml_model)
                self.model_type = "bentoml"
                model_load_status.labels(model_type=self.model_type).set(1)
            except Exception as e_bento:
                log_event("warning", "BentoML load failed", error=str(e_bento))
                try:
                    self.model = load_joblib_model(settings.joblib_filename)
                    self.model_type = "joblib"
                    model_load_status.labels(model_type=self.model_type).set(1)
                except Exception as e_joblib:
                    log_event(
                        "critical",
                        "All model loading failed",
                        mlflow_error=str(e_mlflow),
                        bentoml_error=str(e_bento),
                        joblib_error=str(e_joblib)
                    )
                    raise RuntimeError("All model loading failed")

        # Mettre à jour les métriques
        model_load_status.labels(model_type=self.model_type).set(1)
        log_event("info", f"Model loaded ({self.model_type})")

    def get_model(self):
        return self.model, self.model_type

model_manager = ModelManager()