import pandas as pd
import censusdis.data as ced
from censusdis.datasets import ACS5
from geopy.geocoders import Nominatim

# Leading zeros can be important in FIPS codes, so read all columns in as strings
df_county_names = pd.read_csv('county_names.csv', dtype=str)

def get_state_names():
    return df_county_names['state.name'].unique()

def get_county_names(state_name):
    return (
        df_county_names
        .loc[df_county_names['state.name'] == state_name]
        ['county.name']
    )

def get_county_fips_codes(state_name, county_name):
    return (
        df_county_names
        .loc[(df_county_names['state.name'] == state_name) & (df_county_names['county.name'] == county_name)] # The row
        [['state.fips', 'county.fips']] # The columns we care about
        .values.tolist() # As a list of lists (one list per row)
        [0] # There is only 1 row, so return the first element
    )

census_vars = {
    # var_label                var_table
    'Median Household Income': 'B19013_001E',
    'Total Population'       : 'B01001_001E',
    'Median Rent'            : 'B25058_001E' }

# See https://github.com/arilamstein/censusdis-streamlit/issues/3#issuecomment-1986709449
def get_hover_data_for_var_label(var_label):
    if var_label == 'Total Population':
        return ":,"
    else:
        return ":$,"

def get_census_data(state_name, county_name, var_table, var_label):
 
    state_fips, county_fips = get_county_fips_codes(state_name, county_name)
    df = ced.download(
        dataset=ACS5,
        vintage=2022,         
        download_variables=['NAME', var_table], 
        state=state_fips,
        county=county_fips,
        tract='*',
        with_geometry=True)

    # "San Francisco, California" -> "San Francisco"
    # df['NAME'] = df['NAME'].apply(lambda x: x.split(';')[0])

    # The dataframe we get from ced.download has a column with the name of the variable's table (i.e. 'B01001_001E').
    # For convenience, change the name to be the variable's label (i.e. 'Median Household Income'). 
    df = df.rename(columns={var_table: var_label})
    
    # See https://stackoverflow.com/questions/78133591/plotly-express-choropleth-of-census-data-fails
    df = df.dropna()

    return df

# Based on https://gist.github.com/ramnathv/348091984eff52aa4fbbe31861a2a50f#file-backend-py-L77
def get_county_center_lat_lon(state_name, county_name):
  """Get lat,lon for center of county"""
  geolocator = Nominatim(user_agent="county_center_locator")
  query = f"Center of {county_name}, {state_name}, USA"
  location = geolocator.geocode(query)
  return {"lat": location.latitude, "lon": location.longitude}