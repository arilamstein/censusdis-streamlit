# This script generates the dataset which is used by the app. The final 
# structure looks similar to:
# (STATE_NAME, COUNTY_NAME, YEAR, 'Total Population', 'Worked From Home', ...)
#
# The Census API only lets you get data one year at a time. So the core of 
# this script is a for loop like:
#
# df = None
# for year in years:
#   Get data for this year
#   Append it to df
#
# But there are issues with the raw data that we want to address:
# 
# 1. Some counties existed in the past but do not exist today. We "prune" df so
# it only includes counties which are present in the last year of the dataset.
# See "Substantial Changes to Counties and County Equivalent Entities: 
# 1970-Present" for more information:
# https://www.census.gov/programs-surveys/geography/technical-documentation/county-changes.html
#
# 2. One variable which we are interested in ('Worked from Home') changed name 
# during the time period (it started as B08006_021E and moved to B08006_017E). 
# This script combines those two datasets into a single column.
#
# 3. Variable changes like the above are important but can be hard to detect. 
# As a safety measure, the script prints out all unique labels that each 
# variable has had, so you can visually inspect whether a similar problem 
# exists in the dataset.

# Step 1: Generate all data for all states and all counties over the time 
# period that we're interested in
import pandas as pd
import time
from census_vars import all_census_vars, get_census_vars_for_year
import censusdis.data as ced
from censusdis.datasets import ACS1
from censusdis.states import ALL_STATES_AND_DC
from validate_variable_labels import print_labels_for_variables_over_time

print("Generating data. Please wait.")

start_time = time.time()
df_county_data = None

# We want all years the ACS1 was published. Note that it was not published in 2020 due to covid.
# See https://www.census.gov/programs-surveys/acs/data/experimental-data.html
ACS1_START_YEAR = 2005
ACS1_END_YEAR   = 2022
ACS1_SKIP_YEARS = [2020]
years = [year 
         for year in range(ACS1_START_YEAR, ACS1_END_YEAR + 1) 
         if year not in ACS1_SKIP_YEARS]

for one_year in years: 
    # Provide some feedback on progress to the user
    print('.', end='', flush=True) 

    # Get all the variables we want to view in the app, plus the name of the county
    vars = list(get_census_vars_for_year(one_year).keys())
    vars.append('NAME')

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
    vintage=ACS1_END_YEAR,
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

# The data appears to already be sorted this way, but I want to ensure that.
df_merge = df_merge.sort_values(['STATE', 'COUNTY', 'YEAR'])

print("\nPrinting the unique labels used for each variable in the dataframe.")
print("Check to make sure no single varible is not used for completely different things over the years!")
print_labels_for_variables_over_time(df_merge)

# Merge the two columns that have work from home data.
# But ensure that, for each row, at most one of them has data
# (For small regions, both values will be na)
for i in range(len(df_merge.index)):
    assert pd.isna(df_merge.iloc[i]['B08006_021E']) or pd.isna(df_merge.iloc[i]['B08006_017E']) 

df_merge['Worked from Home'] = df_merge['B08006_021E'].fillna(0) + df_merge['B08006_017E'].fillna(0)
del df_merge['B08006_021E']
del df_merge['B08006_017E']

# Rename the columns from names (B01001) to labels ("Total Population")
df_merge = df_merge.rename(columns = all_census_vars)

# Reorder columns
column_order = ['STATE_NAME', 'COUNTY_NAME', 'YEAR']
column_order.extend(set(all_census_vars.values())) # Remove duplicate 'Worked from Home'
df_merge = df_merge[column_order]

df_merge.to_csv('county_data.csv')