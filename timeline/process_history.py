from dataclasses import asdict, dataclass


@dataclass
class Place:
    year: int
    month: str
    latitude: int
    longitude: int
    name: str
    address: str = None

    def __hash__(self):
        return hash((self.latitude, self.longitude))

    def __lt__(self, other):
        return (self.latitude < other.latitude) and (self.longitude < other.longitude)


def extract_date_from_filename(filename):
    name, _ = filename.split(".")
    year, month = name.split("_")
    return int(year), month.lower()


def process_history(history):
    for filename, monthly_history in history:
        print("Processing", filename)
        year, month = extract_date_from_filename(filename)

        timeline_objects = monthly_history["timelineObjects"]
        places = (
            visit["placeVisit"] for visit in timeline_objects if "placeVisit" in visit
        )

        for place in places:
            if "name" not in place["location"]:
                continue

            yield Place(
                **{
                    "year": year,
                    "month": month,
                    "latitude": place["location"]["latitudeE7"],
                    "longitude": place["location"]["longitudeE7"],
                    "name": place["location"]["name"],
                    "address": place["location"].get("address"),
                }
            )
