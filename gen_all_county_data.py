import pandas as pd
import time
from backend import census_vars
import censusdis.data as ced
from censusdis.datasets import ACS1
from censusdis.states import ALL_STATES_AND_DC

start_time = time.time()
df_all = None

# Skip 2020 because it was not published due to covid.
# See https://www.census.gov/programs-surveys/acs/data/experimental-data.html
years =[2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022]
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

# Took me about 1 minute
print(f"Script gen_all_county_data.py finished in {time.time() - start_time}")