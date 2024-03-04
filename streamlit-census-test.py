import streamlit as st
import censusdis.data as ced
from censusdis.datasets import ACS5
import plotly.express as px
import pandas as pd

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

st.header('Selected County Demographics (2022)')
state_name = st.selectbox("Select a State:", get_state_names()) 
county_name = st.selectbox("Select a County:", get_county_names(state_name))

census_vars = {
    # var_label                var_table
    'Median Household Income': 'B19013_001E',
    'Total Population'       : 'B01001_001E',
    'Median Rent'            : 'B25058_001E' }

var_label = st.selectbox("Select a demographic", census_vars.keys())
var_table = census_vars[var_label]

@st.cache_data
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
    df['NAME'] = df['NAME'].apply(lambda x: x.split(';')[0])

    # The dataframe we get from ced.download has a column with the name of the variable's table (i.e. 'B01001_001E').
    # For convenience, change the name to be the variable's label (i.e. 'Median Household Income'). 
    df = df.rename(columns={var_table: var_label, 'NAME': 'County'})

    return df

df = get_census_data(state_name, county_name, var_table, var_label)

col1, col2 = st.columns(2)

with col1:
    df = df.sort_values(var_label, ascending=False)
    st.dataframe(df[['County', var_label]], hide_index=True)

with col2:
    df = df.set_index('County')
    fig = px.choropleth(df, geojson=df.geometry, locations=df.index, 
                        color=var_label, color_continuous_scale="Viridis",
                        projection="mercator")
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig)

st.write("Created by [Ari Lamstein](https://www.arilamstein.com). View the code [here](https://github.com/arilamstein/censusdis-streamlit).")
