import pandas as pd
import numpy as np
from scipy import stats

#Create a sample DataFrame of student heights
df = pd.read_csv('clean_dataset.csv')
df['Year End'] = df['Year End'].astype(str)

numeric_cols = df.select_dtypes(include=[np.number]).columns
print(numeric_cols)

# Calculate quantiles and IQR
Q1 = df[numeric_cols].quantile(0.25) # Same as np.percentile but maps (0,1) and not (0,100)
Q3 = df[numeric_cols].quantile(0.75)
IQR = Q3 - Q1

# Return a boolean array of the rows with (any) non-outlier column values
condition = ~((df[numeric_cols] < (Q1 - 5 * IQR)) | (df[numeric_cols] > (Q3 + 5 * IQR))).any(axis=1)

