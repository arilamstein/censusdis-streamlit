import backend as be

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.express as px
import seaborn as sns
import streamlit as st


@st.cache_resource
def get_map(var, year1, year2, unit_col):
    fig = px.choropleth(
        be.get_mapping_df(var, year1, year2, unit_col),
        geojson=be.county_map,
        locations="FIPS",
        color="Quartile",
        color_discrete_sequence=[
            "#a1dab4",
            "#41b6c4",
            "#225ea8",
            "#081d58",
        ],  # Light for low, dark for high
        scope="usa",
        hover_name="County",
        hover_data={"FIPS": False, unit_col: True},
        labels={"Quartile": unit_col, "FIPS": "NAME"},
    )
    fig.update_layout(title_text=f"{unit_col} of {var} between {year1} and {year2}")

    return fig


@st.cache_resource
def get_line_graph(df, var, state_name, county_name):
    df["YEAR"] = df["YEAR"].astype(int)

    # Create the figure and axis
    fig, ax = plt.subplots()

    # Assign dataset categories
    df["Period"] = df["YEAR"].apply(
        lambda x: "Pre-Covid" if x <= 2019 else "Post-Covid" if x >= 2021 else "Missing"
    )

    # Plot the data using seaborn
    sns.lineplot(
        data=df[df["YEAR"] <= 2019],
        x="YEAR",
        y=var,
        ax=ax,
        marker="o",
        color="black",
        label="Pre-Covid",
    )
    sns.lineplot(
        data=df[df["YEAR"] >= 2021],
        x="YEAR",
        y=var,
        ax=ax,
        marker="o",
        color="orange",
        label="Post-Covid",
    )

    # Handle missing 2020 connection (gray dashed line)
    if 2019 in df["YEAR"].values and 2021 in df["YEAR"].values:
        value_2019 = df.loc[df["YEAR"] == 2019, var].values[0]
        value_2021 = df.loc[df["YEAR"] == 2021, var].values[0]
        ax.plot([2019, 2021], [value_2019, value_2021], "--", color="gray")

    # Set custom x-axis labels
    selected_years = [2005, 2010, 2015, 2020]
    ax.set_xticks(selected_years)
    ax.set_xticklabels(selected_years)

    # Formatting
    ax.set_title(f"{var}\n{county_name}, {state_name}")
    ax.legend()

    # Apply comma formatting to y-axis
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

    return fig


@st.cache_resource
def get_swarmplot(df, var, year1, year2, state_name, county_name, unit_col):
    fig, ax = plt.subplots()

    # If the selected county is in the dataset, we want to render it separately.
    # That allows us to make it 2x larger and a different color
    full_name = f"{county_name}, {state_name}"
    df_black = df[df["County"] != full_name]
    df_highlight = df[df["County"] == full_name]

    # Plot swarm plot with only black points (excluding the highlighted county)
    # The values for "Total With Public Assistance" cluster around low values, so with size=4 we get the warning:
    # "41.6% of the points cannot be placed; you may want to decrease the size of the markers or use stripplot."
    # This conditional resizing makes that warning go away.
    size = 2 if var == "Total With Public Assistance" else 4
    sns.swarmplot(x=df_black[unit_col], color="black", size=size, ax=ax)

    # If the highlighted county exists, plot it separately in orange
    if not df_highlight.empty:
        sns.swarmplot(
            x=df_highlight[unit_col], color="orange", size=8, ax=ax
        )  # Larger size for visibility

        # Manually set the legend with the correct color
        legend_patch = plt.Line2D(
            [0],
            [0],
            marker="o",
            color="orange",
            markersize=8,
            label=full_name,
            linestyle="None",
        )
        ax.legend(handles=[legend_patch])  # Only add legend if the county exists

    ax.set_title(f"{unit_col} of {var}\nAll Counties, {year1} to {year2}")
    ax.set_xlabel(unit_col)

    # Apply comma formatting to the x-axis
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

    return fig
