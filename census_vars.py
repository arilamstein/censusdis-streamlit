census_vars = {
    'Total Population'       : 'B01001_001E',
    'Worked from Home'       : None,
    'Median Household Income': 'B19013_001E',
    'Median Rent'            : 'B25058_001E' 
}

# Thank you to the Census Slack group for explaining that variable B08006_017E  
# changed in 2006. In 2005 it was used for "total motorcycle commuters". In all other years
# it was used for "total worked from home".
def get_table_for_wfh(year):
    if year == 2005:
        return 'B08006_021E'
    else:
        return 'B08006_017E'

def get_census_vars_for_year(year):
    ret = census_vars
    ret['Worked from Home'] = get_table_for_wfh(year)

    return ret