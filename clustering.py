# Importing librairies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer 
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# ====== IMPORTING DATASET ======
customer = pd.read_csv(r"../data/customer_segmentation.csv")
print("Dataset Impoted ✅✅")

# ====== DETECTION OF DATA TYPES ======
num_col = customer.select_dtypes(include=['int64','float64']).columns.tolist()
cat_col = customer.select_dtypes(include=['object']).columns.tolist()

# ====== PIPELINE ======
# Categoricals columns
cat_transformers = Pipeline([
    ("imputer",SimpleImputer(strategy='constant', fill_value="Missing")),
    ("oneencoder",OneHotEncoder(sparse_output=False, handle_unknown="ignore"))
])

# Numericals columns
num_transformers = Pipeline([
    ("impute", KNNImputer(n_neighbors=3)),
    ("scaler", StandardScaler())
])

# Preprocessing
preprocessors = ColumnTransformer(
    transformers=[
        ("cat", cat_transformers, cat_col),
        ('num', num_transformers,num_col)
    ]
)

# ====== PRINCIPAL COMPONENTS ANALYSIS ======
pipeline = Pipeline([
    ("preprocess", preprocessors),
    ("pca", PCA(n_components=10))
])

# ====== DATA TRANSFORMING ======
data_transformed = pipeline.fit_transform(customer)
print("PCA Passed ✅✅")

# ====== ELBOW METHOD ======
inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit_predict(data_transformed)
    inertias.append(kmeans.inertia_)

# Visualization
plt.plot(range(1,11), inertias, marker='o')
plt.title("Elbow Method")
plt.xlabel('Number of Cluster')
plt.ylabel("Inertias")
plt.show()

# ====== SILHOUETTE COEFFICIENT METHOD ======
silhouette_scores = []
for k in range(2,11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit(data_transformed)
    score = silhouette_score(data_transformed,labels)
    silhouette_scores.append(score)

# Visualization
plt.figure(figsize=(8,5))
plt.plot(range(2,11), silhouette_scores, marker='o', linestyle="--")
plt.title("Silhouette coefficient Method")
plt.xlabel( "Number of Clusters")
plt.ylabel("Silhouette score")
plt.show()

# ====== APPLYING KMEANS ======
optimal_k = 3
kmean = KMeans(n_clusters=3, random_state=42)
clusters = kmean.fit_predict(data_transformed)
customer["Clusters"] = clusters
print("KMeans Applied ✅✅")

# Centroids
pca = PCA(n_components=2)
data_pca = pca.fit_transform(data_transformed)
centroids =pca.transform(kmean.cluster_centers_)
print("PCA Applied for visualizing Centroids ✅✅")

# Visualization
plt.figure(figsize=(8,6))
colors = ["red","purple","green"]

for i in range(optimal_k):
    plt.scatter(
        data_pca[clusters == i, 0], 
        data_pca[clusters == i, 1],
        label = f"Clusters {i}", 
        alpha=0.6, 
        colors =colors[i]
    )

plt.scatter(centroids[:, 0], centroids[:,1], marker="X", s=200, c="black", label ="Centroids")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.title(f"Visualizing KMeans Clusters (k={optimal_k})")
plt.legend()
plt.show()

# ====== AVERAGE ANALYSIS ======
cluster_summary = customer.groupby("Clusters")[num_col].mean()

# ====== MOST FREQUENT CATEGORY BY CLUSTER ======
for col in cat_col :
    model_per_cluster = customer.groupby("Clusters")[cat_col].agg(lambda x: x.mode()[0])
    print(f"\n Most Frequent categor {col} by Clusters : \n {model_per_cluster}")

# ====== CLUSTERS PROPORTION BY CATEGORIES ======
# Categroy : Used Discount
cluster_proportion_used_discount = customer.groupby("Clusters")["Used_Discount"].value_counts(normalize=True)

# Category :  Preferred Category
cluster_percentage_preferred_category = customer.groupby("Clusters")["Preferred_Category"].value_counts(normalize=True)