import backend as be
import visualizations as viz
import streamlit as st
import ui

# st.set_page_config(layout="wide")
st.title("How has America Changed Since Covid?")
st.write(open("text/intro.md").read())

line_tab, compare_tab, table_tab, about_tab = st.tabs(
    ["📈 Graph", "🔍 Compare Years", "📋 All Data", "ℹ️ About"]
)
with line_tab:
    location, column = ui.location_and_demographic_block("line")

    fig = viz.get_line_graph(location, column)
    st.plotly_chart(fig)
    st.write("*Dashed line indicates that data is missing for 2020.*")

with compare_tab:
    years = be.get_years()
    col1, col2, col3 = st.columns(3)
    with col1:
        column = ui.demographic_selector("compare")
    with col2:
        year1 = st.selectbox("First Year:", years, years.index(2019))
    with col3:
        year2 = st.selectbox("Second Year:", years, years.index(2021))

    fig = viz.get_compare_boxplot(year1, year2, column)
    st.plotly_chart(fig)

    df = be.get_compare_df_styled(year1, year2, column)
    st.dataframe(df, hide_index=True)

with table_tab:
    df = be.get_table_df_styled()
    st.dataframe(df, hide_index=True)

with about_tab:
    st.write(open("text/about.md").read())
