
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # MinIO
    minio_bucket: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str
    
    # API
    api_title: str
    api_description: str
    api_version: str
    
    # Tracking urls
    mlflow_s3_endpoint: str
    mlflow_s3_endpoint_uri: str
    mlflow_artifacts_uri: str
    tracking_uri:str
    
    # Others
    mapping: str
    experiment_name: str
    joblib_filename: str
    run_name: str
    
    model_config = SettingsConfigDict(
        env_file= ".env",
        env_file_encoding= "utf-8"
    )

settings = Settings()