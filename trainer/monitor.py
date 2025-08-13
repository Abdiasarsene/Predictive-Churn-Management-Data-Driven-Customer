# Modules Required
import logging
import mlflow
import bentoml
import traceback

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== DATA OVERVIEW ======
def log_data_info(churn):
    try:
        mlflow.log_metric("n_row", churn.shape[0])
        mlflow.log_metric("n_columns", churn.shape[1])
        missing_value = churn.isna().sum().sum()
        mlflow.log_metric("missing_value", missing_value)
        logger.info("✅ Data log done")
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.debug(f"Traceback : {traceback.format_exc()}")

# ====== NUM & CAT FEATURES ======
def log_preprocess_info(num_cols, cat_cols):
    try: 
        mlflow.log_metric("n_numeric_cols", len(num_cols))
        mlflow.log_metric("n_categoricals_clos", len(cat_cols))        
        logger.info("✅ Preprocessing log done")
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.debug(f"Traceback : {traceback.format_exc()}")

# ====== TRAINING ======
def log_train_info(model_name, durations_seconds):
    try:
        mlflow.log_param("models", model_name)
        mlflow.log_metric(f"{model_name}_time_duration", durations_seconds)
        logger.info("✅Train log")
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.debug(f"Traceback : {traceback.format_exc()}")

# ====== BACKUP MODELS AND EVBALUATION ======
def log_backup_info(evaluation_result):
    try:
        for model_name, content in evaluation_result.items():
            model = content["model"]
            metrics = content["metrics"]
            
            # === MLflow Back Up == 
            with mlflow.start_run(run_name=f"{model_name}_eval", nested=True):
                # Log Models
                mlflow.log_param("model_type", model_name)
                mlflow.log_params(model.get_params())
                logger.info("✅ Models logged in MLflow")
                
                # Log Metrics
                for metric_name, value in metrics.items():
                    mlflow.log_metric(metric_name, value)
                logger.info("✅ Metrics Always Loogged")
                
                # Backup
                mlflow.sklearn.log_model(model, model_name)
                logger.info("✅ MLflow done")
                
                # Register Model to MLflow Registry
                model_uri = f"run:/{mlflow.active_run().info.run_id}/{model_name}"
                result = mlflow.register_model(model_uri=model_uri, name=model_name)
                
                client = mlflow.tracking.MlflowClient()
                client.transition_model_version_stage(
                    name=model_name,
                    version=result.version,
                    stage="Production",
                    archive_existing_versions=True
                )
                logger.info(f"🚀 {model_name} promoted to Production")
        
            # === BentoML Back Up ===
            bentoml.sklearn.log_model(model, model_name)
            logger.info("✅ BentoML done")
        logger.info("📊 MLflow & BentoML logged")
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.debug(f"Traceback : {traceback.format_exc()}")