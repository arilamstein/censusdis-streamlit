import pandas as pd
import censusdis.data as ced
from censusdis.datasets import ACS5
import shapely

df_combined = pd.read_csv('combined_county_data.csv')

def get_state_names():
    return df_combined['state.name'].unique()

def get_county_names(state_name):
    return (
        df_combined
        .loc[df_combined['state.name'] == state_name]
        ['county.name']
        .sort_values()
        .unique()
    )

def get_county_fips_codes(state_name, county_name):
    return (
        df_combined
        .loc[(df_combined['state.name'] == state_name) & (df_combined['county.name'] == county_name)] # The row
        [['state.fips', 'county.fips']] # The columns we care about
        .values.tolist() # As a list of lists (one list per row)
        [0] # There is only 1 row, so return the first element
    )

census_vars = {
    # var_label                var_table
    'Median Household Income': 'B19013_001E',
    'Total Population'       : 'B01001_001E',
    'Median Rent'            : 'B25058_001E' 
    # TODO: Maybe add B08006_017E - Work from Home?
}

census_vars_reverse = {v: k for k, v in census_vars.items()}

# See https://github.com/arilamstein/censusdis-streamlit/issues/3#issuecomment-1986709449
def get_hover_data_for_var_label(var_label):
    if var_label == 'Total Population':
        return ":,"
    else:
        return ":$,"

def get_census_data(state_name, county_name, var_label):
 
    var_table = census_vars[var_label]

    return (
        df_combined
        .loc[(df_combined['state.name'] == state_name) & (df_combined['county.name'] == county_name)]
        [['state.name', 'county.name', 'YEAR', var_table]]
        .rename(columns={var_table: var_label})
    )

# See https://stackoverflow.com/questions/78149896/center-of-geopandas-geodataframe-geodataframe/78150383#78150383
def get_df_center_lat_lon(df):
    """Get lat,lon for center of dataframe"""
    center = shapely.box(*df.total_bounds).centroid
    return {"lat": center.y, "lon": center.x}