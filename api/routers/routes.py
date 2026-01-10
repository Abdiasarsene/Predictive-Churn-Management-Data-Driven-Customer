# api/routers/predict_router.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from api.core.data_transformer import normalize_input
from api.schemas.schema import ChurnData
from api.services.predictor import make_prediction
from api.services.output_message import format_message
from api.events.model_manager import model_manager
from api.connectors.minio_connection_checker import MinIOConnectionChecker
from api.logs.efk_logger import log_event

router = APIRouter()

# ====== PREDICTION ENDPOINT ======
@router.post("/predict")
async def predict_endpoint(payload: ChurnData):
    # 1️⃣ Validation Pydantic explicite
    try:
        validated_data = ChurnData(**payload.dict())
        input_dict = validated_data.dict(by_alias=True)
        log_event("info", "Input data successfully validated", payload_sample=str(input_dict)[:200])
    except Exception as e:
        log_event("error", "Pydantic validation failed", error=str(e))
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")

    # 2️⃣ Transformation
    try:
        normalize_input(input_dict)
        log_event("info", "Input data successfully transformed")
    except Exception as e:
        log_event("error", "Data transformation failed", error=str(e))
        raise HTTPException(status_code=400, detail=f"Data transformation error: {str(e)}")

    # 3️⃣ Récupérer le modèle
    model, model_type = model_manager.get_model()
    if not model:
        log_event("error", "Prediction requested but model not loaded")
        raise HTTPException(status_code=500, detail="Model not loaded")

    # 4️⃣ Prédiction
    try:
        predicted_class = make_prediction(model, model_type, input_dict)
    except Exception as e:
        log_event("error", "Prediction failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

    # 5️⃣ Formatage message
    message = format_message(predicted_class)

    # 6️⃣ Retour JSON
    return JSONResponse(
        content={
            "predicted_class": predicted_class,
            "message": message,
            "model_type": model_type
        }
    )

# ====== HEALTH CHECK ENDPOINT ======
@router.get("/health")
async def health_check():
    # 1️⃣ Vérification modèle
    model, model_type = model_manager.get_model()
    model_status = bool(model)

    # 2️⃣ Vérification MinIO
    try:
        minio_checker = MinIOConnectionChecker()
        minio_ok = minio_checker.check_connection()
    except Exception as e:
        minio_ok = False
        log_event("error", "MinIO health check failed", error=str(e))

    status = "ok" if model_status and minio_ok else "degraded"
    log_event("info", "Health check performed", model_status=model_status, minio_ok=minio_ok)

    return JSONResponse(
        content={
            "status": status,
            "model_loaded": model_status,
            "minio_connection": minio_ok
        }
    )