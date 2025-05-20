import backend as be

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.express as px
import seaborn as sns


def get_map(var, year1, year2, unit_col):
    fig = px.choropleth(
        be.get_mapping_df(var, year1, year2, unit_col),
        geojson=be.county_map,
        locations="FIPS",
        color="Quartile",
        color_discrete_sequence=["#ffffcc", "#a1dab4", "#41b6c4", "#225ea8"],
        scope="usa",
        hover_name="County",
        hover_data={"FIPS": False, unit_col: True},
        labels={"Quartile": unit_col, "FIPS": "NAME"},
    )
    fig.update_layout(title_text=f"{unit_col} of {var} between {year1} and {year2}")

    return fig


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

def get_swarmplot(df, var, year1, year2, state_name, county_name, unit_col):
    fig, ax = plt.subplots()

    # Define the full county name
    full_name = f"{county_name}, {state_name}"

    # Create a new column to control coloring
    df["Highlight"] = [
        "orange" if county == full_name else "black" for county in df["County"]
    ]

    # Create swarm plot, using hue to differentiate colors
    ax = sns.swarmplot(
        x=df[unit_col],
        hue=df["Highlight"],
        palette={"black": "black", "orange": "orange"},
        size=4,
    )

    # Remove the default hue-based legend.
    # And if the selected county is not in the dataset, remove mention of it from the legend
    handles, labels = ax.get_legend_handles_labels()
    if len(handles) > 1:
        ax.legend([handles[1]], [full_name])  # Keep only the highlighted county
    else:
        ax.legend_.remove() # Selected county not in dataset - remove entire legend

    ax.set_title(f"{unit_col} of {var}\nAll Counties, {year1} to {year2}")
    ax.set_xlabel(unit_col)

    # Apply comma formatting to the x-axis
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

    return fig
