import backend as be
import ui_helpers as uih
import streamlit as st
import plotly.express as px
import pandas as pd

st.header("How has your County Changed Since Covid?")

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

# At one point the app was designed to let people toggle between viewing Count data vs. Percent Change data, and
# also change which years they used to compare when looking at percent change calculations.
# All the graphing functions still maintain that flexibility. But I'm now experimenting with hard-coding both
# of these variables
display_col = "Percent Change"
YEAR1 = "2019"
YEAR2 = "2023"

# Now display the data the user requested
county_tab, table_tab, map_tab, about_tab = st.tabs(
    ["📈 Graphs", "📋 Table", "🗺️ Map ", "ℹ️ About"]
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
        # Time Series graph data for this county, for the given variable
        fig = be.get_line_graph(df, var, state_name, county_name)
        st.pyplot(fig)

    with col2:
        # How does this county compare to all other counties?
        ranking_df = be.get_ranking_df(var, YEAR1, YEAR2, display_col)
        fig = be.get_boxplot(
            ranking_df, var, YEAR1, YEAR2, state_name, county_name, display_col
        )
        st.pyplot(fig)

with table_tab:
    ranking_df = be.get_ranking_df(var, YEAR1, YEAR2, display_col)
    ranking_text = be.get_ranking_text(
        state_name, county_name, var, ranking_df, YEAR1, YEAR2, display_col
    )

    st.markdown(ranking_text, unsafe_allow_html=True)

    # The styling here are things like the gradient on the column the user selected
    ranking_df = ranking_df.style.pipe(
        uih.apply_styles, state_name, county_name, YEAR1, YEAR2, display_col
    )
    st.dataframe(ranking_df)

with map_tab:
    fig = px.choropleth(
        be.get_mapping_df(var, YEAR1, YEAR2, display_col),
        geojson=be.county_map,
        locations="FIPS",
        color="Quartile",
        color_discrete_sequence=["#ffffcc", "#a1dab4", "#41b6c4", "#225ea8"],
        scope="usa",
        hover_name="County",
        hover_data={"FIPS": False, display_col: True},
        labels={"Quartile": display_col, "FIPS": "NAME"},
    )
    fig.update_layout(title_text=f"{display_col} of {var} between {YEAR1} and {YEAR2}")
    st.plotly_chart(fig)

with about_tab:
    text = open("about.md").read()
    st.write(text)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "Created by [Ari Lamstein](https://www.arilamstein.com). View the code "
    + "[here](https://github.com/arilamstein/censusdis-streamlit)."
)
