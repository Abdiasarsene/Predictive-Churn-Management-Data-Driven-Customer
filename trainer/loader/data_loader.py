# Modules Required
import logging
import traceback
import pandas as pd
from trainer.config import settings
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# ====== LOGGING ======
logger = logging.getLogger()

# ====== LOADING + ENCODAGE + SPLIT ======
def load_and_split():
    try:
        # Dataset Loading
        churn = pd.read_excel(settings.train_dataset)
        logger.info('✅ Imported data done')
        
        # Features + Label
        x = churn.drop(columns=settings.target)
        y = LabelEncoder().fit_transform(churn[settings.target])
        
        # Split train/test
        x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42)
        logger.info("✅ Split done")
        return x_train, x_test, y_train, y_test, churn
    except Exception as e : 
        logger.error(f"❌ Error Detected : {e}")
        logger.debug(f"Traceback : {traceback.format_exc()}")
