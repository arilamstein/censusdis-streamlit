"""
Generate US, state, county, and place data for all variables and write them to CSV files.
"""

from pathlib import Path
from gen_data_helpers import (
    get_us_data,
    get_state_data,
    get_county_data,
    get_place_data,
)
from utils import format_duration
import time

start = time.time()

END_YEAR = 2024
DATA_DIR = Path("data")
get_us_data(end_year=END_YEAR, verbose=True).to_csv(DATA_DIR / "us.csv", index=False)
# get_state_data(end_year=END_YEAR, verbose=True).to_csv(
#     DATA_DIR / "state.csv", index=False
# )
# get_county_data(end_year=END_YEAR, verbose=True).to_csv(
#     DATA_DIR / "county.csv", index=False
# )
# get_place_data(end_year=END_YEAR, verbose=True).to_csv(
#     DATA_DIR / "place.csv", index=False
# )

end = time.time()
duration = end - start

print(f"Ran in {format_duration(duration)}")
