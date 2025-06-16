# Dossier du test
TEST_DIR = test

# MLflow Server
mlflow_server :
	@echo "Lancement du serveur MLflow"
	@mlflow ui

# Pipeline Complet d'entraînement
train :
	@echo "Lancement du Pipeline Global"
	@py models.py

# Linting + Formatage
format : 
	@echo "Linting + Format"
	@ruff check . --fix

# Affichage des modèles sur BentoML
bentoml :
	@echo "Modèles packagés via BentoML"
	@py -m bentoml models list