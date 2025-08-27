# Modules Required 
import logging 
import traceback
from sklearn.metrics import accuracy_score, recall_score, f1_score

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== EVALUATE METRICS ======
def evaluate_metrics(y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)
    return acc, rec, f1

# ====== EVALUATE + PREDICT ======
def evaluate_and_predict(trained_pipeline, x_test, y_test):
    try:
        # Dico to save metrics and model
        result = {}
        
        # Loop
        for name, model in trained_pipeline.items():
            # Predict
            y_pred = model.predict(x_test)
            logger.info('🚀 Prediction done')
            
            # Evaluate
            acc, rec, f1 = evaluate_metrics(y_test, y_pred)
            logger.info("🚀 Evaluation done")
            
            # Save
            result[name] = {
                "model": model,
                "metrics":{
                    "accuracy":acc,
                    "recall": rec, 
                    "f1_score":f1
                }
            }
        logger.info("✅ Predict + Evaluate done")
        return result
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.debug(f"Traceback : {traceback.format_exc()}")
        raise e
