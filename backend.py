import pandas as pd
from pathlib import Path


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
