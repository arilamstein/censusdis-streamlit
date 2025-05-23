# The Census Bureau calls 'B01001_001E' a 'Name' and 'Total Population' a 'Label'.
# The actual labels from Census are a bit awkward (e.g. "Estimate!!Total!!Worked at home"),
# so replace them with something simpler.
# Note that the Label 'Worked from Home' has had different 'Names' over the years.
census_vars = {
    "B01001_001E": "Total Population",
    "B08006_021E": "Total Worked from Home",  # 2005 only
    "B08006_017E": "Total Worked from Home",  # 2006 onwards
    "B19057_002E": "Total With Public Assistance",
    "B19013_001E": "Median Household Income",
    "B25058_001E": "Median Rent",
}


# In 2005 B08006_017E was used for "total motorcycle commuters".
# In all other years it was used for "total worked from home".
def get_census_vars_for_year(year):
    ret = dict(census_vars)  # Copy to avoid modifying the global variable
    if year == 2005:
        del ret["B08006_017E"]
    else:
        del ret["B08006_021E"]

    return ret


# This code is hard to read but it serves a purpose.
# In short: the order in which census_vars lists the variables is the order
# in which I want them to appear in the dropdown. The issue is that they contain
# duplicates due to the variable for "Work From Home" changing name throughtout
# the years. This code removes the duplicates while retaining the initial ordering,
# and prevents me from needing to duplicate data here.
# See: https://stackoverflow.com/a/17016257/2518602
def get_unique_census_labels():
    return list(dict.fromkeys(census_vars.values()))
