# Modules Required
import logging
import traceback
from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# ====== FUNCTION OF MODELS TRAINING ======
def train_models(x_train, y_train, preprocessor):
    try:
        # Models to train
        models = {
            "Logistic": LogisticRegression(
                max_iter=1000,
                solver="liblinear",
                class_weight="balanced"
            ),

            "Random_forest": RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=10,
                class_weight="balanced",
                min_samples_split=10,
                min_samples_leaf=4
            ),

            "Xgboost": XGBClassifier(
                n_estimators=300,
                learning_rate=0.05,
                max_depth=5,
                subsample=0.8,
                colsample_bytree=0.8,
                scale_pos_weight=1, 
                random_state=42,
                use_label_encoder=False,
                eval_metric="logloss",
            ),

            "Tree_decision": DecisionTreeClassifier(
                max_depth=5,
                min_samples_split=10,
                min_samples_leaf=4,
                class_weight="balanced",
                random_state=42
            )
        }

        
        # Dico for storage of models trained
        trained_pipeline = {}
        
        # Loop Training
        for name, model in models.items():
            try: 
                logger.info(f"🚀 Starting Training : {name}")
                
                model_pipeline = Pipeline([
                    ('preprocessing', preprocessor),
                    ('models', model)
                ])
                
                # Training & Back up for models
                model_pipeline.fit(x_train, y_train)
                trained_pipeline[name] = model_pipeline
                logger.info(f"✅ {name} model trained")
                print(type(trained_pipeline))

            except Exception as e: 
                logger.error(f"❌ Error Detected {name} : {e}")
                logger.debug(f"Traceback : {traceback.format_exc()}")
        logger.info("🟢Training models done")
        return trained_pipeline
    except Exception as e: 
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.debug(f"Traceback : {traceback.format_exc()}")
