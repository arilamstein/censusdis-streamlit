# Generating the dataset which the app uses is somewhat complicated.
#
# Fundamentally, we want to generate time series data on each county over the totality of the ACS 1-Year Survey (2005-2022).
# However, counties change: Some counties which existed in the past do not exist today. The app runs smoother 
# if the dataset it uses only has data on counties which exist today. So we:
#
#     1. Generate all data on all counties for each year the survey was published
#     2. Generate all counties which exist today
#     3. Remove counties from (1) that do not exist in (2)
#     4. Write the resulting dataset to disk
#
# See "Substantial Changes to Counties and County Equivalent Entities: 1970-Present" for more information:
# https://www.census.gov/programs-surveys/geography/technical-documentation/county-changes.html

# Step 1: Generate all data for all states and all counties over the time period that we're interested in
import pandas as pd
import time
from census_vars import census_vars
import censusdis.data as ced
from censusdis.datasets import ACS1
from censusdis.states import ALL_STATES_AND_DC

print("Generating data. Please wait.")

start_time = time.time()
df_county_data = None

# Skip 2020 because it was not published due to covid.
# See https://www.census.gov/programs-surveys/acs/data/experimental-data.html
years =[2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022]

# Get all the variables we want to view in the app, plus the name of the county
vars = list(census_vars.values())
vars.append('NAME')

for one_year in years: 
    print('.', end='', flush=True) # Provide some feedback on progress to the user
    df_new = ced.download(
        dataset = ACS1,
        vintage = one_year,
        download_variables = vars,
        state = ALL_STATES_AND_DC,
        county = '*')
    
    # Add in some new columns to make working with the data a bit easier
    df_new['COUNTY_NAME'] = df_new['NAME'].apply(lambda name: name.split(', ')[0])
    df_new['STATE_NAME']  = df_new['NAME'].apply(lambda name: name.split(', ')[1])

    df_new = df_new.set_index(['STATE', 'COUNTY'])
    df_new['YEAR'] = one_year

    if df_county_data is None:
        df_county_data = df_new
    else:
        df_county_data = pd.concat([df_county_data, df_new])

print(f"\nGenerating all historic data took {(time.time() - start_time):.1f} seconds")
print(f"The resulting dataframe has {len(df_county_data.index)} rows with {len(df_county_data.index.unique())} unique counties")

# Step 2: Get a list of all counties which exist today
df_current_counties = ced.download(
    dataset=ACS1,
    vintage=2022,
    download_variables='NAME',
    state=ALL_STATES_AND_DC,
    county='*'
)

df_current_counties = df_current_counties.set_index(['STATE', 'COUNTY'])
print(f"The dataframe of current counties is {len(df_current_counties.index)} rows")

# Step 3: drop all rows in df_county_data that don't have an entry in df_current_counties
df_current_counties = df_current_counties.drop(columns='NAME')
df_merge = df_current_counties.join(df_county_data, how='left')

print(f"After filtering df_county_data to only current counties, the resulting dataframe has {len(df_merge.index)} rows with {len(df_merge.index.unique())} unique counties")

df_merge.to_csv('county_data.csv')