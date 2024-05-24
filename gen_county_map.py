# This is the county map that plotly uses in their example choropleth map page:
# https://plotly.com/python/choropleth-maps/

from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
    with open('county_map.json', 'w', encoding='utf-8') as f:
        json.dump(counties, f, ensure_ascii=False, indent=4)
