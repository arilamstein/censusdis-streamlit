import backend as be
import streamlit as st
import plotly.express as px
import seaborn as sns

@st.cache_data
def get_census_data(state_name, county_name, var_table, var_label):
    return be.get_census_data(state_name, county_name, var_table, var_label)

st.header('Census Tract Demographics (2022)')

# State index 4 is California, and county index 37 is San Francisco
state_name = st.selectbox("Select a State:", be.get_state_names(), index=4)
county_name_index = 37 if state_name == "California" else 0
county_name = st.selectbox("Select a County:", be.get_county_names(state_name), index=county_name_index)

# var_label is something human readable like 'Median Household Income'
# var_table is the actual table in the Census Bureau that contains the data (e.g. 'B19013_001E')
var_label = st.selectbox("Select a demographic", be.census_vars.keys())
var_table = be.census_vars[var_label]

# We need all 4 pieces of information to get the data we want to visualize
df = get_census_data(state_name, county_name, var_table, var_label)

col1, col2 = st.columns(2)

# Column 1 is a simple histogram
with col1:
    plot = sns.boxplot(data=df, y=var_label)
    st.pyplot(plot.figure)

# Column 2 is a choropleth map
with col2:
    df = df.set_index('NAME')
    fig = px.choropleth_mapbox(df, 
                               geojson=df.geometry,
                               hover_data={var_label:be.get_hover_data_for_var_label(var_label)},
                               locations=df.index, 
                               center=be.get_df_center_lat_lon(df), 
                               color=var_label, 
                               color_continuous_scale="Viridis", 
                               mapbox_style="carto-positron", 
                               opacity=0.5,
                               zoom=10)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

st.write("Created by [Ari Lamstein](https://www.arilamstein.com). View the code [here](https://github.com/arilamstein/censusdis-streamlit).")