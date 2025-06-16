# Importation des libraires nécessaires
import logging
import pandas as pd
from train_pipeline.config import settings
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# ====== LOGGING ======
logger = logging.getLogger()

# ====== CHARGEMENT + ENCODAGE + SPLIT ======
def load_and_encode():
    try:
        # Chargement du jeu de données
        churn = pd.read_excel(settings.train_dataset)
        logger.info('✅✅ Jeu de données importé')
        
        # Séparation des features du label
        x = churn.drop(columns=["Churn"])
        y = LabelEncoder().fit_transform(churn["Churn"])
        
        # Split train/test
        x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42)
        logger.info("✅✅ Split réussi")
    except Exception as e : 
        logger.error(f"❌❌ Erreur de chargement et d'encodage : {e}")
    return x_train, x_test, y_train, y_test, churn
