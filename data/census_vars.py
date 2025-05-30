# The Census Bureau calls 'B01001_001E' a 'Name' and 'Total Population' a 'Label'.
# The actual labels from Census are a bit awkward (e.g. "Estimate!!Total!!Worked at home"),
# so replace them with something simpler.
# Note that the Label 'Worked from Home' had a different 'Name' in 2005 as opposed to every other year.
census_vars_2005 = {
    "NAME": "NAME",
    "B01001_001E": "Total Population",
    "B08006_021E": "Total Worked from Home",  # 2005 only
    "B19057_002E": "Total With Public Assistance",
    "B19013_001E": "Median Household Income",
    "B25058_001E": "Median Rent",
}

census_vars_post_2005 = {
    "NAME": "NAME",
    "B01001_001E": "Total Population",
    "B08006_017E": "Total Worked from Home",  # 2006 onwards
    "B19057_002E": "Total With Public Assistance",
    "B19013_001E": "Median Household Income",
    "B25058_001E": "Median Rent",
}

census_dropdown_values = [v for v in census_vars_post_2005.values() if v != "NAME"]

