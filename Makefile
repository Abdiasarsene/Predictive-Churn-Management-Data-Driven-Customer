.PHONY: mlflow train format bentoml cyclo code api

# Dossier du test
TEST_DIR = test
TRAINER_DIR = trainer
API_DIR = api

# Defaut Pipeline
default: format cyclo code mypy
	@echo "Default Pipeline Done"

# MLflow Server
mlflow:
	@echo "Lancement du serveur MLflow"
	@mlflow ui

# Pipeline Complet d'entraînement
train:
	@echo "Lancement du Pipeline Global"
	@python runner.py

# Linting + Formatage
format:
	@echo "Linting + Format"
	@ruff check . --fix

# Affichage des modèles sur BentoML
bentoml:
	@echo "Modèles packagés via BentoML"
	@python -m bentoml models list

# Cyclomatic Analysis
cyclo:
	@echo CC Analysis
	@radon mi $(TRAINER_DIR)/ $(API_DIR)/ -s

# Code Analysis
code:
	@echo "Code Analysis"
	@bandit -r $(TRAINER_DIR)/ $(API_DIR)/ -ll

# Run API
api:
	@echo "API Launched"
	@uvicorn main:app --host 127.0.0.1 --port 8000 --reload

# Mypy
mypy:
	@echo "Mypy's running"
	@mypy --config mypy.ini

# Test schema for API 
schema:
	@echo "Test schema"
	@python $(TEST_DIR)/schema_test.py

# Test request for API 
request:
	@echo "Test request"
	@python $(TEST_DIR)/request_test.py