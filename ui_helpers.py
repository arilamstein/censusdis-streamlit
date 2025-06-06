# If the user selects California then have the County dropdown default to San Francisco County.
# If the user selects New York then have it default to New York County (i.e. Manhattan).
# Otherwise have it default to the first county using alphabetical order.
def get_county_index(state):
    if state == "California":
        return 25  # San Francisco
    elif state == "New York":
        return 16  # New York (Manhattan)

    return 0


# The "County Ranking" table benefits from some styling ...
def apply_styles(styler, full_name, year1, year2, sorting_col):
    # 1. A background gradient to the "Percent Change" column
    styler.background_gradient(axis=0, cmap="Blues_r", subset=sorting_col)

    # The above change seems to cause the app to write too many significant changes. So re-apply that
    # style, and also add in a % to the "percent change" column
    styler.format(
        {
            year1: "{:,.0f}",  # Comma for thousands separator, and no significant digits
            year2: "{:,.0f}",
            "Change": "{:,.0f}",
            "Percent Change": "{:,.1f}%",  # Ditto but end with a % sign
        }
    )

    # 2. Highlighting the row corresponding to the selected county
    def highlight_row(row):
        condition = row["Full Name"] == full_name

        style = [
            (
                "background-color: #FFFACD; font-weight: bold; color: black"
                if condition and col != "Percent Change"
                else ""
            )
            for col in row.index
        ]

        return style

    return styler.apply(lambda _: highlight_row(_), axis=1)
