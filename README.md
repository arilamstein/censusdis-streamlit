# Covid Demographics Explorer
[![CI](https://github.com/arilamstein/censusdis-streamlit/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/arilamstein/censusdis-streamlit/actions/workflows/lint.yml)

This [app](https://census-explorer.streamlit.app/) uses data from the American Community Survey (ACS) to help people understand how America has changed since Covid-19. You can view trends for the nation, all 50 states, and all counties and cities with populations of 65,000 or more.

The app has three tabs:

- **Trend** — a time series showing how a demographic changed in your selected location from 2005 to 2024
- **Compare Years** — an interactive scatterplot showing how all locations changed between any two years, with a sortable table of the underlying data
- **Ranking** — a scatterplot and table showing where your selected location stands relative to all others for a given year and demographic

In addition to informing the public, I hope that this project will inspire others to use Python to explore Census data. If you'd like to use this repo as a starting off point for your own project, see [DEVELOPER.md](DEVELOPER.md).

I've written a series of blog posts documenting how this project evolved. If you're interested in building something similar, they walk through the key design decisions and technical choices along the way:

 * [How Remote Work Has Grown — and Shrunk — Since Covid](https://arilamstein.com/blog/2026/05/18/how-remote-work-has-grown-and-shrunk-since-covid/) — a case study using the latest version of the app, showing how remote work more than tripled nationally between 2019 and 2021 and has declined since — but unevenly, with striking local variation. This version also introduced several major changes: coverage expanded beyond counties to include the nation, all states, and cities; a swarm plot was replaced with a dedicated Compare tab featuring an interactive scatterplot; and a new Ranking tab was added.
 * [New Release: Covid Demographics Explorer v2](https://arilamstein.com/blog/2025/06/02/new-release-covid-demographics-explorer-v2/) — covers the addition of a swarm plot for comparing a location to all others, plus significant codebase improvements including CI, migration to `uv`, and better project structure
 * [San Francisco Python Meetup talk (June 2024)](https://www.youtube.com/watch?v=sdmR5YxGS4g&t=25s) — a talk about an earlier version of the project, focused on how it uses Streamlit
 * [Creating Time Series Data from the American Community Survey (ACS)](https://arilamstein.com/blog/2024/05/28/creating-time-series-data-from-the-american-community-survey-acs/) — covers two subtle but important pitfalls when treating ACS data as a time series: variables can silently change meaning across years, and geographies can appear and disappear
 * [Visualizing the Impact of Covid-19 on US Counties](https://arilamstein.com/blog/2024/05/04/visualizing-the-impact-of-covid-19-on-us-counties/) — explains why the 1-year ACS at the county level was chosen for the initial version of the app, and why Census tracts don't work for this purpose
 * [Building a Census Explorer in Python: Part 1](https://arilamstein.com/blog/2024/02/04/building-a-census-explorer-in-python-part-1/) — the origin of the project: why Streamlit was chosen over other frameworks, why `censusdis` was chosen for Census data access, and how to approach learning Python seriously as an experienced R programmer

This app was created by [Ari Lamstein](https://www.arilamstein.com).