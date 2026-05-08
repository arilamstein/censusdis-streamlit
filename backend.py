from pathlib import Path

import pandas as pd
from pandas.io.formats.style import Styler

from scripts.census_vars import census_vars_post_2005

DATA_DIR = Path("data")
df_us = pd.read_csv(DATA_DIR / "us.csv")
df_state = pd.read_csv(DATA_DIR / "state.csv")
df_county = pd.read_csv(DATA_DIR / "county.csv")
df_place = pd.read_csv(DATA_DIR / "place.csv")
df_all = pd.concat([df_us, df_state, df_county, df_place])

# Certain cities (especially "unincoporated cities" in Virginia) appear twice in the
# underlying data - once in the county file and once in the place data.
df_all = df_all.drop_duplicates(subset=["Name", "Year"]).reset_index(drop=True)


def get_all_names() -> list[str]:
    return sorted(df_all["Name"].unique().tolist())


def get_data_for_name(name: str) -> pd.DataFrame:
    return df_all.loc[df_all["Name"] == name].copy()


def get_data_by_geo(
    include_nation: bool,
    include_states: bool,
    include_counties: bool,
    include_places: bool,
) -> pd.DataFrame:
    frames = []
    if include_nation:
        frames.append(df_us)
    if include_states:
        frames.append(df_state)
    if include_counties:
        frames.append(df_county)
    if include_places:
        frames.append(df_place)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames)


def get_table_df(
    year: int | None,
    include_nation: bool = True,
    include_states: bool = True,
    include_counties: bool = True,
    include_places: bool = True,
) -> pd.DataFrame:
    df = get_data_by_geo(
        include_nation, include_states, include_counties, include_places
    )
    df = df_all.drop(columns=["State", "County", "Place"])
    if year:
        df = df[df["Year"] == year]
    return df


def get_demographic_statistics() -> list[str]:
    demographics = [v for v in census_vars_post_2005.values() if v != "Name"]
    special = "Total Worked from Home"
    demographics.remove(special)
    return [special] + demographics


def style_table_df(df: pd.DataFrame) -> Styler:
    fmt = {
        v: lambda x: f"{x:,.0f}" for v in census_vars_post_2005.values() if v != "Name"
    }
    return df.style.format(fmt)  # type: ignore[arg-type]


def get_table_df_styled(
    year: int,
    column: str,
    include_nation: bool,
    include_states: bool,
    include_counties: bool,
    include_places: bool,
) -> Styler:
    df = get_table_df(
        year, include_nation, include_states, include_counties, include_places
    ).sort_values(column, ascending=False)
    return style_table_df(df[["Name", "Year", column]])


def get_years() -> list[int]:
    return list(df_all["Year"].unique())


def get_compare_df(year1: int, year2: int, column: str) -> pd.DataFrame:
    """
    Return a wide DataFrame with Name, year1, year2, and change columns
    for the given location and column.
    """
    # Pivot so we can easily compare years
    df = get_table_df(None)
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


def style_compare_df(df: pd.DataFrame) -> Styler:
    int_cols = [str(year) for year in get_years()] + ["Change"]
    fmt = {col: lambda x: f"{x:,.0f}" for col in int_cols}
    fmt["Percent Change"] = lambda x: f"{x:,.1f}%"
    return df.style.format(fmt)  # type: ignore[arg-type]


def get_compare_df_styled(year1: int, year2: int, column: str) -> Styler:
    df = get_compare_df(year1, year2, column)
    return style_compare_df(df)
