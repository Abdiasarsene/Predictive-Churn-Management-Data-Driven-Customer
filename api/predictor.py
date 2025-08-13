# Modules Required Imported
import logging
import traceback
import pandas as pd
from fastapi import HTTPException
from .monitor import increment_inference_count

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== MAPPING CLASS ======
churn_mapping = {
    0 : "No",
    1 : "Yes"
}

# ====== MESSAGE OUTPUT BEFORE PREDICTION  ====
def format_message(predicted_class: int) -> str:
    label = churn_mapping.get(predicted_class, "Unknown")
    base_question = "Is the client going to churn? 😨"

    if label == "Yes":
        response = "Yeah 🥶 - Looks like this client might churn. Time to re-engage!"
    elif label == "No":
        response = "Nope 🥹 - The client seems loyal. Keep up the good work!"
    else:
        response = "Unknown 😩 - Prediction unclear. Please check the input or model output."

    return f"{base_question}\n{response}"


# ====== PREDICTION FUNCTION ======
def make_prediction(model, model_type: str, input_dict: dict) -> tuple:
    try: 
        # Create Data Input
        df = pd.DataFrame([input_dict])
        
        # Do prediction based on model type
        if model_type in ["MLflow", "BentoML"]:
            prediction = model.predict(df)
            predicted_class = int(prediction[0])
            
            # Prediction output as a Message
            message = format_message(predicted_class)
            increment_inference_count()
            return predicted_class, message
    
    except Exception as e: 
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.debug(f"🟢 Complete Traceback : {traceback.format_exc()}")
        raise HTTPException(status_code=500, details="Uninitialized Model")