# app/monitors/model/model_metrics.py
from prometheus_client import Gauge, Counter, Histogram

# Model loading status
model_load_status = Gauge("ml_model_loaded", "1=loaded, 0=failed", ["model_type"])

# Predictions
prediction_count = Counter("ml_predictions_total", "Total predictions", ["model_type", "status"])
prediction_duration = Histogram("ml_prediction_duration_seconds", "Prediction duration", ["model_type"])

# Drift custom (optionnel)
model_drift_detected = Gauge("ml_model_drift", "Drift detected 1=yes,0=no", ["model_type"])