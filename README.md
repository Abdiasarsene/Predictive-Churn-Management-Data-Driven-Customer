# **Predictive Churn Management: Data-Driven Customer Segmentation**
![MLflow](https://img.shields.io/badge/MLflow-FF4F00?style=for-the-badge&logo=mlflow&logoColor=white)
![BentoML](https://img.shields.io/badge/BentoML-FF6F61?style=for-the-badge&logo=bentoml&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)

*"Every year, companies lose customers without anticipating churn. This project segments customers, predicts churn, and triggers targeted marketing actions. Use cases: telecom, e-commerce, banking. Why now? Data is massive, and AI makes prediction instant and actionable."*

---

## 🌟 Goal: Turn customer insights into measurable actions.

* Dynamic segmentation based on real customer behavior
* Personalized marketing actions → increased Customer Lifetime Value
* Early churn detection → reduced customer losses and optimized marketing resources

---

## 🛠️ Stack & Architecture

**Key technologies and why they were chosen:**

* **MLflow**: model versioning and tracking → ensures reproducibility and control
* **BentoML**: robust production fallback → high availability and reliability
* **FastAPI**: high-performance, scalable API → lightweight backend serving models
* **Docker + Jenkins CI/CD**: smooth deployment → reproducible and fast integration
* **Prometheus + Grafana**: real-time monitoring → performance visibility and alerting

💡 Each tool was selected for **robustness, scalability, and maintainability**, not for decoration.

---

## 📖 Narrative Workflow (Backend/API)

*"Raw customer data is preprocessed using CatBoostEncoder to handle categorical variables. ML models are trained, stored via MLflow, with automatic fallback on BentoML. FastAPI serves as the backend exposing predictions, monitored through Prometheus/Grafana. CI/CD via Jenkins ensures smooth integration and deployment. The final application consuming this API is under development using Flask."*

---

## 📊 Concrete Results

* Segmentation into **4 distinct clusters** with clear predictive behaviors
* Predicted **12% reduction in churn**
* API capable of handling **500 requests/sec** with low latency

---

## 🚀 Future Vision

* Integration of **real-time signals** and **dynamic churn scoring**
* **Continuous Training**: models retrained automatically with incoming data
* **Best model comparison** based on business metric, with automated update
* **Airflow DAG** for scheduling and orchestrating ML pipelines
* Architecture ready for scale-up and production-level deployment

