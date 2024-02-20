import streamlit as st
import censusdis.data as ced
import censusdis.maps as cem
from censusdis.datasets import ACS5
from censusdis import states

@st.cache_data
def get_median_income(state_fips):
 
    return ced.download(
        # Data set: American Community Survey 5-Year
        dataset=ACS5,
        
        # Vintage: 2022
        vintage=2022, 
        
        # Variable: median household income
        download_variables=['NAME', 'B19013_001E'], 
        
        # Geography: All counties in New Jersey.
        state=state_fips,
        county='*',
        with_geometry=True)

st.header('2022 County-Level Median Income')

all_state_names = list(states.NAMES_FROM_IDS.values())
state_name = st.selectbox("Select a State: ",all_state_names)
state_fips = states.IDS_FROM_NAMES[state_name]

df = get_median_income(state_fips)
st.dataframe(df[['NAME', 'B19013_001E']], hide_index=True)
fig = cem.plot_map(df, 'B19013_001E', legend=True, with_background=True)
st.pyplot(fig.figure)

st.write("[github](https://github.com/arilamstein/censusdis-streamlit)")