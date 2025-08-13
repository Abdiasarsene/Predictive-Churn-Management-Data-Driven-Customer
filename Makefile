# Dossier du test
TEST_DIR = test

# MLflow Server
mlflow_server :
	@echo "Lancement du serveur MLflow"
	@mlflow ui

# Pipeline Complet d'entraînement
train :
	@echo "Lancement du Pipeline Global"
	@py runner.py

# Linting + Formatage
format : 
	@echo "Linting + Format"
	@ruff check . --fix

# Affichage des modèles sur BentoML
bentoml :
	@echo "Modèles packagés via BentoML"
	@py -m bentoml models list

# Cyclomatic Analysis
cyclo:
	@echo CC Analysis
	@radon mi trainer/ -s

# Code Analysis
code:
	@echo "Code Analysis"
	@bandit -r trainer/ -ll

# Run API
	runapi:
	@echo "API Launched"
	@uvicorn main:app --host 0.0.0.0 --port 8000 --reload