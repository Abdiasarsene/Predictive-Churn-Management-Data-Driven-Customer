# Modules Required
import logging
import traceback
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from category_encoders import CatBoostEncoder
from sklearn.preprocessing import RobustScaler
from sklearn.impute import KNNImputer, SimpleImputer

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# ====== PREPROCESSING ======
def get_preprocessing(churn):
    try:
        features = churn.drop(columns=["Churn"])
        
        # Separation of cat & num features
        num_cols = features.select_dtypes(include=['int32',"int64","float64"]).columns.tolist()
        cat_cols = features.select_dtypes(include=['object']).columns.tolist()
        
        # Print columns
        logger.info(f"📊 Numericals features : {num_cols}")
        logger.info(f"📊 Categoricals features : {cat_cols}")
        
        # Pipeline
        num_transformed = Pipeline([
            ('impute', KNNImputer(n_neighbors=3)),
            ('scaler', RobustScaler())
        ])
        
        cat_transformed = Pipeline([
            ('impute', SimpleImputer(strategy='most_frequent')),
            ('encoder', CatBoostEncoder())
        ])
        
        preprocessor = ColumnTransformer([
            ('num', num_transformed, num_cols),
            ('cat', cat_transformed, cat_cols)
        ])
        logger.info("✅ Preprocessing done")
        return preprocessor
    except Exception as e : 
        logger.error(f"❌ Error Detected : {e}")
        logger.debug(f"Traceback : {traceback.format_exc()}")
        raise e
