from collections import defaultdict

from timeline.geography import ReverseGeoLookup, country_code_to_continent


def compute_statistics(places):
    countries_per_continent = defaultdict(set)
    num_places_per_year_per_month = defaultdict(lambda: defaultdict(int))
    distinct_continents = set()
    distinct_countries = set()
    distinct_cities = set()
    distinct_places = set()
    distinct_england_counties = set()
    distinct_london_boroughs = set()
    distinct_usa_states = set()

    reverse_geo = ReverseGeoLookup()

    for place in places:
        address = reverse_geo.get_address(
            place["latitude"] / 10_000_000, place["longitude"] / 10_000_000
        )
        continent = country_code_to_continent(address.country_code)

        distinct_continents.add(continent)
        distinct_countries.add(address.country)

        if address.city:
            distinct_cities.add(address.city)

        distinct_places.add(place["name"])  # TODO add coordinates

        if address.state == "England" and (address.county or address.state_district):
            distinct_england_counties.add(address.county or address.state_district)

        if address.city == "London" and address.city_district:
            distinct_london_boroughs.add(address.city_district)

        if address.country == "United States":
            distinct_usa_states.add(address.state)

        countries_per_continent[continent].add(address.country)
        num_places_per_year_per_month[place["year"]][place["month"]] += 1

    num_countries_per_continent = {
        continent: len(countries)
        for continent, countries in countries_per_continent.items()
    }

    num_places_per_year = {
        year: sum(monthly.values())
        for year, monthly in num_places_per_year_per_month.items()
    }

    return {
        "num_continents": len(distinct_continents),
        "num_countries": len(distinct_countries),
        "num_cities": len(distinct_cities),
        "num_countries_per_continent": num_countries_per_continent,
        "num_places_per_year_per_month": num_places_per_year_per_month,
        "num_places_per_year": num_places_per_year,
        "num_places": len(distinct_places),
        "num_england_counties": len(distinct_england_counties),
        "num_london_boroughs": len(distinct_london_boroughs),
        "num_usa_states": len(distinct_usa_states),
        "continents": sorted(list(distinct_continents)),
        "countries": sorted(list(distinct_countries)),
        "countries_per_continent": {
            continent: sorted(list(countries))
            for continent, countries in countries_per_continent.items()
        },
        "cities": sorted(list(distinct_cities)),
        "places": list(distinct_places),
        "england_counties": sorted(list(distinct_england_counties)),
        "london_boroughs": sorted(list(distinct_london_boroughs)),
        "usa_states": sorted(list(distinct_usa_states)),
    }
