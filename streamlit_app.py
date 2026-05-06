import streamlit as st

import backend as be
import ui
import visualizations as viz

st.title("How has America Changed Since Covid?")
with open("text/intro.md") as intro_file:
    st.write(intro_file.read())

line_tab, compare_tab, table_tab, about_tab = st.tabs(
    ["📈 Trends", "🔍 Compare Years", "📋 All Data", "ℹ️ About"]
)
with line_tab:
    location, column = ui.location_and_demographic_block("line")

    fig = viz.get_line_graph(location, column)
    st.plotly_chart(fig)

with compare_tab:
    years = be.get_years()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        location = ui.location_selector("compare")
    with col2:
        column = ui.demographic_selector("compare")
    with col3:
        year1 = st.selectbox("First Year:", years, years.index(2019))
    with col4:
        year2 = st.selectbox("Second Year:", years, years.index(2021))

    fig = viz.get_compare_violinplot(year1, year2, column, location)
    st.plotly_chart(fig)

    df = be.get_compare_df_styled(year1, year2, column)
    st.dataframe(df, hide_index=True)

with table_tab:
    df = be.get_table_df_styled()
    st.dataframe(df, hide_index=True)

with about_tab, open("text/about.md") as about_file:
    st.write(about_file.read())
