census_vars = {
    # var_label                var_table
    'Total Population'       : 'B01001_001E',
    'Median Household Income': 'B19013_001E',
    'Median Rent'            : 'B25058_001E' 
    # TODO: Maybe add B08006_017E - Work from Home?
}

census_vars_reverse = {v: k for k, v in census_vars.items()}
