import pandas as pd
import numpy as np
from census_vars import census_vars
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches

df = pd.read_csv("county_data.csv", dtype={"FIPS": str, "YEAR": str})
with open("county_map.json", "r") as read_file:
    county_map = json.load(read_file)


def get_state_names():
    return df["STATE_NAME"].unique()


def get_county_names(state_name):
    return df.loc[df["STATE_NAME"] == state_name]["COUNTY_NAME"].sort_values().unique()


def get_census_data(state_name, county_name, var):
    return df.loc[
        (df["STATE_NAME"] == state_name) & (df["COUNTY_NAME"] == county_name)
    ][["STATE_NAME", "COUNTY_NAME", "YEAR", var]]


# This code is hard to read but it serves a purpose.
# In short: the order in which census_vars lists the variables is the order
# in which I want them to appear in the dropdown. The issue is that they contain
# duplicates due to the variable for "Work From Home" changing name throughtout
# the years. This code removes the duplicates while retaining the initial ordering,
# and prevents me from needing to duplicate data here.
# See: https://stackoverflow.com/a/17016257/2518602
def get_unique_census_labels():
    return list(dict.fromkeys(census_vars.values()))


def get_ranking_df(column, year1, year2, display_col):
    df2 = df.copy()  # We don't want to modify the global variable

    # Select just the rows and columns we need
    df2 = df2.loc[(df2["YEAR"] == year1) | (df2["YEAR"] == year2)]
    df2 = df2[["STATE_NAME", "COUNTY_NAME", "YEAR", column]]

    # Combine state and county into a single column
    df2 = df2.assign(County=lambda x: x.COUNTY_NAME + ", " + x.STATE_NAME)
    df2 = df2.drop(columns=["STATE_NAME", "COUNTY_NAME"])

    # Pivot for structure we need, calculate change and percent change, sort
    df2 = df2.pivot_table(index="County", columns="YEAR", values=column)
    df2["Change"] = df2[year2] - df2[year1]
    df2["Percent Change"] = (df2[year2] - df2[year1]) / df2[year1] * 100
    df2["Percent Change"] = df2["Percent Change"].round(1)
    df2 = df2.sort_values(display_col, ascending=False)

    # Drop Columns with Infinite percent change (first or last year has 0)
    df2 = df2.replace([np.inf, -np.inf], np.nan).dropna()
    # Create an index called "Rank"
    df2["Rank"] = list(range(1, len(df2.index) + 1))
    df2 = df2.reset_index().set_index("Rank")

    return df2


def get_ranking_text(state, county, var, ranking_df, year1, year2, display_col):
    full_name = ", ".join([county, state])

    if full_name not in list(ranking_df["County"]):
        return f"**{full_name}** does not have a ranking for **{var}**."

    rank = ranking_df[ranking_df["County"] == full_name].index.tolist()[0]

    num_counties = len(ranking_df.index)

    return (
        f"{full_name} ranks **{rank} of {num_counties}** for {display_col} in {var} "
        f"between {year1} and {year2}."
    )


def get_mapping_df(column, year1, year2, display_col):
    df2 = df.copy()  # We don't want to modify the global variable

    # Select just the rows and columns we need
    df2 = df2.loc[(df2["YEAR"] == year1) | (df2["YEAR"] == year2)]
    df2 = df2[["FIPS", "STATE_NAME", "COUNTY_NAME", "YEAR", column]]

    # Combine state and county into a single column
    df2 = df2.assign(County=lambda x: x.COUNTY_NAME + ", " + x.STATE_NAME)
    df2 = df2.drop(columns=["STATE_NAME", "COUNTY_NAME"])

    # Pivot for structure we need, calculate change and percent change, sort
    df2 = df2.pivot_table(index=["FIPS", "County"], columns="YEAR", values=column)
    df2["Change"] = df2[year2] - df2[year1]
    df2["Percent Change"] = (df2[year2] - df2[year1]) / df2[year1] * 100
    df2["Percent Change"] = df2["Percent Change"].round(1)

    df2 = df2.sort_values(display_col, ascending=False)
    df2 = df2.replace([np.inf, -np.inf], np.nan).dropna().reset_index()

    # Color the map with 4 quartiles. This allows the user to quickly see high-level geographic
    # patterns in the data. The default (continuous) scale highlights outliers, which we already
    # show in the "Rankings" tab.
    df2["Quartile"] = pd.qcut(df2[display_col], q=4, precision=1)
    # When the legend represents percent change (a) add a % to each number and
    # (b) Fix an issue where an interval was appearing as (-10.299999999999999, 0.1] despite setting the precision to 1
    if display_col == "Percent Change":
        df2["Quartile"] = df2["Quartile"].apply(
            lambda x: (
                f"({round(x.left, 1)}% - {round(x.right, 1)}%]"  # Decimal format for small values
            )
        )
    else:
        df2["Quartile"] = df2["Quartile"].apply(
            lambda x: (
                f"({int(x.left):,} - {int(x.right):,}]"  # Comma format for large values
            )
        )

    return df2


def get_line_graph(df, var, state_name, county_name):
    fig, ax = plt.subplots()

    df["YEAR"] = df["YEAR"].astype(int)

    # Plot pre-Covid data (before 2020) in black
    df_pre = df[df["YEAR"] <= 2019]
    ax.plot(df_pre["YEAR"], df_pre[var], "-o", color="black", label="Pre-Covid")

    # Plot post-COVID data (2021 onwards) in blue
    df_post = df[df["YEAR"] >= 2021]
    ax.plot(df_post["YEAR"], df_post[var], "-o", color="orange", label="Post-Covid")

    # If 2019 and 2021 are present, connect them with a dashed line to highlight that 2020 is always missing.
    # Any year can be missing because counties with a population < 65k are are dropped from the ACS 1-year estimates.
    if (
        not df.loc[df["YEAR"] == 2019, var].empty
        and not df.loc[df["YEAR"] == 2021, var].empty
    ):
        value_2019 = df.loc[df["YEAR"] == 2019, var].values[0]
        value_2021 = df.loc[df["YEAR"] == 2021, var].values[0]
        ax.plot([2019, 2021], [value_2019, value_2021], "--", color="gray")

    # Set custom x-axis labels
    selected_years = [2005, 2010, 2015, 2020]  # Define the specific years to display
    ax.set_xticks(selected_years)  # Set ticks at these positions
    ax.set_xticklabels(selected_years)  # Ensure labels match the chosen ticks

    # Formatting
    ax.set_title(f"{var}\n{county_name}, {state_name}")
    ax.get_yaxis().set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
    ax.legend()

    return fig


def get_bar_graph(df, var, state_name, county_name):
    fig, ax = plt.subplots()

    df["YEAR"] = df["YEAR"].astype(int)

    df.plot(kind="bar", x="YEAR", y="Percent Change", ax=ax)

    # Modify bar colors based on YEAR values
    for bar, year in zip(ax.patches, df["YEAR"]):
        if year <= 2019:
            bar.set_facecolor("black")
        elif year == 2020:
            bar.set_facecolor("gray")
        elif year >= 2021:
            bar.set_facecolor("orange")

    # Formatting
    ax.set_title(f"Percent Change of {var}\n{county_name}, {state_name}")
    selected_years = [2005, 2010, 2015, 2020]  # Define the specific years to display
    ax.set_xticklabels(
        [str(year) if year in selected_years else "" for year in df["YEAR"]], rotation=0
    )

    # Manually create custom legend
    pre_covid_patch = mpatches.Patch(color="black", label="Pre-Covid")
    post_covid_patch = mpatches.Patch(color="orange", label="Post-Covid")
    ax.legend(handles=[pre_covid_patch, post_covid_patch])

    return fig


def get_percent_change_histogram(df, var, year1, year2, state_name, county_name):
    fig, ax = plt.subplots()

    df.hist(column="Percent Change", ax=ax, color="black", edgecolor="white")

    # Add a vertical line to highlight the selected county
    full_name = ", ".join([county_name, state_name])
    highlight_value = df.loc[df["County"] == full_name, "Percent Change"].values[0]
    ax.axvline(
        highlight_value,
        color="orange",
        linestyle="--",
        linewidth=4,
        label=f"{county_name}",
    )
    ax.legend()

    ax.set_title(f"Percent Change of {var}\nBetween {year1} and {year2}")
    ax.set_xlabel("Percent Change")
    ax.set_ylabel("Number of Counties")

    return fig


def get_change_histogram(df, var, year1, year2, state_name, county_name):
    fig, ax = plt.subplots()

    df.hist(column="Change", ax=ax, color="black", edgecolor="white")

    # Add a vertical line to highlight the selected county
    full_name = ", ".join([county_name, state_name])
    highlight_value = df.loc[df["County"] == full_name, "Change"].values[0]
    ax.axvline(
        highlight_value,
        color="orange",
        linestyle="--",
        linewidth=4,
        label=f"{county_name}",
    )
    ax.legend()

    ax.set_title(f"Change of {var}\nBetween {year1} and {year2}")
    ax.set_xlabel("Change")
    ax.set_ylabel("Number of Counties")

    return fig
