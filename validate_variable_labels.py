from collections import defaultdict

import censusdis.data as ced
from censusdis.datasets import ACS1


def get_unique_labels_for_variable(acs, variable, years):
    """
    Return all labels the ACS has used for a given variable.

    Note that the ACS sometimes changes the labels of a variable. Sometimes these changes are minor,
    and sometimes the same variable is used for something completely different. This function is designed to
    facilitate doing this check over multiple years.

    For example, B08006_017E in 2005 had label 'Estimate!!Total!!Motorcycle'. But in 2006 it switched to
    'Estimate!!Total!!Worked at home'. And in 2019 it changed to 'Estimate!!Total:!!Worked from home'.

    Parameters:
    - acs: The ACS to use. Ex. censusdis.datasets.ACS1)
    - variable: The variable in question. Ex. 'B01001_001E'
    - years: An iterable of years to use. Ex. [2005, 2006, 2007]

    Returns:
    - A dict where each key is a label, and each value is a list of years that key has been used.

    Note: If the dict returned is of length 1, then the variable has only ever had 1 label.
    """
    labels = defaultdict(list)

    for year in years:
        label = ced.variables.get(acs, year, variable)["label"]
        labels[label].append(year)

    return labels


def get_variables_used(df):
    non_variable_columns = ["NAME", "COUNTY_NAME", "STATE_NAME", "YEAR"]
    return [
        one_column
        for one_column in df.columns
        if one_column not in non_variable_columns
    ]


def get_years_variable_used(df, variable):
    return df[df[variable].notna()]["YEAR"].unique()


def print_labels_for_variables_over_time(df):
    variables_used = get_variables_used(df)

    for variable in variables_used:
        years_variable_used = sorted(get_years_variable_used(df, variable))
        unique_labels_for_variable = get_unique_labels_for_variable(
            ACS1, variable, years_variable_used
        )

        if len(unique_labels_for_variable) == 1:
            print(f"{variable} has only 1 label")
        else:
            print(f"{variable} has the following labels:")
            for label, years in unique_labels_for_variable.items():
                print(f"\t'{label}' in years {years}")
