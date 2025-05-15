# This script generates the dataset which is used by the app. The final
# structure looks like:
# (STATE_NAME, COUNTY_NAME, YEAR, 'Total Population', 'Worked From Home', ...)
#
# The Census API only lets you get data from one year at a time. So the core of
# this script is a for loop like:
#
# df = None
# for year in years:
#   Get data for this year
#   Append it to df
#
# But there are issues with the raw data that we want to address:
#
# 1. One variable which we are interested in ('Worked from Home') changed name
# during the time period (it started as B08006_021E and moved to B08006_017E).
# This script combines those two datasets into a single column.
#
# 2. Variable changes like the above are important but can be hard to detect.
# As a safety measure, the script prints out all unique labels that each
# variable has had, so you can visually inspect whether a similar problem
# exists in the dataset.

import pandas as pd
import time
from census_vars import census_vars, get_census_vars_for_year
from backend import get_unique_census_labels
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
ACS1_END_YEAR = 2023
ACS1_SKIP_YEARS = [2020]
years = [
    year
    for year in range(ACS1_START_YEAR, ACS1_END_YEAR + 1)
    if year not in ACS1_SKIP_YEARS
]

for one_year in years:
    # Provide some feedback on progress to the user
    print(".", end="", flush=True)

    # Get all the variables we want to view in the app, plus the name of the county
    vars = list(get_census_vars_for_year(one_year).keys())
    vars.append("NAME")

    df_new = ced.download(
        dataset=ACS1,
        vintage=one_year,
        download_variables=vars,
        state=ALL_STATES_AND_DC,
        county="*",
    )

    # Add in some new columns to make working with the data a bit easier
    df_new["COUNTY_NAME"] = df_new["NAME"].apply(lambda name: name.split(", ")[0])
    df_new["STATE_NAME"] = df_new["NAME"].apply(lambda name: name.split(", ")[1])

    df_new = df_new.set_index(["STATE", "COUNTY"])
    df_new["YEAR"] = one_year

    if df_county_data is None:
        df_county_data = df_new
    else:
        df_county_data = pd.concat([df_county_data, df_new])

print(f"\nGenerating all historic data took {(time.time() - start_time):.1f} seconds.")
print(
    f"The resulting dataframe has {len(df_county_data.index):,} rows with {len(df_county_data.index.unique()):,} "
    + "unique counties."
)

# The data appears to already be sorted this way, but I want to ensure that.
df_county_data = df_county_data.sort_values(["STATE", "COUNTY", "YEAR"])

print("\nPrinting the unique labels used for each variable in the dataframe.")
print(
    "Check to make sure no single varible is not used for completely different things over the years!"
)
print_labels_for_variables_over_time(df_county_data)


# Merge the two columns that have work from home data.
def splice_wfh_columns(row):
    # Error check: ensure that, for each row, at *most* one of them has data
    # (For small regions, both values will be NA)
    assert pd.isna(row["B08006_021E"]) or pd.isna(row["B08006_017E"])

    # If the first is not NA, then return it
    if not pd.isna(row["B08006_021E"]):
        return row["B08006_021E"]
    else:
        return row["B08006_017E"]


df_county_data["Total Worked from Home"] = df_county_data.apply(
    splice_wfh_columns, axis=1
)
del df_county_data["B08006_021E"]
del df_county_data["B08006_017E"]

# Rename the columns from names (B01001) to labels ("Total Population")
df_county_data = df_county_data.rename(columns=census_vars)

# Reorder columns
column_order = ["STATE_NAME", "COUNTY_NAME", "YEAR"]
column_order.extend(
    get_unique_census_labels()
)  # Columns appear in same order as UI dropdown
df_county_data = df_county_data[column_order]

# Remove the index and drop those columns.
# Retain FIPS code as a single column for mapping.
df_county_data = (
    df_county_data.reset_index()
    .assign(FIPS=lambda x: x.STATE + x.COUNTY)
    .drop(columns=["STATE", "COUNTY"])
)

df_county_data.to_csv("county_data.csv", index=False)
