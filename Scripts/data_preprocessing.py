# Importing librairies
import numpy as np
import pandas as pd
import missingno as msno
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.impute import KNNImputer

# Importing dataset
customer = pd.read_csv(r"D:\Projects\IT\Data Science & IA\Customer_segmentation_for_a_Marketing_Campaign\Data\customer_segmentation.csv")

# Overview of dataset
customer #Print head and tail of the dataset
customer.info() #Print more information about the columns

# Data Preprocessing

# Transform categorical into numerics
label_encoder = LabelEncoder()
customer['Pref_Category_Num'] = label_encoder.fit_transform(customer['Preferred_Category'])

# Reconfiguring of the new dataset
    # Define columns of my DataFrame
columns = ['Age', 'Annual_Income', 'Spending_Score', 'Visit_Frequency','Average_Basket', 'Used_Discount', 'Preferred_Category','Satisfaction_Score', 'Pref_Category_Num']
    # Apply the columns of my ndarray
customer_data = pd.DataFrame(customer, columns=customer.columns)
    # Remove an object column into the dataset
customer = customer_data.select_dtypes(exclude=['object'])

msno.bar(customer, color='green') #Print more information about the missing values

# Handling missing values using the KNN method
knn = KNNImputer(n_neighbors=3)
customer = pd.DataFrame(data=knn.fit_trasnform(customer), columns=customer.columns)

# re-Checking of missing values
msno.bar(customer, color='cyan')

customer.duplicated().sum() #Chercking duplicates
customer = customer.drop_duplicates() # Remove duplicates

# Outiliers detection
for column in customer.select_dtypes(include=[np.number]).columns :
    Q1 = customer[column].quantile(0.25)
    Q3 = customer[column].quantile(0.75)
    IQR = Q3 - Q1

    # Limits
    lower_bound = Q1 - 1.5*IQR
    upper_bound = Q3 + 1.5*IQR

    # Outliers corrections
    customer[column] = np.clip(customer[column], lower_bound, upper_bound)

# Conveerting an round
customer_rounded = round(customer)
customer_rounded

# Data normalization
min_scaler = MinMaxScaler()
customer_data_normalized = pd.DataFrame(min_scaler.fit_transform(customer_rounded), columns=customer_rounded.columns)
customer_data_normalized