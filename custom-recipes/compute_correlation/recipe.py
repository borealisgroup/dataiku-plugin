# Code for custom code recipe compute_correlation (imported from a Python recipe)

# To finish creating your custom recipe from your original PySpark recipe, you need to:
#  - Declare the input and output roles in recipe.json
#  - Replace the dataset names by roles access in your code
#  - Declare, if any, the params of your custom recipe in recipe.json
#  - Replace the hardcoded params values by acccess to the configuration map

# See sample code below for how to do that.
# The code of your original recipe is included afterwards for convenience.
# Please also see the "recipe.json" file for more information.

# import the classes for accessing DSS objects from the recipe
import dataiku
# Import the helpers for custom recipes
from dataiku.customrecipe import *

# Inputs and outputs are defined by roles. In the recipe's I/O tab, the user can associate one
# or more dataset to each input and output role.
# Roles need to be defined in recipe.json, in the inputRoles and outputRoles fields.

# Retrieve array of dataset names from 'input' role, then create datasets
input_names = get_input_names_for_role('input')
input_datasets = [dataiku.Dataset(name) for name in input_names]

# For outputs, the process is the same:
output_names = get_output_names_for_role('main_output')
output_datasets = [dataiku.Dataset(name) for name in output_names]

# Retrieve parameter values from the of map of parameters
threshold = get_recipe_config()['threshold']
filter_method = get_recipe_config()['filter_method']
col_multiple = get_recipe_config()['col_multiple']
col_patterns = get_recipe_config()['col_patterns']

# Read the input
input_dataset = input_datasets[0]
df = input_dataset.get_dataframe()


#############################
# Your original recipe
#############################
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from eda.filters import filter_columns

# Read recipe inputs
cols = df.columns

df_filtered = filter_columns(df, filter_method=filter_method, col_multiple=col_multiple, col_patterns=col_patterns)
filtered_cols = df_filtered.columns

# We'll only compute correlations on numerical columns
# So extract all pairs of names of numerical columns
pairs = []
for i in range(len(cols)):
    for j in range(len(cols)):
        col1 = cols[i]
        col2 = cols[j]
        if df[col1].dtype == "float64" and col1 != col2 and \
           df[col2].dtype == "float64" and col2 in filtered_cols and (col2, col1) not in pairs:
            pairs.append((col1, col2))


# Compute the correlation for each pair, and write a
# row in the output array
output = []
for pair in pairs:
    corr = df[[pair[0], pair[1]]].corr().iloc[0][1]
    if np.abs(corr) > threshold:
        output.append({"col0" : pair[0],
                     "col1" : pair[1],
                     "corr" :  corr})

df_out = pd.DataFrame(output)
if ('corr' in df_out.columns):
    df_out = df_out.sort_values('corr', ascending=False)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Write the output to the output dataset
output_dataset =  output_datasets[0]
output_dataset.write_with_schema(df_out)