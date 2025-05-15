import backend as be
import ui_helpers as uih
import streamlit as st
import plotly.express as px
import pandas as pd

st.header("How has your County Changed Since Covid?")

# Let the user select a (state, county, demographic) combination to get data on
state_col, county_col, demographic_col = st.columns(3)
with state_col:
    state_name = st.selectbox("State:", be.get_state_names(), index=4)  # 4 = California
    county_name_index = uih.get_county_name_index(state_name)
with county_col:
    county_name = st.selectbox(
        "County:", be.get_county_names(state_name), index=county_name_index
    )
with demographic_col:
    var = st.selectbox("Demographic:", be.get_unique_census_labels())

# Now display the data the user requested
tab1, tab2, tab3 = st.tabs(["📈 Single County", "🥇 County Comparison", "ℹ️ About"])

# Tab 1: Time series data on selected county / demographic combination
with tab1:
    df = be.get_census_data(state_name, county_name, var)

    # Add in NA data for 2020 because having the time series jump from 2019 to 2021
    # with no space in between looks odd.
    row_for_2020 = pd.DataFrame(
        [
            {
                "STATE_NAME": df.iloc[0]["STATE_NAME"],
                "COUNTY_NAME": df.iloc[0]["COUNTY_NAME"],
                "YEAR": "2020",
            }
        ]
    )
    df = pd.concat([df, row_for_2020])
    df = df.sort_values(["STATE_NAME", "COUNTY_NAME", "YEAR"])

    col1, col2 = st.columns(2)
    with col1:
        fig = be.get_line_graph(df, var, state_name, county_name)
        st.pyplot(fig)

    with col2:
        # Bar plot showing % change
        df["Percent Change"] = df[var].pct_change() * 100
        fig = be.get_bar_graph(df, var, state_name, county_name)
        st.pyplot(fig)

# Tab 2: Ranking of all counties for that demographic
with tab2:
    # Let the user selecting years to compare when ranking how counties changed.
    # The ACS 1-year estimates are available for each year since 2005 with the exception of 2020.
    years = [str(year) for year in range(2005, 2023 + 1) if year != 2020]
    col1, col2 = st.columns(2)
    with col1:
        year1 = st.selectbox("Starting Year:", years, index=14)
    with col2:
        year2 = st.selectbox("Ending Year:", years, index=17)

    ranking_df = be.get_ranking_df(var, year1, year2)
    ranking_text = be.get_ranking_text(
        state_name, county_name, var, ranking_df, year1, year2
    )

    st.write(ranking_text)

    subtab = st.radio("Choose a visualization:", ["Histogram", "Table", "Map"])
    if subtab == "Histogram":
        st.pyplot(be.get_percent_change_histogram(ranking_df, var, year1, year2))
    elif subtab == "Table":
        # The styling here are things like the gradient on the "Percent Change" column
        ranking_df = ranking_df.style.pipe(
            uih.apply_styles, state_name, county_name, year1, year2
        )
        st.dataframe(ranking_df)
    elif subtab == "Map":
        fig = px.choropleth(
            be.get_mapping_df(var, year1, year2),
            geojson=be.county_map,
            locations="FIPS",
            color="Quartile",
            color_discrete_sequence=["#ffffcc", "#a1dab4", "#41b6c4", "#225ea8"],
            scope="usa",
            hover_name="County",
            hover_data={"FIPS": False, "Percent Change": True},
            labels={"Quartile": "Percent Change", "FIPS": "NAME"},
        )
        st.plotly_chart(fig)

with tab3:
    text = open("about.md").read()
    st.write(text)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "Created by [Ari Lamstein](https://www.arilamstein.com). View the code "
    + "[here](https://github.com/arilamstein/censusdis-streamlit)."
)
