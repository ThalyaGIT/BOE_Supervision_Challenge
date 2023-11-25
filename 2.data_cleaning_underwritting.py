import pandas as pd

# convert second excel into dataframe
underwritting_df = pd.read_excel('raw_dataset.xlsx', sheet_name=1)

# The goal of this script is to format the underwritting dataset into one that is more usable for data visualisaton in Tableau

# Combine the Year End and Metric columns
underwritting_df.columns = underwritting_df.columns + '_' + underwritting_df.iloc[0]
underwritting_df = underwritting_df.drop([0])

# Rename first column to "Firm Name"
underwritting_df.columns.values[0] = 'Firm Name'

# Melt dataframe
underwritting_df = pd.melt(underwritting_df, id_vars=['Firm Name'], var_name='Metric', value_name='Value')

# Remove unwanted characters from Metric
underwritting_df['Metric'] = underwritting_df['Metric'].str.replace('.1', '')
underwritting_df['Metric'] = underwritting_df['Metric'].str.replace('.2', '')
underwritting_df['Metric'] = underwritting_df['Metric'].str.replace('.3', '')
underwritting_df['Metric'] = underwritting_df['Metric'].str.replace('.4', '')

# Split Year End values from Metrics into different columns
underwritting_df[['Metric', 'Year End']] = underwritting_df['Metric'].str.split('_', expand=True)

# Remove "YE" from Year End values
underwritting_df['Year End'] = underwritting_df['Year End'].str.replace('YE', '')

# Configure data types
underwritting_df['Firm Name'] = underwritting_df['Firm Name'].astype(str)
underwritting_df['Metric'] = underwritting_df['Metric'].astype(str)
underwritting_df['Value'] = underwritting_df['Value'].astype(float)
underwritting_df['Year End'] = underwritting_df['Year End'].astype(str)

# Unmelt dataframe
underwritting_df = pd.pivot_table(underwritting_df, values = 'Value', index=['Firm Name','Year End'], columns = 'Metric').reset_index()

# Remove index column name
underwritting_df = underwritting_df.rename_axis(None, axis=1)

# Display the DataFrame
print(underwritting_df)
underwritting_df.to_csv('clean_underwritting_tableau.csv', encoding='utf-8', index=False)