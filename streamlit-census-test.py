import streamlit as st
import censusdis.data as ced
import censusdis.maps as cem
from censusdis.datasets import ACS5
from censusdis import states

@st.cache_data
def get_census_data(state_fips, census_var):
 
    return ced.download(
        dataset=ACS5,
        vintage=2022,         
        download_variables=['NAME', census_var], 
        state=state_fips,
        county='*',
        with_geometry=True)

st.header('2022 County-Level Median Income')

all_state_names = list(states.NAMES_FROM_IDS.values())
state_name = st.selectbox("Select a State: ",all_state_names)
state_fips = states.IDS_FROM_NAMES[state_name]

# all_census_vars = {'Median Household Income': 'B19013_001E',
#                'Median Rent': 'B25058_E',
#                'Median Age': 'B01002_E'}
all_census_vars = {'Median Household Income': 'B19013_001E'}

selected_census_var = st.selectbox("Select a demographic", all_census_vars.keys())
census_var = all_census_vars[selected_census_var]

df = get_census_data(state_fips, census_var)
st.dataframe(df[['NAME', census_var]], hide_index=True)

fig = cem.plot_map(df, 'B19013_001E', legend=True, with_background=True, alpha=.5)
st.pyplot(fig.figure)

st.write("View the code [here](https://github.com/arilamstein/censusdis-streamlit).")