import streamlit as st
import plotly.express as px
import backend as be

@st.cache_data
def get_census_data(state_name, county_name, var_table, var_label):
    return be.get_census_data(state_name, county_name, var_table, var_label)

st.header('Selected County Demographics (2022)')

# State index 4 is California, and county index 37 is San Francisco
state_name = st.selectbox("Select a State:", be.get_state_names(), index=4) 
county_name = st.selectbox("Select a County:", be.get_county_names(state_name))

# var_label is something human readable like 'Median Household Income'
# var_table is the actual table in the Census Bureau that contains the data (e.g. 'B19013_001E')
var_label = st.selectbox("Select a demographic", be.census_vars.keys())
var_table = be.census_vars[var_label]

# We need all 4 pieces of information to get the data we want to visualize
df = get_census_data(state_name, county_name, var_table, var_label)

col1, col2 = st.columns(2)

# Column 1 is a simple table
with col1:
    df = df.sort_values(var_label, ascending=False)
    st.dataframe(df[['County', var_label]], hide_index=True)

# Column 2 is a choropleth map
with col2:
    df = df.set_index('County')
    fig = px.choropleth(df, geojson=df.geometry, locations=df.index, 
                        color=var_label, color_continuous_scale="Viridis",
                        projection="mercator")
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig)

st.write("Created by [Ari Lamstein](https://www.arilamstein.com). View the code [here](https://github.com/arilamstein/censusdis-streamlit).")
