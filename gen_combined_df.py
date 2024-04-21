import pandas as pd

# For the purposes of this app, fips codes are treated as numeric, so leading 0's are dropped
df_county_names = pd.read_csv('county_names.csv', index_col='fips')
df_county_data = pd.read_csv('county_data_for_all_years.csv', index_col='fips')

# TODO: This join loses 9 rows in Virginia:
# {9110, 9120, 9130, 9140, 9150, 9160, 9170, 9180, 9190}
#
# This can be verified with the following code:
# print(len(df_county_names.index))
# print(len(df_county_data.index))
# len(df_county_data.join(df_county_names, how="inner").index)
# set(df_county_data.index) - set(df_county_names.index)
#
# At some point I will need to dig into this to find out why. It might be because the 
# the fips data I'm using is from a point in time, and the demographic data is a ~20 year times series.
# I.e., fips codes / names change, and so I might need a fundamentally different approach to this.
# See, for example, the complete overhaul of county names in Connecticut. It's possible something similar 
# happene in Virginia.
df_combined = df_county_data.join(df_county_names, how='left')

df_combined.to_csv('combined_county_data.csv')