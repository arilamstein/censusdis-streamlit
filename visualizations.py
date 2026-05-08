import numpy as np
import plotly.graph_objects as go

import backend as be


def _add_source_footer(
    fig: go.Figure,
    source_text: str = "Source: American Community Survey 1-Year Estimates",
) -> None:
    fig.add_annotation(
        text=source_text,
        x=0,
        y=-0.15,
        xref="paper",
        yref="paper",
        showarrow=False,
        xanchor="left",
        yanchor="top",
        align="left",
        font=dict(size=12, color="gray"),
    )


def _get_prefix_for_column(column: str) -> str:
    formats = {
        "Total Population": "",
        "Total Worked from Home": "",
        "Total With Public Assistance": "",
        "Median Household Income": "$",
        "Median Rent": "$",
    }

    if column not in formats:
        raise ValueError(f"Unknown variable: {column}")

    return formats[column]


def _get_ranking_hovertext(column: str) -> str:
    prefix = _get_prefix_for_column(column)
    return (
        "%{customdata[0]}<br>"  # Line 1: location
        f"{column}: {prefix}"  # Line 2: start with column name and optional $
        "%{customdata[1]:,}"  # Add location's value, formatted with , but no .
        "<extra></extra>"  # Suppress trace name
    )


def get_single_year_scatterplot(
    year: int,
    column: str,
    name_to_highlight: str | None = None,
    include_nation: bool = True,
    include_states: bool = True,
    include_counties: bool = True,
    include_places: bool = True,
) -> go.Figure:
    df = be.get_data_by_geo(
        include_nation, include_states, include_counties, include_places
    )
    fig = go.Figure()

    df = df[df["Year"] == year].reset_index(drop=True)

    # A scatterplot with jitter
    rng = np.random.default_rng(seed=42)
    jitter = rng.uniform(-0.3, 0.3, size=len(df))
    fig.add_trace(
        go.Scatter(
            y=df[column],
            x=jitter,
            mode="markers",
            marker=dict(size=8, opacity=0.5),
            customdata=df[["Name", column]].values,
            hovertemplate=_get_ranking_hovertext(column),
            name=column,
            showlegend=False,
        )
    )

    # Optionally highlight a point
    if name_to_highlight:
        hdf = df[df["Name"] == name_to_highlight]

        fig.add_trace(
            go.Scatter(
                x=[0],
                y=hdf[column],
                mode="markers",
                marker=dict(
                    color="gold",
                    size=14,
                    symbol="star",
                    line=dict(color="darkorange", width=1.5),
                ),
                name=name_to_highlight,
                customdata=hdf[["Name", column]].values,
                hovertemplate=_get_ranking_hovertext(column),
            )
        )

    # Title and footer
    fig.update_layout(
        title=(
            f"{column}, {year}<br><sup>Each point represents a location. "
            "Hover to explore.</sup>"
        ),
        xaxis=dict(visible=False, range=[-1, 1]),
        yaxis=dict(title=column, tickformat=","),
        dragmode=False,
    )
    _add_source_footer(fig)

    return fig


def _get_compare_hovertext() -> str:
    return (
        "%{customdata[0]}<br>"  # Line 1: location
        # Line 2: format with 1 decimal point and trailing %
        "Percent Change: %{customdata[1]:,.1f}%"
        "<extra></extra>"  # Suppress trace name
    )


def get_compare_scatterplot(
    year1: int, year2: int, column: str, name_to_highlight: str | None = None
) -> go.Figure:
    fig = go.Figure()

    df = be.get_compare_df(year1, year2, column).reset_index(drop=True)

    # A scatterplot with jitter
    rng = np.random.default_rng(seed=42)
    jitter = rng.uniform(-0.25, 0.25, size=len(df))
    fig.add_trace(
        go.Scatter(
            y=df["Percent Change"],
            x=jitter,
            mode="markers",
            marker=dict(size=8, opacity=0.5),
            customdata=df[["Name", "Percent Change"]].values,
            hovertemplate=_get_compare_hovertext(),
            name="Percent Change",
            showlegend=False,
        )
    )

    # Optionally put a star to highlight a point
    if name_to_highlight:
        hdf = df[df["Name"] == name_to_highlight]

        fig.add_trace(
            go.Scatter(
                x=[0],
                y=hdf["Percent Change"],
                mode="markers",
                marker=dict(
                    color="gold",
                    size=14,
                    symbol="star",
                    line=dict(color="darkorange", width=1.5),
                ),
                name=name_to_highlight,
                customdata=hdf[["Name", "Percent Change"]].values,
                hovertemplate=_get_compare_hovertext(),
            )
        )

    # Title and footer
    fig.update_layout(
        title=(
            f"Percent Change in {column}, {year1}–{year2}<br>"
            "<sup>Each point represents a location. Hover to explore.</sup>"
        ),
        xaxis=dict(visible=False, range=[-1, 1]),
        yaxis=dict(title="Percent Change", tickformat=","),
        dragmode=False,
    )
    _add_source_footer(fig)

    return fig


def _get_line_hovertext(column: str) -> str:
    prefix = _get_prefix_for_column(column)
    return (
        "Year: %{x}<br>"  # Line 1: year
        f"{column}: {prefix}"  # Line 2: Start with variable name and optional $
        "%{y:,}"  # format number with commas and no .
        "<extra></extra>"  # Suppress trace name
    )


def _get_axis_unit_for_column(column: str) -> str:
    units = {
        "Total Population": "People",
        "Total Worked from Home": "People",
        "Total With Public Assistance": "People",
        "Median Household Income": "Dollars",
        "Median Rent": "Dollars",
    }

    if column not in units:
        raise ValueError(f"Unknown variable: {column}")

    return units[column]


def get_line_graph(name: str, col: str) -> go.Figure:
    df = be.get_data_for_name(name)
    df["Year"] = df["Year"].astype(int)

    pre_covid_color = "black"
    post_covid_color = "#FF4500"
    missing_color = "gray"

    fig = go.Figure()

    # Pre‑COVID line (<= 2019)
    pre_df = df[df["Year"] <= 2019]
    fig.add_trace(
        go.Scatter(
            x=pre_df["Year"],
            y=pre_df[col],
            mode="lines+markers",
            line=dict(color=pre_covid_color),
            marker=dict(color=pre_covid_color),
            name="Pre‑Covid",
            hovertemplate=_get_line_hovertext(col),
        )
    )

    # Post‑COVID line (>= 2021)
    post_df = df[df["Year"] >= 2021]
    fig.add_trace(
        go.Scatter(
            x=post_df["Year"],
            y=post_df[col],
            mode="lines+markers",
            line=dict(color=post_covid_color),
            marker=dict(color=post_covid_color),
            name="Post‑Covid",
            hovertemplate=_get_line_hovertext(col),
        )
    )

    # Missing 2020 connector (dashed)
    if 2019 in df["Year"].values and 2021 in df["Year"].values:
        y2019 = df.loc[df["Year"] == 2019, col].values[0]
        y2021 = df.loc[df["Year"] == 2021, col].values[0]
        fig.add_trace(
            go.Scatter(
                x=[2019, 2021],
                y=[y2019, y2021],
                mode="lines",
                line=dict(color=missing_color, dash="dash"),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    # Layout
    fig.update_layout(
        title={
            "text": f"{col}<br>{name}",
            "x": 0.5,
            "xanchor": "center",
        },
        xaxis=dict(
            tickmode="array",
            tickvals=[2005, 2010, 2015, 2020],
            ticktext=["2005", "2010", "2015", "2020"],
        ),
        yaxis=dict(
            tickformat=",",
            title=_get_axis_unit_for_column(col),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        margin=dict(l=40, r=40, t=80, b=80),
        dragmode=False,
    )

    _add_source_footer(
        fig,
        (
            "Dashed line indicates data missing for 2020.<br>"
            "Source: American Community Survey 1-Year Estimates."
        ),
    )

    return fig
