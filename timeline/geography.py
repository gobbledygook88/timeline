import inspect
import json
import os
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from dataclasses import dataclass
import pycountry_convert as pc

CACHE_FILE = "geolookup_cache.json"

NOMINATIM_USER_AGENT = os.getenv("NOMINATIM_USER_AGENT")
if not NOMINATIM_USER_AGENT:
    raise ValueError("Please set the NOMINATIM_USER_AGENT environment variable")


@dataclass
class Address:
    house_number: str = None
    road: str = None

    neighbourhood: str = None
    suburb: str = None
    quarter: str = None
    borough: str = None
    village: str = None

    city_district: str = None
    county: str = None

    city: str = None
    province: str = None

    state: str = None
    state_district: str = None

    postcode: str = None

    country: str = None
    country_code: str = None

    @classmethod
    def from_dict(cls, env):
        return cls(
            **{k: v for k, v in env.items() if k in inspect.signature(cls).parameters}
        )


class ReverseGeoLookup:
    def __init__(self):
        self.geolocator = Nominatim(user_agent=NOMINATIM_USER_AGENT)
        self.reverse = RateLimiter(self.geolocator.reverse, min_delay_seconds=1)
        self.cache = self.load_cache()

    def load_cache(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_cache(self):
        with open(CACHE_FILE, "w") as f:
            json.dump(self.cache, f)

    def get_address(self, latitude, longitude):
        key = f"{latitude},{longitude}"

        if key in self.cache:
            return Address.from_dict(self.cache[key])

        location = self.reverse((latitude, longitude), language="en")
        address = location.raw["address"]

        self.cache[key] = address
        self.save_cache()

        return Address.from_dict(address)


def country_code_to_continent(country_code):
    try:
        country_alpha2 = country_code.upper()
        continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        continent_name = pc.convert_continent_code_to_continent_name(continent_code)
        return continent_name
    except KeyError:
        return None
