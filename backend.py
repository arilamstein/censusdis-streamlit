import pandas as pd
import numpy as np
import json


df = pd.read_csv("data/county_data.csv", dtype={"FIPS": str, "YEAR": str})
with open("data/county_map.json", "r") as read_file:
    county_map = json.load(read_file)


def get_state_names():
    return df["STATE_NAME"].unique()


def get_county_names(state_name):
    return df.loc[df["STATE_NAME"] == state_name]["COUNTY_NAME"].sort_values().unique()


def get_census_data(state_name, county_name, var, add_2020):
    ret = df.loc[(df["STATE_NAME"] == state_name) & (df["COUNTY_NAME"] == county_name)][
        ["STATE_NAME", "COUNTY_NAME", "YEAR", var]
    ]

    # There is no data for 2020. But adding in an NA row helps the graphs look better.
    if add_2020:
        row_for_2020 = pd.DataFrame(
            [
                {
                    "STATE_NAME": ret.iloc[0]["STATE_NAME"],
                    "COUNTY_NAME": ret.iloc[0]["COUNTY_NAME"],
                    "YEAR": "2020",
                }
            ]
        )
        ret = pd.concat([ret, row_for_2020])
        ret = ret.sort_values(["STATE_NAME", "COUNTY_NAME", "YEAR"])

    return ret


def get_ranking_df(column, year1, year2, unit_col):
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
    df2 = df2.sort_values(unit_col)

    # Drop Columns with Infinite percent change (first or last year has 0)
    df2 = df2.replace([np.inf, -np.inf], np.nan).dropna()
    # Create an index called "Rank"
    df2["Rank"] = list(range(1, len(df2.index) + 1))
    df2 = df2.reset_index().set_index("Rank")

    return df2


def get_ranking_text(state, county, var, ranking_df, year1, year2, unit_col):
    full_name = ", ".join([county, state])

    if full_name not in list(ranking_df["County"]):
        return f"**{full_name}** does not have a ranking for **{var}**."

    rank = ranking_df[ranking_df["County"] == full_name].index.tolist()[0]

    num_counties = len(ranking_df.index)

    return (
        f"{unit_col} of {var} between {year1} and {year2}.<br>"
        f"{full_name} ranks **{rank}** of {num_counties} counties."
    )


def get_mapping_df(column, year1, year2, unit_col):
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

    df2 = df2.sort_values(unit_col, ascending=False)
    df2 = df2.replace([np.inf, -np.inf], np.nan).dropna().reset_index()

    # Color the map with 4 quartiles. This allows the user to quickly see high-level geographic
    # patterns in the data. The default (continuous) scale highlights outliers, which we already
    # show in the "Rankings" tab.
    df2["Quartile"] = pd.qcut(df2[unit_col], q=4, precision=1)
    # When the legend represents percent change (a) add a % to each number and
    # (b) Fix an issue where an interval was appearing as (-10.299999999999999, 0.1] despite setting the precision to 1
    if unit_col == "Percent Change":
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
