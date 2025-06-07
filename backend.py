import pandas as pd
import numpy as np
import json


df = pd.read_csv("data/county_data.csv", dtype={"FIPS": str, "Year": str})
with open("data/county_map.json", "r") as read_file:
    county_map = json.load(read_file)


def get_states():
    return df["State"].unique()


def get_counties(state):
    return df.loc[df["State"] == state]["County"].sort_values().unique()


def get_census_data(full_name, var, add_2020):
    ret = df.loc[df["Full Name"] == full_name][["Full Name", "Year", var]]

    # There is no data for 2020. But adding in an NA row helps the graphs look better.
    if add_2020:
        row_for_2020 = pd.DataFrame(
            [
                {
                    "Full Name": ret.iloc[0]["Full Name"],
                    "Year": "2020",
                }
            ]
        )
        ret = pd.concat([ret, row_for_2020])
        ret = ret.sort_values(["Full Name", "Year"])

    return ret


def get_ranking_df(column, year1, year2, unit_col, include_fips):
    df2 = df.copy()  # We don't want to modify the global variable

    # Select just the rows and columns we need
    df2 = df2.loc[(df2["Year"] == year1) | (df2["Year"] == year2)]
    df2 = df2[["FIPS", "Full Name", "Year", column]]

    # Pivot for structure we need, calculate change and percent change, sort
    df2 = df2.pivot_table(index=["FIPS", "Full Name"], columns="Year", values=column)
    df2["Change"] = df2[year2] - df2[year1]
    df2["Percent Change"] = (df2[year2] - df2[year1]) / df2[year1] * 100
    df2["Percent Change"] = df2["Percent Change"].round(1)
    df2 = df2.sort_values(unit_col)

    # Drop Columns with Infinite percent change (first or last year has 0)
    df2 = df2.replace([np.inf, -np.inf], np.nan).dropna()
    # Create an index called "Rank"
    df2["Rank"] = list(range(1, len(df2.index) + 1))
    df2 = df2.reset_index().set_index("Rank")

    # The FIPS code column is only needed for the map. And we don't want to show
    # it to the user in the table.
    if not include_fips:
        df2 = df2.drop(columns="FIPS")

    return df2


def get_ranking_text(full_name, var, ranking_df):
    # Thank you copilot
    def ordinal_suffix(n):
        if 11 <= n <= 13:
            return "th"
        return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")

    if full_name not in list(ranking_df["Full Name"]):
        return f"**{full_name}** does not have a ranking for **{var}**."

    rank = ranking_df[ranking_df["Full Name"] == full_name].index.tolist()[0]
    num_counties = len(ranking_df.index)
    percentile = round((rank - 1) / (num_counties - 1) * 100)

    return (
        f"{full_name} ranks **{rank}** of {num_counties} counties "
        f"(the {percentile}{ordinal_suffix(percentile)} percentile)."
    )
