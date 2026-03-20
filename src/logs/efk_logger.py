# monitoring/logs/efk_logger.py
import logging
from pythonjsonlogger import jsonlogger

# Crée le logger
logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

# Formatter JSON pour Fluentd / EFK
logHandler = logging.FileHandler("logs/api.log")
formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s %(extra)s"
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

# Helper pour logs structurés
def log_event(level, message, **kwargs):
    """
    level: INFO, ERROR, WARNING, etc.
    message: texte
    kwargs: contexte additionnel (request_id, model_type, endpoint, etc.)
    """
    extra = {"extra": kwargs}
    if level == "info":
        logger.info(message, extra=extra)
    elif level == "warning":
        logger.warning(message, extra=extra)
    elif level == "error":
        logger.error(message, extra=extra)
    elif level == "debug":
        logger.debug(message, extra=extra)