# server_layer/events/mlflow_model_loader.py
import os
import mlflow
import logging
from api.utils.config import settings

# ====== LOGGING ======
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MLflowModelLoader:
    """
    Classe pour charger un modèle MLflow depuis un bucket MinIO déjà validé.
    La connexion MinIO doit avoir été validée par MinIOConnectionChecker.
    """

    def __init__(self, experiment_name: str):
        # === Configuration MinIO pour MLflow ===
        # endpoint = (
        #     settings.mlflow_s3_endpoint_uri
        #     if settings.mlflow_s3_endpoint_uri.startswith("http")
        #     else f"http://{settings.mlflow_s3_endpoint_uri}"
        # )

        os.environ["MLFLOW_S3_ENDPOINT_URL"] =settings.mlflow_s3_endpoint_uri
        os.environ["AWS_ACCESS_KEY_ID"] = settings.minio_access_key
        os.environ["AWS_SECRET_ACCESS_KEY"] = settings.minio_secret_key

        # === Connexion MLflow ===
        mlflow.set_tracking_uri(settings.tracking_uri)
        self.experiment = mlflow.get_experiment_by_name(experiment_name)

        if not self.experiment:
            raise ValueError(f"❌ Experiment '{experiment_name}' not found in MLflow.")

        self.experiment_id = self.experiment.experiment_id
        logger.info(f"✅ MLflow connected (experiment: {experiment_name})")

    def get_model_uri_by_name(self, model_run_name: str, artifact_path: str = "model") -> str:
        """Retourne l'URI MLflow pour un run donné."""
        try:
            runs_df = mlflow.search_runs(experiment_ids=[self.experiment_id])
            matches = runs_df[runs_df["tags.mlflow.runName"] == model_run_name]

            if matches.empty:
                raise ValueError(
                    f"No model found with run name '{model_run_name}' "
                    f"in experiment '{self.experiment.name}'."
                )

            # Prend le run le plus récent si plusieurs
            run_id = matches.iloc[0].run_id
            model_uri = f"runs:/{run_id}/{artifact_path}"
            logger.info(f"✅ Model '{model_run_name}' found — URI: {model_uri}")
            return model_uri

        except Exception as e:
            logger.error(f"❌ Error searching model '{model_run_name}': {str(e)}", exc_info=True)
            return None

    def load_model_by_name(self, model_run_name: str):
        """Charge le modèle depuis MLflow et retourne l'objet Python."""
        try:
            model_uri = self.get_model_uri_by_name(model_run_name)
            if not model_uri:
                raise ValueError(f"Unable to resolve model URI for '{model_run_name}'")

            model = mlflow.sklearn.load_model(model_uri)
            logger.info(f"📦 Model '{model_run_name}' successfully loaded from {model_uri}")
            return model

        except Exception as e:
            logger.error(f"❌ Error loading model '{model_run_name}': {str(e)}", exc_info=True)
            return None