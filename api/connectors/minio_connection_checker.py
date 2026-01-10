# api/utils/minio_connection_checker.py
import logging
from minio import Minio
from minio.error import S3Error
from api.utils.config import settings

# ====== LOGGING ======
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MinIOConnectionChecker:
    # Préfixes attendus dans le bucket
    EXPECTED_PREFIXES = [
        "bentoml_storage/",
        "joblib_storage/",
        "mlflow_storage/"
    ]

    def __init__(self):
        self.client = Minio(
            settings.mlflow_s3_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=False
        )
        self.bucket_name = settings.minio_bucket

    def check_bucket_exists(self) -> bool:
        """
        Vérifie que le bucket existe sur MinIO.
        """
        try:
            if self.client.bucket_exists(self.bucket_name):
                logger.info(f"✅ Bucket '{self.bucket_name}' accessible.")
                return True
            else:
                logger.warning(f"⚠️ Bucket '{self.bucket_name}' introuvable sur MinIO.")
                return False
        except S3Error as e:
            logger.error(f"❌ Erreur S3: {e}")
            return False
        except Exception as e:
            logger.exception(f"💥 Erreur inattendue lors de la vérification du bucket: {e}")
            return False

    def check_prefixes(self) -> bool:
        """
        Vérifie que chaque préfixe attendu contient au moins un objet.
        """
        all_prefixes_ok = True
        for prefix in self.EXPECTED_PREFIXES:
            try:
                objects = list(self.client.list_objects(self.bucket_name, prefix=prefix, recursive=True))
                if objects:
                    logger.info(f"✅ Préfixe '{prefix}' contient {len(objects)} objet(s).")
                else:
                    logger.warning(f"⚠️ Préfixe '{prefix}' vide ou inexistant.")
                    all_prefixes_ok = False
            except S3Error as e:
                logger.error(f"❌ Erreur S3 lors de la vérification du préfixe '{prefix}': {e}")
                all_prefixes_ok = False
            except Exception as e:
                logger.exception(f"💥 Erreur inattendue lors de la vérification du préfixe '{prefix}': {e}")
                all_prefixes_ok = False
        return all_prefixes_ok

    def check_connection(self) -> bool:
        """
        Vérifie le bucket et les préfixes. Retourne True seulement si tout est OK.
        """
        bucket_ok = self.check_bucket_exists()
        prefixes_ok = self.check_prefixes() if bucket_ok else False
        return bucket_ok and prefixes_ok