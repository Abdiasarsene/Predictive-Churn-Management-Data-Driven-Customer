#!/bin/bash
echo "🚀 Déploiement sécurisé du modèle BentoML..."

# 1. Créer le volume si nécessaire
docker volume create bentoml_cache

# 2. Copier le modèle local vers le volume Docker
docker run --rm -v ~/bentoml:/source -v bentoml_cache:/target alpine cp -r /source/models/ /target/

# 3. Lancer les services
docker compose up -d

echo "✅ Modèle déployé sécurisé dans le volume Docker"