import streamlit as st
import censusdis.data as ced
import censusdis.maps as cem
from censusdis.datasets import ACS5
from censusdis import states

@st.cache_data
def get_census_data(state_fips, var_table, var_label):
 
    df = ced.download(
        dataset=ACS5,
        vintage=2022,         
        download_variables=['NAME', var_table], 
        state=state_fips,
        county='*',
        with_geometry=True)

    # "San Francisco, California" -> "San Francisco"
    df['NAME'] = df['NAME'].apply(lambda x: x.split(',')[0])

    # The dataframe we get from ced.download has a column with the name of the variable's table (i.e. 'B01001_001E').
    # For convenience, change the name to be the variable's label (i.e. 'Median Household Income'). 
    df = df.rename(columns={var_table: var_label, 'NAME': 'County'})

    return df

st.header('Selected County Demographics (2022)')

all_state_names = list(states.NAMES_FROM_IDS.values())
state_name = st.selectbox("Select a State: ", all_state_names, index=4) # Default to California
state_fips = states.IDS_FROM_NAMES[state_name]

census_vars = {
    # var_label                var_table
    'Total Population'       : 'B01001_001E',
    'Median Household Income': 'B19013_001E',
    'Median Rent'            : 'B25058_001E' }

var_label = st.selectbox("Select a demographic", census_vars.keys())
var_table = census_vars[var_label]

col1, col2 = st.columns(2)

with col1:
    df = get_census_data(state_fips, var_table, var_label)
    df = df.sort_values(var_label, ascending=False)
    st.dataframe(df[['County', var_label]], hide_index=True)

with col2:
    fig = cem.plot_map(df, var_label, legend=True, with_background=True, alpha=.5)
    st.pyplot(fig.figure)

st.write("Created by [Ari Lamstein](https://www.arilamstein.com). View the code [here](https://github.com/arilamstein/censusdis-streamlit).")