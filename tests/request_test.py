import requests

url ="http://localhost:8000/v1/predict"
data = {
    "Clusters": "Cluster_0",
    "Annual_income": 50000,
    "Spending_Score": 200,
    "Visit_Frequence": 12,
    "Average_Basket": 326.45,
    "Used_Discount": "Oui",
    "Preferred_Category": "Fashion",
    "Satisfaction_Score": 5
}

res = requests.post(url, json=data, timeout=10)
print(res.json())