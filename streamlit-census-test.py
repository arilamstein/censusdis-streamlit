import streamlit as st
#import censusdis
import censusdis.data as ced
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

st.header('My first census explorer thingy!')

all_state_names = list(states.NAMES_FROM_IDS.values())
state_name = st.selectbox("Select a State to get data on: ",all_state_names)
state_fips = states.IDS_FROM_NAMES[state_name]

st.write("You selected ", state_name)
st.write("The FIPS code of that that state is ", state_fips)

st.write(get_median_income(state_fips))