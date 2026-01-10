# api/schemas/schema.py
from pydantic import BaseModel, Field
from enum import Enum

# ====== CATEGORICALS COLUMNS ======
class Clusters(str, Enum):
    cluster_0 = "Cluster_0"
    cluster_1 = "Cluster_1"
    cluster_2 = "Cluster_2"

class UsedDiscount(str, Enum):
    oui = "Oui"
    non = "Non"

class PreferredCategory(str, Enum):
    fashion = "Fashion"
    health = "Health"
    home = "Home"
    electronic = "Electronic"
    leisure = "Leisure"

# ====== INPUT SCHEMA ======
class ChurnData(BaseModel):
    cluster: Clusters = Field(..., alias="Clusters")
    annual_income: float = Field(..., ge=50000, le=500000, alias="Annual_Income")
    spending_score: int = Field(..., ge=5, le=200, alias="Spending_Score")
    visit_frequence: int = Field(..., ge=0, le=12, alias="Visit_Frequency") 
    average_basket: float = Field(..., ge=10, le=326.45, alias="Average_Basket")
    used_discount: UsedDiscount = Field(..., alias="Used_Discount")
    preferred_category: PreferredCategory = Field(..., alias="Preferred_Category")
    satisfaction_score: int = Field(..., ge=1, le=5, alias="Satisfaction_Score")

    class Config:
        populate_by_name = True