import backend as be
import ui_helpers as uih
import streamlit as st
import matplotlib
import plotly.express as px

st.header("How did your County Change During Covid?")

# Let the user select a (state, county, demographic) combination to get data on
# State and County dropdowns appear side by side
state_col, county_col = st.columns(2)
with state_col:
    state_name = st.selectbox("State:", be.get_state_names(), index=4)  # 4 = California
    county_name_index = uih.get_county_name_index(state_name)
with county_col:
    county_name = st.selectbox(
        "County:", be.get_county_names(state_name), index=county_name_index
    )

# Demographic statistic dropdown appears below
var = st.selectbox(
    "Demographic:", be.get_unique_census_labels()
)  # Something like "Total Population"

# Now display the data the user requested
tab1, tab2, tab3, tab4 = st.tabs(["📈 Details", "🥇 Rankings", "🗺️ Map", "ℹ️ About"])

# Tab 1: Time series data on selected county / demographic combination
with tab1:
    st.write(f"All data for **{county_name}, {state_name}** for **{var}**.")
    df = be.get_census_data(state_name, county_name, var)

    col1, col2 = st.columns(2)
    with col1:
        # Line graph of raw data. Set y-axis formatter to use commas
        fig = df.plot(x="YEAR", y=var, style="-o").figure
        fig.gca().get_yaxis().set_major_formatter(
            matplotlib.ticker.StrMethodFormatter("{x:,.0f}")
        )
        st.pyplot(fig)
    with col2:
        # Bar plot showing % change
        df["Percent Change"] = df[var].pct_change() * 100
        st.pyplot(df.plot(kind="bar", x="YEAR", y="Percent Change").figure)

# Tab 2: Ranking of all counties for that demographic (2019-2021)
with tab2:
    ranking_df = be.get_ranking_df(var)
    ranking_text = be.get_ranking_text(state_name, county_name, var, ranking_df)

    st.write(ranking_text)
    # The styling here are things like the gradient on the "Percent Change" column
    ranking_df = ranking_df.style.pipe(uih.apply_styles, state_name, county_name)
    st.dataframe(ranking_df)

# Tab 3: Choropleth map
with tab3:
    st.write("Data is provided only for counties with a population of at least 65,000.")
    fig = px.choropleth(
        be.get_mapping_df(var),
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

# Tab 4: Info about the data / app
with tab4:
    text = open("about.md").read()
    st.write(text)

st.write(
    "Created by [Ari Lamstein](https://www.arilamstein.com). View the code " +
    "[here](https://github.com/arilamstein/censusdis-streamlit)."
)
