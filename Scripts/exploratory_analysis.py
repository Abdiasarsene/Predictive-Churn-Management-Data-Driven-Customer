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