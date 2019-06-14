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
input_A_names = get_input_names_for_role('input_A_role')
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
my_variable = get_recipe_config()['parameter_name']

# For optional parameters, you should provide a default value in case the parameter is not present:
my_variable = get_recipe_config().get('parameter_name', None)

# Note about typing:
# The configuration of the recipe is passed through a JSON object
# As such, INT parameters of the recipe are received in the get_recipe_config() dict as a Python float.
# If you absolutely require a Python int, use int(get_recipe_config()["my_int_param"])


#############################
# Your original recipe
#############################

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: MARKDOWN
# # Analyzing correlations between variables in merged_raw_data_targets_prepared

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: MARKDOWN
# ### Correlations > 0.99

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from eda.correlations import get_rejected_variables
from wp8 import remove_volume_without_close

# Read recipe inputs
merged_raw_data_targets_prepared = dataiku.Dataset("merged_raw_data_targets_prepared")
merged_raw_data_targets_prepared_df = merged_raw_data_targets_prepared.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
rejected_variables_99 = get_rejected_variables(merged_raw_data_targets_prepared_df, threshold=0.99)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df = merged_raw_data_targets_prepared_df.drop(rejected_variables_99, axis=1)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df.corr()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: MARKDOWN
# For each RIC: CLOSE, HIGH, LOW and OPEN columns are highly correlated.
# 
# => Only the CLOSE will be kept for further analysis.

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: MARKDOWN
# Do we remove the volume columns without?

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df_without_volume = remove_volume_without_close(df)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: MARKDOWN
# ### Correlations > 0.90

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
rejected_variables_90 = get_rejected_variables(df, threshold=0.90, substring_overrides='LCOc1')

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: MARKDOWN
# High correlation between:
# 
# - US crude oil stocks | Brent Crude closing prices
# - Baker Hughes RIG count - North America | Brent Crude closing prices
# - global refinery runrates | global refinery outages
# 
# Which variable do we remove?

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Write recipe outputs
data_targets_filter_high_corr = dataiku.Dataset("data_targets_filter_high_corr")
data_targets_filter_high_corr.write_with_schema(df)