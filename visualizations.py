import backend as be

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
import plotly.express as px


def get_map(var, year1, year2, display_col):
    fig = px.choropleth(
        be.get_mapping_df(var, year1, year2, display_col),
        geojson=be.county_map,
        locations="FIPS",
        color="Quartile",
        color_discrete_sequence=["#ffffcc", "#a1dab4", "#41b6c4", "#225ea8"],
        scope="usa",
        hover_name="County",
        hover_data={"FIPS": False, display_col: True},
        labels={"Quartile": display_col, "FIPS": "NAME"},
    )
    fig.update_layout(title_text=f"{display_col} of {var} between {year1} and {year2}")

    return fig


def get_line_graph(df, var, state_name, county_name):
    fig, ax = plt.subplots()

    df["YEAR"] = df["YEAR"].astype(int)

    # Plot pre-Covid data (before 2020) in black
    df_pre = df[df["YEAR"] <= 2019]
    ax.plot(df_pre["YEAR"], df_pre[var], "-o", color="black", label="Pre-Covid")

    # Plot post-COVID data (2021 onwards) in blue
    df_post = df[df["YEAR"] >= 2021]
    ax.plot(df_post["YEAR"], df_post[var], "-o", color="orange", label="Post-Covid")

    # If 2019 and 2021 are present, connect them with a dashed line to highlight that 2020 is always missing.
    # Any year can be missing because counties with a population < 65k are are dropped from the ACS 1-year estimates.
    if (
        not df.loc[df["YEAR"] == 2019, var].empty
        and not df.loc[df["YEAR"] == 2021, var].empty
    ):
        value_2019 = df.loc[df["YEAR"] == 2019, var].values[0]
        value_2021 = df.loc[df["YEAR"] == 2021, var].values[0]
        ax.plot([2019, 2021], [value_2019, value_2021], "--", color="gray")

    # Set custom x-axis labels
    selected_years = [2005, 2010, 2015, 2020]  # Define the specific years to display
    ax.set_xticks(selected_years)  # Set ticks at these positions
    ax.set_xticklabels(selected_years)  # Ensure labels match the chosen ticks

    # Formatting
    ax.set_title(f"{var}\n{county_name}, {state_name}")
    ax.get_yaxis().set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
    ax.legend()

    return fig


def get_bar_graph(df, var, state_name, county_name):
    fig, ax = plt.subplots()

    df["YEAR"] = df["YEAR"].astype(int)

    df.plot(kind="bar", x="YEAR", y="Percent Change", ax=ax)

    # Modify bar colors based on YEAR values
    for bar, year in zip(ax.patches, df["YEAR"]):
        if year <= 2019:
            bar.set_facecolor("black")
        elif year == 2020:
            bar.set_facecolor("gray")
        elif year >= 2021:
            bar.set_facecolor("orange")

    # Formatting
    ax.set_title(f"Percent Change of {var}\n{county_name}, {state_name}")
    selected_years = [2005, 2010, 2015, 2020]  # Define the specific years to display
    ax.set_xticklabels(
        [str(year) if year in selected_years else "" for year in df["YEAR"]], rotation=0
    )

    # Manually create custom legend
    pre_covid_patch = mpatches.Patch(color="black", label="Pre-Covid")
    post_covid_patch = mpatches.Patch(color="orange", label="Post-Covid")
    ax.legend(handles=[pre_covid_patch, post_covid_patch])

    return fig


def get_histogram(df, var, year1, year2, state_name, county_name, display_col):
    fig, ax = plt.subplots()

    df.hist(column=display_col, ax=ax, color="black", edgecolor="white")

    # Add a vertical line to highlight the selected county
    full_name = ", ".join([county_name, state_name])
    highlight_value = df.loc[df["County"] == full_name, display_col].values[0]
    ax.axvline(
        highlight_value,
        color="orange",
        linestyle="--",
        linewidth=4,
        label=f"{county_name}",
    )
    ax.legend()

    ax.set_title(f"{display_col} of {var}\nAll Counties, {year1} to {year2}")
    ax.set_xlabel(display_col)
    ax.set_ylabel("Number of Counties")

    return fig


def get_boxplot(df, var, year1, year2, state_name, county_name, display_col):
    fig, ax = plt.subplots()

    df.boxplot(column=display_col, ax=ax)

    # If the highlighted county is present in both years, add a vertical line to highlight its value
    full_name = ", ".join([county_name, state_name])
    if not df.loc[df["County"] == full_name, display_col].empty:
        highlight_value = df.loc[df["County"] == full_name, display_col].values[0]
        ax.axhline(
            highlight_value,
            color="orange",
            linestyle="--",
            linewidth=2,
            label=f"{county_name}",
        )
        ax.legend()

    ax.set_title(f"{display_col} of {var}\nAll Counties, {year1} to {year2}")
    ax.set_ylabel(display_col)
    ax.xaxis.set_visible(False)

    return fig
