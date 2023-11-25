import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load your dataset
df = pd.read_csv('clean_dataset_2.csv')

# filter by year
df = df[df['Year End'] == 2020]

# Select the relevant metrics for clustering
metrics = df.select_dtypes(include=[np.number]).columns

# Extract the selected metrics
data = df[metrics]

# Handle missing values
data.fillna(data.mean(), inplace=True) 

# Standardize the data (important for K-means)
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

# Choose the number of clusters (you may need to experiment with this)
num_clusters = 4

# Apply K-means clustering
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(scaled_data)

# Print the clusters assigned to each firm
pd.set_option('display.max_rows', None)
print(df[['Firm Name', 'cluster']])