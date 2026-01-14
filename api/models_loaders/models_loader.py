import s3fs
import joblib
import logging
from api.utils.config import settings

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== COMMON: ensure MinIO endpoint is well formatted ======
def _get_minio_endpoint():
    endpoint = settings.mlflow_s3_endpoint_uri
    return endpoint if endpoint.startswith("http") else f"http://{endpoint}"

# ====== JOBLIB LOADER ======
def load_joblib_model(filename: str, prefix: str = "joblib_storage/"):
    try:
        fs = s3fs.S3FileSystem(
            key=settings.minio_access_key,
            secret=settings.minio_secret_key,
            client_kwargs={"endpoint_url": _get_minio_endpoint()}
        )

        s3_path = f"s3://{settings.minio_bucket}/{prefix}{filename}"
        logger.info(f"📥 Attempting to load Joblib model from: {s3_path}")
        with fs.open(s3_path, "rb") as f:
            model = joblib.load(f)
        logger.info(f"✅ Joblib model successfully loaded from {s3_path}")
        return model

    except FileNotFoundError:
        logger.error(f"❌ File not found on MinIO: {s3_path}")
        return None
    except Exception as e:
        logger.error(f"❌ Error while loading Joblib model: {str(e)}", exc_info=True)
        return None