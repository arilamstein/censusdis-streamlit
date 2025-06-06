import backend as be
import visualizations as viz
import ui_helpers as uih
import data.census_vars as cv
import streamlit as st

st.set_page_config(layout="wide")
st.header("How has America Changed Since Covid?")
st.write(open("text/intro.md").read())

# Let the user select data to view and how to view it
state_col, county_col, demographic_col = st.columns(3)
with state_col:
    state = st.selectbox("State:", be.get_states(), index=4)  # 4 = California
    county_index = uih.get_county_index(state)
with county_col:
    county = st.selectbox("County:", be.get_counties(state), index=county_index)
    full_name = ", ".join([county, state])
with demographic_col:
    var = st.selectbox("Demographic:", cv.census_dropdown_values)

# At one point the app let people toggle between viewing Count data vs. Percent Change data. It also let users
# change which years they used to compare when looking at percent change calculations.
# The graphing functions still maintain that flexibility. But I now hard-code these variables.
unit_col = "Percent Change"
YEAR1 = "2019"
YEAR2 = "2023"

# Now display the data the user requested
graph_tab, table_tab, map_tab, about_tab = st.tabs(
    ["📈 Graphs", "🔍 Table", "🗺️ Map ", "ℹ️ About"]
)

with graph_tab:
    df = be.get_census_data(full_name, var, True)

    line_graph, swarm_plot = st.columns(2)

    with line_graph:
        # Time Series graph data for this county, for the given variable
        fig = viz.get_line_graph(df, var, full_name)
        st.pyplot(fig)
        st.write("*Dashed line indicates that data is missing for 2020.*")

    with swarm_plot:
        # How does the change this county experienced compare to the change in all other counties?
        ranking_df = be.get_ranking_df(var, YEAR1, YEAR2, unit_col)
        fig = viz.get_swarmplot(ranking_df, var, YEAR1, YEAR2, full_name, unit_col)
        st.pyplot(fig)
        text = open("text/swarmplot.md").read().format(var=var)
        st.write(f"{text}")

with table_tab:
    ranking_df = be.get_ranking_df(var, YEAR1, YEAR2, unit_col)
    ranking_text = be.get_ranking_text(full_name, var, ranking_df)

    # The styling here are things like the gradient on the column the user selected
    ranking_df = ranking_df.style.pipe(
        uih.apply_styles, full_name, YEAR1, YEAR2, unit_col
    )

    text = (
        open("text/table.md")
        .read()
        .format(var=var, year1=YEAR1, year2=YEAR2, ranking_text=ranking_text)
    )
    st.markdown(text)

    st.dataframe(ranking_df)

with map_tab:
    text = open("text/map.md").read().format(var=var)
    st.write(text)
    fig = viz.get_map(var, YEAR1, YEAR2, unit_col)
    st.plotly_chart(fig)

with about_tab:
    st.write(open("text/about.md").read())
