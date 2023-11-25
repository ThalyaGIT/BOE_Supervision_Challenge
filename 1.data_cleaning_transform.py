import pandas as pd
import numpy as np

# convert first excel into dataframe
general_df = pd.read_excel('raw_dataset.xlsx', sheet_name=0)
underwritting_df = pd.read_excel('raw_dataset.xlsx', sheet_name=1)

# The goal of this script is to format the general dataset into one that is more usable for data visualisaton in Tableau

# Combine the Year End and Metric columns
general_df.columns = general_df.columns + '_' + general_df.iloc[0]
general_df = general_df.drop([0])

underwritting_df.columns = underwritting_df.columns + '_' + underwritting_df.iloc[0]
underwritting_df = underwritting_df.drop([0])

# Rename first column to "Firm Name"
general_df.columns.values[0] = 'Firm Name'
underwritting_df.columns.values[0] = 'Firm Name'

# Merge the two dataframes
df = general_df.merge(underwritting_df, left_on='Firm Name', right_on='Firm Name', how='outer')

# Melt dataframe
df = pd.melt(df, id_vars=['Firm Name'], var_name='Metric', value_name='Value')

# Remove unwanted characters from Atribute
df['Metric'] = df['Metric'].str.replace('.1', '')
df['Metric'] = df['Metric'].str.replace('.2', '')
df['Metric'] = df['Metric'].str.replace('.3', '')
df['Metric'] = df['Metric'].str.replace('.4', '')

# Split Year End values from Metrics into different columns
df[['Metric', 'Year End']] = df['Metric'].str.split('_', expand=True)

# Remove "YE" from Year End values
df['Year End'] = df['Year End'].str.replace('YE', '')

# Configure data types
df['Firm Name'] = df['Firm Name'].astype(str)
df['Metric'] = df['Metric'].astype(str)
df['Value'] = df['Value'].astype(float)
df['Year End'] = df['Year End'].astype(str)

# Unmelt dataframe
df = pd.pivot_table(df, values = 'Value', index=['Firm Name','Year End'], columns = 'Metric').reset_index()

# Remove index column name
df = df.rename_axis(None, axis=1)

# Replace all zeros with NaN given that is unlikely a zero is the real value of those metrics
df.replace(0, np.nan, inplace=True)

# Save dataframe as CSV
df.to_csv('clean_dataset.csv', encoding='utf-8', index=False)
print(df)