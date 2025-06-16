# Importation des bibliothèques nécessaires
import logging
from sklearn.impute import KNNImputer, SimpleImputer
from category_encoders import CatBoostEncoder
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# ====== PREPROCESSING ======
def get_preprocessing(churn):
    try:
        features = churn.drop(columns=["Churn"])
        
        # Séparation des features catégorielles et numériques
        num_cols = features.select_dtypes(include=['int32',"int64","float64"]).columns.tolist()
        cat_cols = features.select_dtypes(include=['object']).columns.tolist()
        
        # Affichage des colonnes
        logger.info(f"📊📊 Colonnes numériques : {num_cols}")
        logger.info(f"📊📊 Colonnes catégorielles : {cat_cols}")
        
        # Prétraitement
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
        logger.info("✅✅ Prétraitemnt fini")
        return preprocessor
    except Exception as e : 
        logger.error(f"Erreur lors du prétraitment : {e}")
        raise e
