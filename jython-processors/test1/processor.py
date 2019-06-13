# This file is the actual code for the custom Jython step test1

# global- and project-level variables are passed as a dss_variables dict

# the step parameters are passed as a params dict

# Define here a function that returns the result of the step.
def process(row):
    # row is a dict of the row on which the step is applied

    return len(row)
