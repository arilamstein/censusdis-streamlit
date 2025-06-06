import backend as be

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.express as px
import seaborn as sns
import streamlit as st


@st.cache_resource
def get_map(var, year1, year2, unit_col):
    df = be.get_mapping_df(var, year1, year2, unit_col)

    # Because we are showing percent change, it helps to use a divergent scale
    # and fix the middle color at 0. Plotly can do this for us, but by default
    # it does so in a way that forces an equal number of values on each side of
    # 0. This is a problem because our distributions are rarely symmetric around
    # 0. For example, when doing population percent change the min is -10.2 and
    # the max is 36.4. This means that using the defaults with plotly there will
    # be a lot of "red" on the legend that simply never appears on the map. This
    # will confuse people. This code uses a divergent scale (blue is positive,
    # yellow is 0, red is negative) and always pins yellow at 0. Actually using
    # the app myself, I find this to make the map feature most useful: it
    # highlights outliers and values around 0.
    cmin = df[unit_col].min()  # -10.2
    cmax = df[unit_col].max()  # 36.4
    zero_norm = abs(cmin) / (cmax - cmin)  # Determine normalized position for 0
    colorscale = [
        [0.0, "#d95f02"],  # Orange at the minimum (-10.2)
        [zero_norm, "#ffffbf"],  # Yellow exactly at 0
        [1.0, "#1b5eab"],  # Blue at the maximum (36.4)
    ]

    fig = px.choropleth(
        df,
        geojson=be.county_map,
        locations="FIPS",
        color="Percent Change",
        color_continuous_scale=colorscale,
        range_color=(cmin, cmax),
        scope="usa",
        hover_name="Full Name",
        hover_data={"FIPS": False, unit_col: True},
        labels={"Percent Change": unit_col, "FIPS": "NAME"},
    )

    # Force ticks to show min, 0 and max as labels.
    fig.update_layout(
        title_text=f"{unit_col} of {var} between {year1} and {year2}",
        coloraxis_colorbar=dict(
            title="Percent Change",
            tickmode="array",
            tickvals=[cmin, 0, cmax],
            ticktext=[f"{cmin:.1f}", "0", f"{cmax:.1f}"],
        ),
    )

    return fig


@st.cache_resource
def get_line_graph(df, var, full_name):
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
        y=var,
        ax=ax,
        marker="o",
        color=pre_covid_color,
        label="Pre-Covid",
    )
    sns.lineplot(
        data=df[df["Year"] >= 2021],
        x="Year",
        y=var,
        ax=ax,
        marker="o",
        color=post_covid_color,
        label="Post-Covid",
    )

    # Handle missing 2020 connection (gray dashed line)
    if 2019 in df["Year"].values and 2021 in df["Year"].values:
        value_2019 = df.loc[df["Year"] == 2019, var].values[0]
        value_2021 = df.loc[df["Year"] == 2021, var].values[0]
        ax.plot([2019, 2021], [value_2019, value_2021], "--", color=missing_color)

    # Set custom x-axis labels
    selected_years = [2005, 2010, 2015, 2020]
    ax.set_xticks(selected_years)
    ax.set_xticklabels(selected_years)

    # Formatting
    ax.set_title(f"{var}\n{full_name}")
    ax.legend()

    # Apply comma formatting to y-axis
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

    return fig


def get_swarm_dot_size(var):
    """Due to the size of the dataset, the swarm plots sometimes have points that cannot be placed.
    The solution is to reduce the size of the points, which we do here. The default size is 4.
    """
    if var == "Total With Public Assistance":
        return 2
    elif var == "Total Population":
        return 3
    return 4


@st.cache_resource
def get_swarmplot(df, var, year1, year2, full_name, unit_col):
    fig, ax = plt.subplots()

    # Define colors for better contrast
    normal_color = "black"
    normal_alpha = 0.3  # Lower alpha for background points
    highlight_color = "#FF4500"  # More saturated orange-red for emphasis

    # Identify the selected county
    df_black = df[df["Full Name"] != full_name]
    df_highlight = df[df["Full Name"] == full_name]

    # Adjust marker size to reduce placement issues
    size = get_swarm_dot_size(var)

    # Plot swarm plot with adjusted alpha for non-highlighted counties
    sns.swarmplot(
        x=df_black[unit_col], color=normal_color, size=size, alpha=normal_alpha, ax=ax
    )

    # If the highlighted county exists, plot it separately with enhanced visibility
    if not df_highlight.empty:
        sns.swarmplot(
            x=df_highlight[unit_col], color=highlight_color, size=8, ax=ax
        )  # Larger size and vivid color

        # Manually set the legend with the correct color
        legend_patch = plt.Line2D(
            [0],
            [0],
            marker="o",
            color=highlight_color,
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
