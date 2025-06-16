# Imoortation des bibliothèques nécessaires
from train_pipeline.data_loader import load_and_encode
from train_pipeline.preprocessing import get_preprocessing
from train_pipeline.training import train_models
from train_pipeline.predict_eval import log_and_save_model

# Lancement du pipeline globale
if __name__ == "__main__":
    # Chargement + Encodage
    x_train, x_test, y_train, y_test, churn= load_and_encode()
    
    # Prétraitment 
    preprocessor = get_preprocessing(churn)
    
    # Entrainement des modèles 
    trained_pipeline = train_models(x_train, y_train, preprocessor)
    
    # Prédiction + Evaluation + Sauvegarde du modèle
    log_and_save_model(x_test, y_test, trained_pipeline)
