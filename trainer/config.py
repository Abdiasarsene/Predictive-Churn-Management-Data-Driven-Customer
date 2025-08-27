# Modules Required
import os
from dotenv import load_dotenv

# ====== LOGGING ======
load_dotenv()

# ====== SETTING ======
class Setting():
    def __init__(self):
        self.train_dataset = os.getenv('TRAIN_DATASET', "")
        self.mlflow_server = os.getenv('MLFLOW_SERVER', "")
        self.mlflow_experiment = os.getenv('MLFLOW_EXPERIMENT', "")
        self.target = "Churn"

settings = Setting()