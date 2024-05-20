import pandas as pd
from census_vars import all_census_vars

df = pd.read_csv('county_data.csv')

def get_state_names():
    return df['STATE_NAME'].unique()

def get_county_names(state_name):
    return (
        df
        .loc[df['STATE_NAME'] == state_name]
        ['COUNTY_NAME']
        .sort_values()
        .unique()
    )

def get_census_data(state_name, county_name, var):
    return (
        df
        .loc[(df['STATE_NAME'] == state_name) & (df['COUNTY_NAME'] == county_name)]
        [['STATE_NAME', 'COUNTY_NAME', 'YEAR', var]]
    )

# This code is hard to read but it serves a purpose.
# In short: the order in which all_census_vars lists the variables is the order
# in which I want them to appear in the dropdown. The issue is that they contain
# duplicates due to the variable for "Work From Home" changing name throughtout
# the years. This code removes the duplicates while retaining the initial ordering,
# and prevents me from needing to duplicate data here. 
# See: https://stackoverflow.com/a/17016257/2518602
def get_unique_census_labels():
    return list(dict.fromkeys(all_census_vars.values()))
