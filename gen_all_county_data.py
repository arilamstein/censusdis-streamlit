import pandas as pd
from backend import census_vars

import censusdis.data as ced
from censusdis.datasets import ACS1
from censusdis.states import ALL_STATES_AND_DC

df_all = None

# Skip 2020 for now because data appears to be missing! 
# See https://www.census.gov/programs-surveys/acs/data/experimental-data.html
years =[2018, 2019, 2021, 2022]
for one_year in years: 
    df_new = ced.download(
        dataset=ACS1,
        vintage=one_year,
        download_variables=census_vars.values(),
        state=ALL_STATES_AND_DC,
        county='*'
    )
    df_new = df_new.set_index(['STATE', 'COUNTY'])
    df_new['YEAR'] = one_year

    if df_all is None:
        df_all = df_new
    else:
        df_all = pd.concat([df_all, df_new])

df_all.to_csv('county_data_for_all_years.csv')