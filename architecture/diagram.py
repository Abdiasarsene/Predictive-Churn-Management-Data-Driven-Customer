from diagrams import Cluster, Diagram
from diagrams.programming.flowchart import Action
from diagrams.onprem.client import Users
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Github
from diagrams.onprem.container import Docker
from diagrams.onprem.compute import Server
from diagrams.custom import Custom

with Diagram("Predictive Churn Management - System Architecture",
             show=False, direction="LR"):

    # Entrée utilisateur / données
    user = Users("Client / Data Source")

    with Cluster("Training Service"):
        raw_data = Action("Raw Data Ingestion")
        preprocessing = Action("Feature Engineering\n(CatBoostEncoder)")
        training = Action("Model Training")
        mlflow = Custom("MLflow Registry", "./icons/mlflow.png")
        bentoml = Custom("BentoML Fallback", "./icons/bentoml.png")

        raw_data >> preprocessing >> training >> mlflow
        training >> bentoml

    with Cluster("API & Serving"):
        api = Server("FastAPI API")
        inference = Action("Inference Logic")

        [mlflow, bentoml] >> inference >> api

    with Cluster("Monitoring"):
        prometheus = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
        api >> prometheus >> grafana

    with Cluster("CI/CD Pipeline"):
        github = Github("GitHub")
        jenkins = Jenkins("Jenkins")
        docker = Docker("Docker")
        github >> jenkins >> docker >> api

    # Connexions globales
    user >> api
