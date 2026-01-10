from api.schemas.schema import ChurnData

exemple ={
    "Clusters": "Cluster_0",
    "Annual_Income": 50000,
    "Spending_Score": 200,
    "Visit_Frequency": 12,
    "Average_Basket": 326.45,
    "Used_Discount": "Oui",
    "Preferred_Category": "Fashion",
    "Satisfaction_Score": 5
}

try:
    data = ChurnData(**exemple)
    print(f"✅ Validate :\n {data}")
except  Exception as e:
    print(f"❌ Error : {str(e)}")