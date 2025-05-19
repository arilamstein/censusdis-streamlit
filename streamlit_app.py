import backend as be
import visualizations as viz
import ui_helpers as uih
import streamlit as st

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
    df = be.get_census_data(state_name, county_name, var, True)

    col1, col2 = st.columns(2)
    with col1:
        # Time Series graph data for this county, for the given variable
        fig = viz.get_line_graph(df, var, state_name, county_name)
        st.pyplot(fig)

    with col2:
        # How does this county compare to all other counties?
        ranking_df = be.get_ranking_df(var, YEAR1, YEAR2, display_col)
        fig = viz.get_violinplot(
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
    fig = viz.get_map(var, YEAR1, YEAR2, display_col)
    st.plotly_chart(fig)

with about_tab:
    text = open("about.md").read()
    st.write(text)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "Created by [Ari Lamstein](https://www.arilamstein.com). View the code "
    + "[here](https://github.com/arilamstein/censusdis-streamlit)."
)
