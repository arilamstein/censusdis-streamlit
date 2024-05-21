import backend as be
import streamlit as st
import matplotlib.pyplot as plt

st.header('How did your County Change During Covid?')

# Set up nice defaults for the various UI elements
state_col, county_col = st.columns(2)
with state_col:
    state_name = st.selectbox("State:", be.get_state_names(), index=4) # 4 = California
    county_name_index = 0
    if state_name == "California":
        county_name_index = 25 # San Francisco
    elif state_name == "New York":
        county_name_index = 15 # New York (Manhattan)

with county_col:
    county_name = st.selectbox("County:", be.get_county_names(state_name), index=county_name_index)

# Something like "Total Population"
var = st.selectbox("Demographic:", be.get_unique_census_labels())

tab1, tab2, tab3 = st.tabs(["📈 County Details", "🥇 National Rankings", "ℹ️ About"])

with tab1:
    st.write(f"All data for {county_name}, {state_name} for {var}. Data was not published for 2020.")

    # Get and chart data
    df = be.get_census_data(state_name, county_name, var)
    col1, col2 = st.columns(2)
    with col1:
        # Line graph of raw data
        st.pyplot(df.plot(x='YEAR', y=var).figure)
    with col2:
        # Bar plot showing % change
        df['Percent Change'] = df[var].pct_change() * 100
        st.pyplot(df.plot(kind='bar', x='YEAR', y='Percent Change').figure)

with tab2:
    st.write("Here's how the counties ranked in terms of percent change between 2019-2021.")
    st.dataframe(be.get_ranking_df(var))

with tab3:
    st.write("All data comes from the American Community Survey (ACS) 1-year estimates.")

st.write("Created by [Ari Lamstein](https://www.arilamstein.com). View the code [here](https://github.com/arilamstein/censusdis-streamlit).")