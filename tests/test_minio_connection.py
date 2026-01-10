# tests/test_minio_connection.py
import logging
from minio import Minio
from api.utils.config import Settings

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Charger les settings
settings = Settings()

# Préfixes attendus dans ton bucket
EXPECTED_PREFIXES = [
    "bentoml_storage/",
    "joblib_storage/",
    "mlflow_storage/"
]

def get_minio_client():
    """Crée un client MinIO avec les settings du .env."""
    return Minio(
        settings.mlflow_s3_endpoint,   # localhost:9000 pour le test local
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=False
    )

def check_bucket_exists(client, bucket_name):
    """Vérifie que le bucket existe."""
    if client.bucket_exists(bucket_name):
        logger.info(f"✅ Bucket '{bucket_name}' accessible.")
        return True
    else:
        logger.warning(f"⚠️ Bucket '{bucket_name}' introuvable.")
        return False

def check_prefixes(client, bucket_name):
    """Vérifie que chaque préfixe attendu contient au moins un objet."""
    all_ok = True
    for prefix in EXPECTED_PREFIXES:
        objects = list(client.list_objects(bucket_name, prefix=prefix, recursive=True))
        if objects:
            logger.info(f"✅ Préfixe '{prefix}' contient {len(objects)} objet(s).")
        else:
            logger.warning(f"⚠️ Préfixe '{prefix}' vide ou inexistant.")
            all_ok = False
    return all_ok

def test_minio_connection():
    client = get_minio_client()
    bucket_ok = check_bucket_exists(client, settings.minio_bucket)
    prefixes_ok = check_prefixes(client, settings.minio_bucket) if bucket_ok else False

    if bucket_ok and prefixes_ok:
        logger.info("✅ Connexion MinIO et préfixes OK.")
    else:
        logger.warning("⚠️ Problème avec MinIO ou les préfixes.")

# Exécution directe
if __name__ == "__main__":
    test_minio_connection()