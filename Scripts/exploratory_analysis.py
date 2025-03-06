# Importing librairies
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Importinf of dataset after preprocessing
data_treated = pd.read_csv(r'D:\Projects\IT\Data Science & IA\Customer_segmentation_for_a_Marketing_Campaign\Data\customer.csv')

# Eploratory Data Analysis
statistic = data_treated.describe()

# Data visualization
sns.pairplot(data_treated)
plt.show()

# Heatmap visualization
data_correlation = data_treated.corr()
sns.heatmap(data_correlation, annot=True, cmap="coolwarm")
plt.show()

# Principal Components Analysis
pca = PCA(n_components=0.98)
pca_data = pd.DataFrame(pca.fit_transform(data_treated))
pca_data

# PCA Data Visualization
sns.pairplot(pca_data)
plt.show()

#Initialize n_cluster
inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(pca_data)
    inertias.append(kmeans.inertia_)

# Graphical visualization
plt.plot(range(1,11), inertias, marker='o')
plt.title("Elbow Method")
plt.xlabel('Number of cluster')
plt.ylabel('Inertia')
plt.show()

# Apply of KMeans method
kmeans = KMeans(n_clusters=2, random_state=0)
labels = kmeans.fit_predict(pca_data)
pca_data['Clusters'] = labels

# Data viz
sns.set(style='whitegrid',palette='viridis')
plt.figure(figsize=(12,5))
sns.scatterplot(data=pca_data, x='Annual_Income', y='Spending_Score', hue='Clusters', s=100)

# Centroids
centroids = kmeans.cluster_centers_
plt.scatter(
    centroids[:, pca_data.columns.get_loc('Annual_Income')],
    centroids[:,pca_data.columns.get_loc('Spending_Score')],
    s=300, c='red',marker='X',label='Centroids'
)

plt.title('Visualizing cluters with KMeans')
plt.xlabel('Target')
plt.ylabel('Predictors')
plt.legend5
plt.show()