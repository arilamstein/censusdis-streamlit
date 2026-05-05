import backend as be

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.figure import Figure
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


@st.cache_resource
def get_line_graph(name: str, col: str) -> Figure:
    df = be.get_census_data(name, col, True)
    df["Year"] = df["Year"].astype(int)

    # Create the figure and axis
    fig, ax = plt.subplots()

    # Define colors for consistency
    pre_covid_color = "black"
    post_covid_color = "#FF4500"  # Same saturated orange-red as in the swarm plot
    missing_color = "gray"

    # Assign dataset categories
    df["Period"] = df["Year"].apply(
        lambda x: "Pre-Covid" if x <= 2019 else "Post-Covid" if x >= 2021 else "Missing"
    )

    # Plot the data using seaborn with the updated colors
    sns.lineplot(
        data=df[df["Year"] <= 2019],
        x="Year",
        y=col,
        ax=ax,
        marker="o",
        color=pre_covid_color,
        label="Pre-Covid",
    )
    sns.lineplot(
        data=df[df["Year"] >= 2021],
        x="Year",
        y=col,
        ax=ax,
        marker="o",
        color=post_covid_color,
        label="Post-Covid",
    )

    # Handle missing 2020 connection (gray dashed line)
    if 2019 in df["Year"].values and 2021 in df["Year"].values:
        value_2019 = df.loc[df["Year"] == 2019, col].values[0]
        value_2021 = df.loc[df["Year"] == 2021, col].values[0]
        ax.plot([2019, 2021], [value_2019, value_2021], "--", color=missing_color)

    # Set custom x-axis labels
    selected_years = [2005, 2010, 2015, 2020]
    ax.set_xticks(selected_years)
    ax.set_xticklabels([str(year) for year in selected_years])

    # Formatting
    ax.set_title(f"{col}\n{name}")
    ax.legend()

    # Apply comma formatting to y-axis
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

    return fig


@st.cache_resource
def get_compare_boxplot(year1: int, year2: int, column: str) -> go.Figure:
    df = be.get_compare_df(year1, year2, column)

    fig = px.box(
        df,
        y="Percent Change",
        custom_data=["Name", "Percent Change"],
        title=f"Percent Change in {column}, {year1}-{year2}",
        points="all",
    )
    fig.update_traces(
        hovertemplate=(
            "%{customdata[0]}<br>Percent Change: %{customdata[1]:,.1f}%<extra></extra>"
        )
    )
    fig.update_layout(
        title={
            "text": f"Percent Change in {column}, {year1}-{year2}",
            "x": 0.5,
            "xanchor": "center"
        }
    )

    return fig
