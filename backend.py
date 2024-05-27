import pandas as pd
import numpy as np
from census_vars import census_vars
import json

df = pd.read_csv('county_data.csv', dtype={'FIPS': str, 'YEAR': str})
with open("county_map.json", "r") as read_file:
    county_map = json.load(read_file)

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
# In short: the order in which census_vars lists the variables is the order
# in which I want them to appear in the dropdown. The issue is that they contain
# duplicates due to the variable for "Work From Home" changing name throughtout
# the years. This code removes the duplicates while retaining the initial ordering,
# and prevents me from needing to duplicate data here. 
# See: https://stackoverflow.com/a/17016257/2518602
def get_unique_census_labels():
    return list(dict.fromkeys(census_vars.values()))

def get_ranking_df(column):
    df2 = df.copy() # We don't want to modify the global variable

    # Select just the rows and columns we need
    df2 = df2.loc[(df2['YEAR'] == '2019') | (df2['YEAR'] == '2021')]
    df2 = df2[['STATE_NAME', 'COUNTY_NAME', 'YEAR', column]]

    # Combine state and county into a single column
    df2 = df2.assign(County=lambda x: x.COUNTY_NAME + ', ' + x.STATE_NAME)
    df2 = df2.drop(columns=['STATE_NAME', 'COUNTY_NAME'])

    # Pivot for structure we need, calculate change and percent change, sort
    df2 = df2.pivot_table(index='County', columns='YEAR', values=column)
    df2['Change'] = df2['2021'] - df2['2019']
    df2['Percent Change'] = (df2['2021'] - df2['2019']) / df2['2019'] * 100
    df2['Percent Change'] = df2['Percent Change'].round(1)
    df2 = df2.sort_values('Percent Change', ascending=False)

    # Create an index called "Rank" and drop columns with NA
    df2['Rank'] = list(range(1, len(df2.index) + 1))
    df2 = df2.reset_index().set_index('Rank')
    df2 = df2.dropna()

    return df2

def get_ranking_text(state, county, var, ranking_df):
    full_name = ', '.join([county, state])

    if not full_name in ranking_df['County']:
        return f"**{full_name}** does not have a ranking for **{var}**."
    
    rank = (
        ranking_df
        [ranking_df['County'] == full_name]
        .index
        .tolist()[0]
    )

    num_counties = len(ranking_df.index)

    return f"{full_name} ranks **{rank}** of {num_counties}."

def get_mapping_df(column):
    df2 = df.copy() # We don't want to modify the global variable

    # Select just the rows and columns we need
    df2 = df2.loc[(df2['YEAR'] == '2019') | (df2['YEAR'] == '2021')]
    df2 = df2[['FIPS', 'STATE_NAME', 'COUNTY_NAME', 'YEAR', column]]

    # Combine state and county into a single column
    df2 = df2.assign(County=lambda x: x.COUNTY_NAME + ', ' + x.STATE_NAME)
    df2 = df2.drop(columns=['STATE_NAME', 'COUNTY_NAME'])

    # Pivot for structure we need, calculate change and percent change, sort
    df2 = df2.pivot_table(index=['FIPS', 'County'], columns='YEAR', values=column)
    df2['Change'] = df2['2021'] - df2['2019']
    df2['Percent Change'] = (df2['2021'] - df2['2019']) / df2['2019'] * 100
    df2['Percent Change'] = df2['Percent Change'].round(1)
    df2 = df2.sort_values('Percent Change', ascending=False)

    df2 = (
        df2
        .replace([np.inf, -np.inf], np.nan)
        .dropna()
        .reset_index()
    )

    # Color the map with 4 quartiles. This allows the user to quickly see high-level geographic
    # patterns in the data. The default (continuous) scale highlights outliers, which we already
    # show in the "Rankings" tab.
    df2['Quartile'] = pd.qcut(df2['Percent Change'], q=4)

    return df2