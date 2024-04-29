import backend as be
import streamlit as st
import matplotlib.pyplot as plt

st.header('Census Covid Explorer')
st.write('This goal of this app is to shine a light on how US Demographics changed as a result of Covid-19. The app is still under development. Data comes from the American Community Survey 1-year estimates.')

# State index 4 is California
state_name = st.selectbox("Select a State:", be.get_state_names(), index=4)
county_name_index = 0
if state_name == "California":
    county_name_index = 25 # San Francisco
elif state_name == "New York":
    county_name_index = 15 # New York
county_name = st.selectbox("Select a County:", be.get_county_names(state_name), index=county_name_index)

# var_label is something human readable like 'Median Household Income'
# var_table is the actual table in the Census Bureau that contains the data (e.g. 'B19013_001E')
var_label = st.selectbox("Select a demographic", be.census_vars.keys())

# We need 3 pieces of information to get the data we want to visualize
df = be.get_census_data(state_name, county_name, var_label)

col1, col2 = st.columns(2)

# Column 1 is a bar plot showing % change
with col1:
    df['Percent Change'] = df[var_label].pct_change() * 100
    st.pyplot(df.plot(kind='bar', x='YEAR', y='Percent Change').figure)

# Column 2 is a line graph 
with col2:
    st.pyplot(df.plot(x='YEAR', y=var_label).figure)

st.write("Created by [Ari Lamstein](https://www.arilamstein.com). View the code [here](https://github.com/arilamstein/censusdis-streamlit).")