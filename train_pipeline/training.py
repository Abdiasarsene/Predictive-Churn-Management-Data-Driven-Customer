# Importation des bibliothèques importantes
import logging
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# ====== FONCTION D'ENTRAINMENT DES MODELES ======
def train_models(x_train, y_train, preprocessor):
    # Définition des modèles à appliquer
    models = {
    "logistic": LogisticRegression(
        max_iter=1000,
        solver="liblinear",
        class_weight="balanced"
    ),

    "random_forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        class_weight="balanced",
        min_samples_split=10,
        min_samples_leaf=4
    ),

    "xgboost": XGBClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=1, 
        random_state=42,
        use_label_encoder=False,
        eval_metric="logloss",
        check_input=False
    ),

    "tree_decision": DecisionTreeClassifier(
        max_depth=5,
        min_samples_split=10,
        min_samples_leaf=4,
        class_weight="balanced",
        random_state=42
    )
    }

    
    # Création de dictionnaires pour le stockage des modèles entraînés
    trained_pipeline = {}
    
    # Création de la boucle d'entraînement
    for name, model in models.items():
        try: 
            print(f"🚀🚀 Entraînement du modèle : {name}")
            
            model_pipeline = Pipeline([
                ('preprocessing', preprocessor),
                ('models', model)
            ])
            
            # Application et sauvegarde des modèles
            model_pipeline.fit(x_train, y_train)
            trained_pipeline[name] = model_pipeline
            logger.info(f"✅✅Modèle {name} entraîné")
            print(type(trained_pipeline))

        except Exception as e: 
            logger.error(f"Erreur lors de l'entraînement du modèle {name} : {e}")
    logger.info("Tous les modèles ont été entraînés ✅✅")
    return trained_pipeline