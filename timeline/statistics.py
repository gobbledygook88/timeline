from collections import defaultdict

from timeline.geography import ReverseGeoLookup, country_code_to_continent


def compute_statistics(places):
    countries_per_continent = defaultdict(set)
    num_places_per_year_per_month = defaultdict(lambda: defaultdict(int))
    distinct_continents = set()
    distinct_countries = set()
    distinct_cities = set()
    distinct_places = set()

    reverse_geo = ReverseGeoLookup()

    for place in places:
        address = reverse_geo.get_address(
            place["latitude"] / 10_000_000, place["longitude"] / 10_000_000
        )
        continent = country_code_to_continent(address.country_code)

        distinct_continents.add(continent)
        distinct_countries.add(address.country)
        distinct_cities.add(address.city)  # TODO ignore None
        distinct_places.add(place["name"])  # TODO add coordinates

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
        "continents": list(distinct_continents),
        "countries": list(distinct_countries),
        "countries_per_continent": {
            continent: list(countries)
            for continent, countries in countries_per_continent.items()
        },
        "cities": list(distinct_cities),
        "places": list(distinct_places),
    }
