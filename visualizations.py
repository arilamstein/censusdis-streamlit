import plotly.express as px
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


def get_compare_boxplot(year1: int, year2: int, column: str) -> go.Figure:
    df = be.get_compare_df(year1, year2, column)

    fig = px.box(
        df,
        y="Percent Change",
        custom_data=["Name", "Percent Change"],
        title=f"Percent Change in {column}, {year1}-{year2}",
        points="all",
    )
    fig.update_traces(
        hovertemplate=(
            "%{customdata[0]}<br>Percent Change: %{customdata[1]:,.1f}%<extra></extra>"
        )
    )
    fig.update_layout(
        title={
            "text": f"Percent Change in {column}, {year1}-{year2}",
            "x": 0.5,
            "xanchor": "center",
        },
        dragmode=False,
    )

    _add_source_footer(fig)

    return fig


def get_compare_violinplot(
    year1: int, year2: int, column: str, name_to_highlight: str | None = None
) -> go.Figure:
    df = be.get_compare_df(year1, year2, column)

    fig = go.Figure()

    violin_hover = (
        "%{customdata[0]}<br>Percent Change: %{customdata[1]:,.1f}%<extra></extra>"
    )
    fig.add_trace(
        go.Violin(
            y=df["Percent Change"],
            x=["Percent Change"] * len(df),
            box_visible=True,
            meanline_visible=False,
            points="all",
            hoveron="points",  # Removes the violin/box stat hovers, keeps point hovers
            customdata=df[["Name", "Percent Change"]].values,
            hovertemplate=violin_hover,
            name="Percent Change",
            showlegend=False,
        )
    )

    # Optionally highlight a point
    if name_to_highlight:
        hdf = df[df["Name"] == name_to_highlight]

        scatter_hover = (
            "%{customdata[0]}<br>Percent Change: %{customdata[1]:,.1f}%<extra></extra>"
        )
        fig.add_trace(
            go.Scatter(
                x=["Percent Change"],
                y=hdf["Percent Change"],
                mode="markers",
                marker=dict(color="red", size=12, symbol="star"),
                name=name_to_highlight,
                customdata=hdf[["Name", "Percent Change"]].values,
                hovertemplate=scatter_hover,
            )
        )

    fig.update_layout(
        title=f"Percent Change in {column}<br><sup>{year1}–{year2}</sup>",
        xaxis=dict(visible=False),
        yaxis=dict(title="Percent Change", tickformat=","),
    )

    _add_source_footer(fig)

    return fig


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
            hovertemplate="Year: %{x}<br>" + f"{col}: " + "%{y:,.0f}<extra></extra>",
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
            hovertemplate="Year: %{x}<br>" + f"{col}: " + "%{y:,.0f}<extra></extra>",
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
