# api/services/output_message.py  
import json 
import logging 
from api.utils.config import settings

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== UPLOAD MAPPING ======
with open(settings.mapping, encoding="utf-8") as f:
    mapping = json.load(f)

# ====== MESSAGE OUTPUT BEFORE PREDICTION ====
def format_message(predicted_class: int) -> str:
    label = mapping.get(predicted_class, "Unknown")
    base_question = "Is the client going to churn? 😨"

    if label == "Yes":
        response = "Yeah 🥶 - Looks like this client might churn. Time to re-engage!"
    elif label == "No":
        response = "Nope 🥹 - The client seems loyal. Keep up the good work!"
    else:
        response = "Unknown 😩 - Prediction unclear. Please check the input or model output."

    return f"{base_question} : {response}"