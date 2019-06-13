# This file is the actual code for the custom Jython step filter-correlation

# global- and project-level variables are passed as a dss_variables dict

# the step parameters are passed as a params dict

# Define here a function that returns the result of the step.
def process(row):
    # row is a dict of the row on which the step is applied

    print(row)
    
    
    
    
    return len(row)

# import dataiku
# import pandas as pd, numpy as np

# # Retrieve array of dataset names from 'input' role, then create datasets
# input_names = get_input_names_for_role('input')
# input_datasets = [dataiku.Dataset(name) for name in input_names]

# # For outputs, the process is the same:
# output_names = get_output_names_for_role('main_output')
# output_datasets = [dataiku.Dataset(name) for name in output_names]

# # Retrieve parameter values from the of map of parameters
# threshold = get_recipe_config()['threshold']


# # Read the input
# input_dataset = input_datasets[0]
# df = input_dataset.get_dataframe()
# column_names = df.columns

# # We'll only compute correlations on numerical columns
# # So extract all pairs of names of numerical columns
# pairs = []
# for i in xrange(0, len(column_names)):
#     for j in xrange(i + 1, len(column_names)):
#         col1 = column_names[i]
#         col2 = column_names[j]
#         if df[col1].dtype == "float64" and \
#            df[col2].dtype == "float64":
#             pairs.append((col1, col2))

# # Compute the correlation for each pair, and write a
# # row in the output array
# output = []
# for pair in pairs:
#     corr = df[[pair[0], pair[1]]].corr().iloc[0][1]
#     output.append({"col0" : pair[0],
#                    "col1" : pair[1],
#                    "corr" :  corr})

# # Write the output to the output dataset
# output_dataset = output_datasets[0]
# output_dataset.write_with_schema(pd.DataFrame(output))