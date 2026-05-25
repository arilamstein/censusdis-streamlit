This tool lets you explore how Covid‑19 reshaped demographic and economic patterns across the United States using American Community Survey (ACS) 1‑year estimates from 2005–2024. You can view trends for the nation, all states, and all counties and places (i.e., cities) with populations of 65,000 or more.

Covid may feel distant now, but its effects are still visible in the data. The rise in people working from home is the clearest example, but you can also see population shifts out of major cities and a sharp increase in households receiving public assistance during the pandemic. This app helps you explore those patterns in your community and compare them with trends across the country.

ACS data for 2020 was not published due to the pandemic. Data for 2025 is expected in September 2026.

You can learn more about the project in these posts and talks:

 * [How Remote Work Has Grown — and Shrunk — Since Covid](https://arilamstein.com/blog/2026/05/18/how-remote-work-has-grown-and-shrunk-since-covid/) — a case study using the latest version of the app, showing how remote work more than tripled nationally between 2019 and 2021 and has declined since — but unevenly, with striking local variation. This version also introduced several major changes: coverage expanded beyond counties to include the nation, all states, and cities; a swarm plot was replaced with a dedicated Compare tab featuring an interactive scatterplot; and a new Ranking tab was added.
 * [New Release: Covid Demographics Explorer v2](https://arilamstein.com/blog/2025/06/02/new-release-covid-demographics-explorer-v2/) — covers the addition of a swarm plot for comparing a location to all others, plus significant codebase improvements including CI, migration to `uv`, and better project structure
 * [San Francisco Python Meetup talk (June 2024)](https://www.youtube.com/watch?v=sdmR5YxGS4g&t=25s) — a talk about an earlier version of the project, focused on how it uses Streamlit
 * [Creating Time Series Data from the American Community Survey (ACS)](https://arilamstein.com/blog/2024/05/28/creating-time-series-data-from-the-american-community-survey-acs/) — covers two subtle but important pitfalls when treating ACS data as a time series: variables can silently change meaning across years, and geographies can appear and disappear
 * [Visualizing the Impact of Covid-19 on US Counties](https://arilamstein.com/blog/2024/05/04/visualizing-the-impact-of-covid-19-on-us-counties/) — explains why the 1-year ACS at the county level was chosen for the initial version of the app, and why Census tracts don't work for this purpose
 * [Building a Census Explorer in Python: Part 1](https://arilamstein.com/blog/2024/02/04/building-a-census-explorer-in-python-part-1/) — the origin of the project: why Streamlit was chosen over other frameworks, why `censusdis` was chosen for Census data access, and how to approach learning Python seriously as an experienced R programmer

This app was created by Ari Lamstein. You can reach me through my [website](https://www.arilamstein.com). 

The app was built in Python using the `streamlit` framework and the `censusdis` package. You can view the code [here](https://github.com/arilamstein/censusdis-streamlit).