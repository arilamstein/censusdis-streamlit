library(choroplethr)
library(choroplethrMaps)
library(dplyr)
library(stringr)
library(tools)
library(readr)

# FYI: ?county.regions is derived from ?county.map
data("county.regions")

# Tailor the data to our specific use case
county.regions = county.regions |>
  select(county.fips.character, county.name, state.name) |>
  rename(fips=county.fips.character) |>
  as_tibble()

county.regions$state.fips = str_sub(county.regions$fips, 1, 2)
county.regions$county.fips = str_sub(county.regions$fips, 3)

county.regions$county.name = toTitleCase(county.regions$county.name)
county.regions$state.name = toTitleCase(county.regions$state.name)

# The data is created for use in the streamlit app
write_csv(county.regions, "~/streamlit-census/county_names.csv")
