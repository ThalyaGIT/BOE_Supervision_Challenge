import pandas as pd

# convert first excel into dataframe
general_df = pd.read_excel('raw_dataset.xlsx', sheet_name=0)

# The goal of this script is to format the general dataset into one that is more usable for data visualisaton in Tableau

# Combine the Year End and Metric columns
general_df.columns = general_df.columns + '_' + general_df.iloc[0]
general_df = general_df.drop([0])

# Rename first column to "Firm Name"
general_df.columns.values[0] = 'Firm Name'

# Melt dataframe
general_df = pd.melt(general_df, id_vars=['Firm Name'], var_name='Metric', value_name='Value')

# Remove unwanted characters from Atribute
general_df['Metric'] = general_df['Metric'].str.replace('.1', '')
general_df['Metric'] = general_df['Metric'].str.replace('.2', '')
general_df['Metric'] = general_df['Metric'].str.replace('.3', '')
general_df['Metric'] = general_df['Metric'].str.replace('.4', '')

# Split Year End values from Metrics into different columns
general_df[['Metric', 'Year End']] = general_df['Metric'].str.split('_', expand=True)

# Remove "YE" from Year End values
general_df['Year End'] = general_df['Year End'].str.replace('YE', '')

# Configure data types
general_df['Firm Name'] = general_df['Firm Name'].astype(str)
general_df['Metric'] = general_df['Metric'].astype(str)
general_df['Value'] = general_df['Value'].astype(float)
general_df['Year End'] = general_df['Year End'].astype(str)

# Unmelt dataframe
general_df = pd.pivot_table(general_df, values = 'Value', index=['Firm Name','Year End'], columns = 'Metric').reset_index()

# Remove index column name
general_df = general_df.rename_axis(None, axis=1)

# Display the DataFrame
print(general_df)
general_df.to_csv('clean_general_tableau.csv', encoding='utf-8', index=False)