# Code for custom code recipe filter_correlation (imported from a Python recipe)

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

# To  retrieve the datasets of an input role named 'input_A' as an array of dataset names:
input_A_names = get_input_names_for_role('input')
# The dataset objects themselves can then be created like this:
input_A_datasets = [dataiku.Dataset(name) for name in input_A_names]

# For outputs, the process is the same:
output_A_names = get_output_names_for_role('main_output')
output_A_datasets = [dataiku.Dataset(name) for name in output_A_names]


# The configuration consists of the parameters set up by the user in the recipe Settings tab.

# Parameters must be added to the recipe.json file so that DSS can prompt the user for values in
# the Settings tab of the recipe. The field "params" holds a list of all the params for wich the
# user will be prompted for values.

# The configuration is simply a map of parameters, and retrieving the value of one of them is simply:
condition = get_recipe_config()['condition']
threshold = get_recipe_config()['threshold']
keep_multiple = get_recipe_config()['keep_multiple']
keep_patterns = get_recipe_config()['keep_patterns']

# For optional parameters, you should provide a default value in case the parameter is not present:
# my_variable = get_recipe_config().get('parameter_name', None)

# Note about typing:
# The configuration of the recipe is passed through a JSON object
# As such, INT parameters of the recipe are received in the get_recipe_config() dict as a Python float.
# If you absolutely require a Python int, use int(get_recipe_config()["my_int_param"])


#############################
# Your original recipe
#############################

import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from eda.correlations import get_rejected_variables
from wp8 import remove_volume_without_close
from build_features import *

# Read the input
input_dataset = input_A_datasets[0]
df = input_dataset.get_dataframe()

rejected_variables = get_rejected_variables(df, threshold=threshold, keep_multiple=keep_multiple, keep_patterns=keep_patterns, condition=condition)
output = df.drop(rejected_variables, axis=1)

# df_without_volume = remove_volume_without_close(df)

# rejected_variables_90 = get_rejected_variables(df, threshold=0.90, substring_overrides='LCOc1')

# Write the output to the output dataset
output_dataset =  output_A_datasets[0]
output_dataset.write_with_schema(pd.DataFrame(output))