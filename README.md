Timeline
========

A small application to pull out statistics from Google Takeout data specifically for Location data.

Given the deprecation of the centralised Google Timeline application (data is now stored locally on each device), these set of scripts were developed to process and visualise the data we can get from Google Takeout.

As of writing, the only statistics computed are those I am using on my website but I hope to compute more over time. Activity data has been excluded for now.

## Running the scripts

Provide the environment variables in `.env`, then run the following

```
uv run timeline/app.py --takeout-dir=<path to takeout directory>
```

This produces a `timeline_statistics.json` file with the following fields

```
{
    "num_continents": int,
    "num_countries": int,
    "num_cities": int,
    "num_countries_per_continent": int,
    "num_places_per_year_per_month": int,
    "num_places_per_year": int,
    "num_places": int,
    "num_england_counties": int,
    "num_london_boroughs": int,
    "num_usa_states": int,
    "continents": array(string),
    "countries": array(string),
    "countries_per_continent": object(string, array(string)),
    "cities": array(string),
    "places": array(string),
    "england_counties": array(string),
    "london_boroughs": array(string),
    "usa_states": array(string),
}
```
