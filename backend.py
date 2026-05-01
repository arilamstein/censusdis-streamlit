import pandas as pd
from pathlib import Path
from scripts.census_vars import census_vars_post_2005

DATA_DIR = Path("data")
df_all = pd.concat(
    [
        pd.read_csv(DATA_DIR / "us.csv"),
        pd.read_csv(DATA_DIR / "state.csv"),
        pd.read_csv(DATA_DIR / "county.csv"),
        pd.read_csv(DATA_DIR / "place.csv"),
    ]
)
# Certain cities (especially "unincoporated cities" in Virginia) appear twice in the
# underlying data - once in the county file and once in the place data.
df_all = df_all.drop_duplicates(subset=["Name", "Year"]).reset_index(drop=True)


def get_all_states() -> list[str]:
    return sorted(df_all["State"].dropna().unique().tolist())


def get_all_names() -> list[str]:
    return sorted(df_all["Name"].unique().tolist())


def get_data_for_name(name: str) -> pd.DataFrame:
    return df_all[df_all["Name"] == name].copy().sort_values("Year")


def get_census_data(name, col, add_2020):
    ret = df_all.loc[df_all["Name"] == name][["Name", "Year", col]]

    # There is no data for 2020. But adding in an NA row helps the graphs look better.
    if add_2020:
        row_for_2020 = pd.DataFrame(
            [
                {
                    "Name": ret.iloc[0]["Name"],
                    "Year": "2020",
                }
            ]
        )
        ret = pd.concat([ret, row_for_2020])
        ret = ret.sort_values(["Name", "Year"])

    return ret


def get_table_df():
    return df_all.drop(columns=["State", "County", "Place"])


def style_table_df(df):
    fmt = {
        v: lambda x: f"{x:,.0f}" for v in census_vars_post_2005.values() if v != "Name"
    }
    return df.style.format(fmt)


def get_table_df_styled():
    df = get_table_df()
    return style_table_df(df)


def get_years():
    return list(df_all["Year"].unique())


def get_compare_df(year1, year2, column):
    """
    Return a wide DataFrame with Name, year1, year2, and change columns
    for the given location and column.
    """
    # Pivot so we can easily compare years
    df = get_table_df()
    df_wide = df.pivot(index="Name", columns="Year", values=column).reset_index()
    df_wide.columns.name = None

    # Years are ints, and "mixed type" columns generates a warning,
    # so convert all columns to string.
    # Also convert the incoming year variables to strings for consistency
    df_wide.columns = df_wide.columns.map(str)
    y1 = str(year1)
    y2 = str(year2)

    # Compute change
    df_wide = df_wide[["Name", y1, y2]].dropna()
    df_wide["Change"] = df_wide[y2] - df_wide[y1]

    # Add a "Percent Change" column and sort on it
    df_wide["Percent Change"] = df_wide["Change"] / df_wide[y1] * 100
    df_wide = df_wide.sort_values("Percent Change", ascending=False)

    return df_wide


def style_compare_df(df):
    int_cols = [str(year) for year in get_years()] + ["Change"]
    fmt = {col: lambda x: f"{x:,.0f}" for col in int_cols}
    fmt["Percent Change"] = lambda x: f"{x:,.1f}%"
    return df.style.format(fmt)


def get_compare_df_styled(year1, year2, column):
    df = get_compare_df(year1, year2, column)
    return style_compare_df(df)
