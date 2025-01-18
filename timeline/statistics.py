from collections import defaultdict
from dataclasses import asdict

from timeline.geography import ReverseGeoLookup, country_code_to_continent


def compute_statistics(places):
    countries_per_continent = defaultdict(set)
    num_places_per_year_per_month = defaultdict(lambda: defaultdict(int))
    distinct_continents = set()
    distinct_countries = set()
    distinct_cities = set()
    distinct_places = set()
    distinct_uk_counties = defaultdict(set)
    distinct_london_boroughs = set()
    distinct_usa_states = set()
    most_northern_place = None
    most_southern_place = None
    most_eastern_place = None
    most_western_place = None

    reverse_geo = ReverseGeoLookup()

    for place in places:
        address = reverse_geo.get_address(
            place.latitude / 10_000_000, place.longitude / 10_000_000
        )
        continent = country_code_to_continent(address.country_code)

        distinct_continents.add(continent)
        distinct_countries.add(address.country)

        if address.city:
            distinct_cities.add(address.city)

        distinct_places.add(place)

        if address.country == "United Kingdom" and (
            address.county or address.state_district
        ):
            if (
                address.state_district == "East Midlands"
                and address.city == "Nottingham"
            ):
                county = "Nottinghamshire"
            elif address.county == "Gwent":
                county = "Blaenau Gwent"
            elif address.county == "Royal Borough of Windsor and Maidenhead":
                county = "Windsor and Maidenhead"
            elif address.county == "Caerphilly County Borough":
                county = "Caerphilly"
            else:
                county = address.county or address.state_district

            distinct_uk_counties[address.state].add(county)

        if address.city == "London" and (address.city_district or address.borough):
            distinct_london_boroughs.add(address.city_district or address.borough)

        if address.city in ("City of Westminster", "City of London"):
            distinct_london_boroughs.add(address.city)

        if address.country == "United States":
            distinct_usa_states.add(address.state)

        countries_per_continent[continent].add(address.country)
        num_places_per_year_per_month[place.year][place.month] += 1

        if most_northern_place is None or place.latitude > most_northern_place.latitude:
            most_northern_place = place

        if most_southern_place is None or place.latitude < most_southern_place.latitude:
            most_southern_place = place

        if most_eastern_place is None or place.longitude > most_eastern_place.longitude:
            most_eastern_place = place

        if most_western_place is None or place.longitude < most_western_place.longitude:
            most_western_place = place

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
        "num_uk_counties": sum(
            len(counties) for counties in distinct_uk_counties.values()
        ),
        "num_london_boroughs": len(distinct_london_boroughs),
        "num_usa_states": len(distinct_usa_states),
        "continents": sorted(list(distinct_continents)),
        "countries": sorted(list(distinct_countries)),
        "countries_per_continent": {
            continent: sorted(list(countries))
            for continent, countries in countries_per_continent.items()
        },
        "cities": sorted(list(distinct_cities)),
        "places": list(asdict(place) for place in sorted(distinct_places)),
        "uk_counties": {
            state: sorted(list(counties))
            for state, counties in distinct_uk_counties.items()
        },
        "london_boroughs": sorted(list(distinct_london_boroughs)),
        "usa_states": sorted(list(distinct_usa_states)),
        "most_northern_place": asdict(most_northern_place),
        "most_southern_place": asdict(most_southern_place),
        "most_eastern_place": asdict(most_eastern_place),
        "most_western_place": asdict(most_western_place),
    }
