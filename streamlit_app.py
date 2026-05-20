import streamlit as st

import backend as be
import ui
import visualizations as viz

st.title("How has Covid changed America?")
st.write("Explore how US demographics have changed since Covid.")

trend_tab, compare_tab, ranking_tab, about_tab = st.tabs(
    ["📈 Trend", "🔍 Compare Years", "🏆 Ranking", "ℹ️ About"]
)
with trend_tab:
    location, column = ui.location_and_demographic_block("trend")

    fig = viz.get_line_graph(location, column)
    st.plotly_chart(fig)

    df = be.get_trend_df_styled(location, column)
    st.dataframe(df, hide_index=True)


with compare_tab:
    years = be.get_years()
    col1, col2, col3, col4 = st.columns([35, 35, 15, 15])
    with col1:
        location = ui.location_selector("compare")
    with col2:
        column = ui.demographic_selector("compare")
    with col3:
        year1 = st.selectbox("First Year:", years, years.index(2019))
    with col4:
        year2 = st.selectbox("Second Year:", years, years.index(2021))

    fig = viz.get_compare_scatterplot(year1, year2, column, location)
    st.plotly_chart(fig)

    with open("text/table.md") as table_file:
        st.write(table_file.read().format(var=column, year1=year1, year2=year2))

    df = be.get_compare_df_styled(year1, year2, column)
    st.dataframe(df, hide_index=True)

with ranking_tab:
    years = be.get_years()
    col1, col2, col3 = st.columns([40, 40, 20])
    with col1:
        location = ui.location_selector("ranking")
    with col2:
        options = be.get_demographic_statistics()
        column = st.selectbox(
            "Demographic:",
            options=options,
            index=options.index("Median Household Income"),
        )

    with col3:
        year = st.selectbox("Year:", years, len(years) - 1)

    col_n, col_s, col_c, col_p = st.columns(4)
    with col_n:
        include_nation = st.checkbox("Nation", True)
    with col_s:
        include_states = st.checkbox("States", True)
    with col_c:
        include_counties = st.checkbox("Counties", True)
    with col_p:
        include_places = st.checkbox("Cities", True)

    if sum([include_nation, include_states, include_counties, include_places]) == 0:
        st.warning("Please select at least one region.")
    else:
        fig = viz.get_single_year_scatterplot(
            year,
            column,
            location,
            include_nation,
            include_states,
            include_counties,
            include_places,
        )
        st.plotly_chart(fig)

        df = be.get_table_df_styled(
            year,
            column,
            include_nation,
            include_states,
            include_counties,
            include_places,
        )
        st.dataframe(df, hide_index=True)

with about_tab, open("text/about.md") as about_file:
    st.write(about_file.read())
