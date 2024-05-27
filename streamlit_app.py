import backend as be
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

st.header('How did your County Change During Covid?')

# Set up nice defaults for the various UI elements
state_col, county_col = st.columns(2)
with state_col:
    state_name = st.selectbox("State:", be.get_state_names(), index=4) # 4 = California
    county_name_index = 0
    if state_name == "California":
        county_name_index = 24 # San Francisco
    elif state_name == "New York":
        county_name_index = 15 # New York (Manhattan)

with county_col:
    county_name = st.selectbox("County:", be.get_county_names(state_name), index=county_name_index)

# Something like "Total Population"
var = st.selectbox("Demographic:", be.get_unique_census_labels())

tab1, tab2, tab3, tab4 = st.tabs(["📈 Details", "🥇 Rankings", "🗺️ Map", "ℹ️ About"])

with tab1:
    st.write(f"All data for **{county_name}, {state_name}** for **{var}**.")

    # Get and chart data
    df = be.get_census_data(state_name, county_name, var)
    col1, col2 = st.columns(2)
    with col1:
        # Line graph of raw data
        st.pyplot(df.plot(x='YEAR', y=var, style='-o').figure)
    with col2:
        # Bar plot showing % change
        df['Percent Change'] = df[var].pct_change() * 100
        st.pyplot(df.plot(kind='bar', x='YEAR', y='Percent Change').figure)

with tab2:
    ranking_df = be.get_ranking_df(var)
    st.write(be.get_ranking_text(state_name, county_name, var, ranking_df))
    st.dataframe(ranking_df)

with tab3:
    st.write("Data is provided only for counties with a population of at least 65,000.")          
    fig = px.choropleth(be.get_mapping_df(var), geojson=be.county_map, locations='FIPS', color='Quartile',
                        color_discrete_sequence = ['#ffffcc','#a1dab4','#41b6c4','#225ea8'],
                        scope="usa",
                        hover_name='County',
                        hover_data={'FIPS': False, 'Percent Change': True},
                        labels={'Quartile':'Percent Change', 'FIPS': 'NAME'})
    st.plotly_chart(fig)

with tab4:
    text = open('about.md').read()
    st.write(text)

st.write("Created by [Ari Lamstein](https://www.arilamstein.com). View the code [here](https://github.com/arilamstein/censusdis-streamlit).")