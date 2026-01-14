# server_layer/events/mlflow_model_loader.py
import os
import mlflow
import logging
from api.utils.config import settings

# ====== LOGGING ======
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MLflowModelLoader:
    def __init__(self, experiment_name: str):
        os.environ["MLFLOW_S3_ENDPOINT_URL"] = settings.mlflow_s3_endpoint_uri
        os.environ["AWS_ACCESS_KEY_ID"] = settings.minio_access_key
        os.environ["AWS_SECRET_ACCESS_KEY"] = settings.minio_secret_key

        mlflow.set_tracking_uri(settings.tracking_uri)
        self.experiment = mlflow.get_experiment_by_name(experiment_name)

        if not self.experiment:
            raise ValueError(f"Experiment '{experiment_name}' not found")

        self.experiment_id = self.experiment.experiment_id
        logger.info(f"MLflow connected (experiment={experiment_name})")

    def get_model_uri_by_name(self, model_run_name: str, artifact_path="model") -> str:
        runs_df = mlflow.search_runs(experiment_ids=[self.experiment_id])
        matches = runs_df[runs_df["tags.mlflow.runName"] == model_run_name]

        if matches.empty:
            raise ValueError(f"No run named '{model_run_name}'")

        matches = matches.sort_values("start_time", ascending=False)
        run_id = matches.iloc[0].run_id

        return f"runs:/{run_id}/{artifact_path}"

    def load_model_by_name(self, model_run_name: str):
        model_uri = self.get_model_uri_by_name(model_run_name)
        model = mlflow.pyfunc.load_model(model_uri)
        logger.info(f"Model loaded from {model_uri}")
        return model