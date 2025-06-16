# Importation des bibliothèques importantes
import logging
import mlflow
import bentoml
from train_pipeline.config import settings
from sklearn.metrics import accuracy_score, recall_score, f1_score

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# ====== PREDICTION + METRIQUE + SAUVEGARDE DES MODELES ======
def log_and_save_model(x_test, y_test,  trained_pipeline):
    # MLflow Expérience + Tracking  URI
    mlflow.set_tracking_uri(settings.mlflow_server)
    mlflow.set_experiment(settings.mlflow_experiment)
    
    for model_name, model in trained_pipeline.items():
        try:
            # Prédiction et calcul des métriques
            y_pred = model.predict(x_test)
            acc = accuracy_score(y_test, y_pred)
            rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_pred, y_test, average="weighted", zero_division=0)
            
            with mlflow.start_run( run_name=model_name):
                # Log paramètre et métriques
                mlflow.log_param('model_type', model.get_params())
                mlflow.log_metric("accuracy", acc)
                mlflow.log_metric("recall", rec)
                mlflow.log_metric("f1_score",f1)
                
                # Enrégistement du modèle
                mlflow.sklearn.log_model(model, model_name)
                logger.info(f"✅✅ Modèle {model_name} enregistré avec MLflow")
                
                # Enrégistrement du modèle dans le Modèle Registry 
                model_uri = f"run:/{mlflow.active_run().info.run_id}/{model_name}"
                result = mlflow.register_model(model_uri=model_uri, name=model_name)

                client = mlflow.tracking.MlflowClient()
                client.transition_model_version_stage(
                    name=model_name,
                    version=result.version,
                    stage="Production", 
                    archive_existing_versions=True
                )
                logger.info(f"🎯 {model_name} promu en Production dans le Model Registry")
                
                
            # Enregistrement avec BentoML
            bentoml.sklearn.save_model(model_name, model)
            logger.info(f"✅✅ Modèle {model_name} sauvegardé dans BentoML")
            
        except Exception as e:
            logger.error(f"⚠️ Erreur  lors de l'enregistrement du modèle {model_name} : {e}")