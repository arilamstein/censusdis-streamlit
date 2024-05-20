# The Census Bureau calls 'B01001_001E' a 'Name'
# It calls 'Total Population' a 'Label'
# Note that the Label 'Worked from Home' has had different 'Names' over the years.
census_vars = {
    'B01001_001E' : 'Total Population',
    'B08006_021E' : 'Worked from Home', # 2005 only
    'B08006_017E' : 'Worked from Home', # 2006 onwards
    'B19013_001E' : 'Median Household Income',
    'B25058_001E' : 'Median Rent'
}

# In 2005 B08006_017E was used for "total motorcycle commuters". 
# In all other years it was used for "total worked from home".
def get_census_vars_for_year(year):
    ret = dict(census_vars) # Copy to avoid modifying the global variable
    if year == 2005:
        del ret['B08006_017E']
    else:
        del ret['B08006_021E']

    return ret