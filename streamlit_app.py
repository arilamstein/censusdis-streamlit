import backend as be
import visualizations as viz
import streamlit as st
from scripts.census_vars import census_vars_2005

# st.set_page_config(layout="wide")
st.title("How has America Changed Since Covid?")
st.write(open("text/intro.md").read())

col1, col2 = st.columns(2)
with col1:  # Location
    location_options = be.get_all_names()
    location = st.selectbox(
        "Location:",
        options=location_options,
        placeholder="Search for a place...",
        index=None,
    )
    if location is None:
        location = "United States"

with col2:  # Demographic
    first_option = "Total Worked from Home"
    options = [first_option] + [
        v for v in census_vars_2005.values() if v not in ("Name", first_option)
    ]

    column = st.selectbox(
        "Demographic:",
        options=options,
    )

fig = viz.get_line_graph(location, column)
st.pyplot(fig)
st.write("*Dashed line indicates that data is missing for 2020.*")
