import backend as be
import streamlit as st
import matplotlib.pyplot as plt

st.header('Census Covid Explorer')
st.write('This goal of this app is to shine a light on how US Demographics changed as a result of Covid-19. The app is still under development. Data comes from the American Community Survey 1-year estimates.')

# Set up nice defaults for the various UI elements
state_name = st.selectbox("Select a State:", be.get_state_names(), index=4) # 4 = California
county_name_index = 0
if state_name == "California":
    county_name_index = 25 # San Francisco
elif state_name == "New York":
    county_name_index = 15 # New York (Manhattan)
county_name = st.selectbox("Select a County:", be.get_county_names(state_name), index=county_name_index)

# Something like "Total Population"
var_label = st.selectbox("Select a demographic", be.census_vars.keys())

# Get and chart data
df = be.get_census_data(state_name, county_name, var_label)
col1, col2 = st.columns(2)
with col1:
    # Line graph of raw data
    st.pyplot(df.plot(x='YEAR', y=var_label).figure)
with col2:
    # Bar plot showing % change
    df['Percent Change'] = df[var_label].pct_change() * 100
    st.pyplot(df.plot(kind='bar', x='YEAR', y='Percent Change').figure)

st.write("Created by [Ari Lamstein](https://www.arilamstein.com). View the code [here](https://github.com/arilamstein/censusdis-streamlit).")