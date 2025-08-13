# Modules required imported
from fastapi import APIRouter, HTTPException
from .schema import ChurnData
from .predictor import make_prediction
from .events import get_model
import logging
import traceback 
from .monitor import increment_inference_count

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1", redirect_slashes=False)

# ====== ROUTE OF VALIDATION =====
@router.post("/validate")
async def validate_churn_input(data: ChurnData):
    try:
        logger.info("🔎 Validation of Input Data")
        validated_data = data.model_dump(by_alias=True)
        logger.info("🟢 Data Checked")
        return {
            "Validated Data" : validated_data,
            "Message" : "Input Data Matched",
            "Statut" : "Success"
        }
    except Exception as e:
        logger.error(f"❌ Error detected : {str(e)}")
        logger.debug(f"🟢 Traceback complete : {traceback.format_exc()}")
        raise HTTPException(status_code=400, details=f"❌ Validation Error: {str(e)}")

# ====== ROUTE OF PREDICTION =====
@router.post("/predict")
async def predict_churn(data: ChurnData):
    try:
        # Prediction + Print of message
        logger.info("🔃 Starting of prediction")
        model, model_type = get_model()
        input_dict = data.dict(by_alias=True)
        predicted_class, message = make_prediction(model, model_type, input_dict)
        increment_inference_count()
        logger.info("🚀 Prediction done")
        
        # Printing of message
        return {
            "Deliver Status" : message, 
            "Code" : predicted_class, 
            "Statut": "Success",
            "Model Used" : model_type
        }
    except Exception as e:
        logger.eeror(f"❌ Error Detected : {str(e)}")
        logger.debug(f"🟢 Complete traceback : {traceback.format_exc()}")
        raise HTTPException(status_code=5000, detail=f"Error of prediction : {str(e)}")