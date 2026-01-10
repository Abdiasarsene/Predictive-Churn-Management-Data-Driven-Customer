import time
import pandas as pd
import logging
from fastapi import HTTPException
from api.monitors.model.model_metrics import prediction_count, prediction_duration
from api.logs.efk_logger import log_event  # si tu veux centraliser le logging

# ====== LOGGER ======
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
def make_prediction(model, model_type: str, input_dict: dict) -> int:
    start_time = time.time()
    model_type_lower = (model_type or "unknown").lower()

    try:
        log_event("info", f"🔮 Making prediction with {model_type_lower} model")

        df = pd.DataFrame([input_dict])

        # 👉 Tous les modèles sklearn-like
        if model_type_lower in ["mlflow", "bentoml", "joblib"]:
            prediction = model.predict(df)
            predicted_class = int(prediction[0])

            duration = time.time() - start_time
            prediction_duration.labels(model_type=model_type_lower).observe(duration)
            prediction_count.labels(model_type=model_type_lower, status="success").inc()

            log_event(
                "info",
                f"✅ Prediction successful: {predicted_class} in {duration:.3f}s"
            )
            return predicted_class

        raise ValueError(f"Unsupported model type: {model_type_lower}")

    except Exception as e:
        duration = time.time() - start_time
        prediction_count.labels(model_type=model_type_lower, status="error").inc()

        log_event(
            "error",
            f"❌ Prediction failed after {duration:.3f}s",
            error=str(e)
        )

        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")