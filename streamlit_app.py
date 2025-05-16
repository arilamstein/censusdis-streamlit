import backend as be
import ui_helpers as uih
import streamlit as st
import plotly.express as px
import pandas as pd

st.header("How has your County Changed Since Covid?")

# Comparisons "since Covid" are hard-coded to the last year before Covid (2019) and the last year of data
YEAR1 = "2019"
YEAR2 = "2023"

# Let the user select data to view and how to view it
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
graph_type = st.radio("View data as: ", ["Counts", "Percent Change"], horizontal=True)

# Now display the data the user requested
county_tab, map_tab, table_tab, about_tab = st.tabs(
    ["📈 Single County", "🗺️ Map ", "📋 Table", "ℹ️ About"]
)

with county_tab:
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
        # All data for this county
        if graph_type == "Counts":
            fig = be.get_line_graph(df, var, state_name, county_name)
        elif graph_type == "Percent Change":
            df["Percent Change"] = df[var].pct_change() * 100
            fig = be.get_bar_graph(df, var, state_name, county_name)

        st.pyplot(fig)

    with col2:
        # How does this county compare to all other counties?
        ranking_df = be.get_ranking_df(var, YEAR1, YEAR2)
        st.pyplot(
            be.get_percent_change_histogram(
                ranking_df, var, YEAR1, YEAR2, state_name, county_name
            )
        )

with map_tab:
    fig = px.choropleth(
        be.get_mapping_df(var, YEAR1, YEAR2),
        geojson=be.county_map,
        locations="FIPS",
        color="Quartile",
        color_discrete_sequence=["#ffffcc", "#a1dab4", "#41b6c4", "#225ea8"],
        scope="usa",
        hover_name="County",
        hover_data={"FIPS": False, "Percent Change": True},
        labels={"Quartile": "Percent Change", "FIPS": "NAME"},
    )
    fig.update_layout(title_text=f"Percent Change of {var} between {YEAR1} and {YEAR2}")
    st.plotly_chart(fig)

with table_tab:
    ranking_df = be.get_ranking_df(var, YEAR1, YEAR2)
    ranking_text = be.get_ranking_text(
        state_name, county_name, var, ranking_df, YEAR1, YEAR2
    )

    st.write(ranking_text)

    # The styling here are things like the gradient on the "Percent Change" column
    ranking_df = ranking_df.style.pipe(
        uih.apply_styles, state_name, county_name, YEAR1, YEAR2
    )
    st.dataframe(ranking_df)

with about_tab:
    text = open("about.md").read()
    st.write(text)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "Created by [Ari Lamstein](https://www.arilamstein.com). View the code "
    + "[here](https://github.com/arilamstein/censusdis-streamlit)."
)
