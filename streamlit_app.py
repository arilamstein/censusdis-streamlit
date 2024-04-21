import backend as be
import streamlit as st
import plotly.express as px
import seaborn as sns

st.header('Census Covid Explorer')

# State index 4 is California, and county index 37 is San Francisco
state_name = st.selectbox("Select a State:", be.get_state_names(), index=4)
county_name_index = 25 if state_name == "California" else 0
county_name = st.selectbox("Select a County:", be.get_county_names(state_name), index=county_name_index)

# var_label is something human readable like 'Median Household Income'
# var_table is the actual table in the Census Bureau that contains the data (e.g. 'B19013_001E')
var_label = st.selectbox("Select a demographic", be.census_vars.keys())
#var_table = be.census_vars[var_label]

# We need all 4 pieces of information to get the data we want to visualize
df = be.get_census_data(state_name, county_name, var_label)

st.dataframe(df)

st.pyplot(df.plot(x='YEAR', y=var_label).figure)

st.write("Created by [Ari Lamstein](https://www.arilamstein.com). View the code [here](https://github.com/arilamstein/censusdis-streamlit).")