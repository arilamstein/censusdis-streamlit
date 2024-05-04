import pandas as pd
from census_vars import census_vars

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
