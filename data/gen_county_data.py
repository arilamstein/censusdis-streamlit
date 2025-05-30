# This script generates the dataset which is used by the app. The final structure looks like:
# (STATE_NAME, COUNTY_NAME, YEAR, 'Total Population', 'Worked from Home', ...)
#
# A complication is that one variable which we are interested in ('Worked from Home')
# changed name over time. In 2005 it was B08006_021E and then was B08006_017E
# in all other years).
#
# This script gets the 2005 data separate from the 2006+ data, and then combines them.

import time
import pandas as pd
from censusdis.datasets import ACS1
from censusdis.states import ALL_STATES_AND_DC
from censusdis.multiyear import download_multiyear
from census_vars import census_vars_2005, census_vars_post_2005, census_dropdown_values

print("Generating data. Please wait.")
start_time = time.time()

df_2005 = download_multiyear(
    dataset=ACS1,
    vintages=[2005],
    download_variables=census_vars_2005.keys(),
    state=ALL_STATES_AND_DC,
    county="*",
    rename_vars=False,
    drop_cols=False,
    prompt=False,
)
df_2005 = df_2005.rename(columns=census_vars_2005)

# When updating data in the future, increment the value of LAST_YEAR. Note that data was not published in
# 2020 due to Covid-19. See https://www.census.gov/programs-surveys/acs/data/experimental-data.html
LAST_YEAR = 2023
years_post_2005 = [year for year in range(2006, LAST_YEAR + 1) if year != 2020]
df_post_2005 = download_multiyear(
    dataset=ACS1,
    vintages=years_post_2005,
    download_variables=census_vars_post_2005.keys(),
    state=ALL_STATES_AND_DC,
    county="*",
    rename_vars=False,
    drop_cols=False,
    prompt=False,
)
df_post_2005 = df_post_2005.rename(columns=census_vars_post_2005)

# Combine the dataframes, and modify the result so that it's easier to work with
df_all = pd.concat([df_2005, df_post_2005])
df_all["COUNTY_NAME"] = df_all["NAME"].apply(lambda name: name.split(", ")[0])
df_all["STATE_NAME"] = df_all["NAME"].apply(lambda name: name.split(", ")[1])

df_all = df_all.rename(columns={"Year": "YEAR"})  # Match how v1 of this script named it
df_all = df_all.sort_values(["STATE", "COUNTY", "YEAR"])

# Drop columns the app doesn't use, but retain FIPS code as a single column for mapping.
df_all = df_all.assign(FIPS=lambda x: x.STATE + x.COUNTY).drop(
    columns=["STATE", "COUNTY", "NAME"]
)

# Reorder columns and drop "NAME" column
column_order = ["STATE_NAME", "COUNTY_NAME", "YEAR", *census_dropdown_values, "FIPS"]
df_all = df_all[column_order]

df_all.to_csv("county_data.csv", index=False)

unique_counties = df_all[["STATE_NAME", "COUNTY_NAME"]].drop_duplicates().shape[0]
print(
    f"\nGenerating the dataset took {(time.time() - start_time):.1f} seconds. "
    f"The resulting dataframe has {len(df_all.index):,} rows with {unique_counties:,} unique counties."
)
