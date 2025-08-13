# Modules Required
import time
import mlflow
import logging
import traceback
from trainer.config import settings
from trainer.data_loader import load_and_split
from trainer.preprocessing import get_preprocessing
from trainer.training import train_models
from trainer.predEvalSave import evaluate_and_predict
from trainer.monitor import (
    log_data_info,
    log_preprocess_info,
    log_train_info, 
    log_backup_info
)
# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== GLOBAL RUN ======
def main():
    try:
        # MLflow Initialization
        mlflow.set_tracking_uri(settings.mlflow_server)
        mlflow.set_experiment(settings.mlflow_experiment)
        logger.info("✅ Initialization done")
        
        with mlflow.start_run(run_name="ChurnPredictive"):
            # Load and Split
            x_train, x_test, y_train, y_test, churn= load_and_split()
            log_data_info(churn)
            
            # Preprocessing
            preprocessor = get_preprocessing(churn)
            num_cols = churn.select_dtypes(include=['int32',"int64","float64"]).columns.tolist()
            cat_cols = churn.select_dtypes(include=['object']).columns.tolist()
            log_preprocess_info(num_cols, cat_cols)
            
            # Models Training
            start_time = time.time()
            trained_pipeline = train_models(x_train, y_train, preprocessor)
            duration = time.time() - start_time
            for model_name in trained_pipeline:
                log_train_info(model_name, duration)
            
            # Prédiction + Evaluation + Sauvegarde du modèle
            evaluation_results = evaluate_and_predict(trained_pipeline,x_test, y_test)
            log_backup_info(evaluation_results)
            logger.info("🏆 All Pipeline done")
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.debug(f"Traceback : {traceback.format_exc()}")
        raise e

if __name__ == "__main__":
    main()