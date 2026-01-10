import pandas as pd
from api.logs.efk_logger import log_event

def normalize_input(payload):
    try:
        # 1️⃣ Déjà un DataFrame
        if isinstance(payload, pd.DataFrame):
            return payload.reset_index(drop=True)

        # 2️⃣ Liste de dictionnaires
        if isinstance(payload, list) and all(isinstance(x, dict) for x in payload):
            return pd.DataFrame(payload)

        # 3️⃣ Dictionnaire (cas principal)
        if isinstance(payload, dict):
            clean = {}

            for k, v in payload.items():
                if isinstance(v, pd.Series):
                    clean[k] = v.iloc[0]
                else:
                    clean[k] = v

            return pd.DataFrame([clean])

        raise TypeError("Unsupported payload type")

    except Exception as e:
        log_event(
            "error",
            "Input Data Failed",
            error=str(e),
            payload_type=type(payload).__name__,
            payload_sample=str(payload)[:200]
        )
        raise