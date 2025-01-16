from argparse import ArgumentParser
import json
import os

from timeline.process_history import process_history
from timeline.read_history import read_history
from timeline.statistics import compute_statistics


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--takeout-dir", type=str, required=True)
    args = parser.parse_args()

    takeout_dir = args.takeout_dir
    location_history_dir = os.path.join(
        takeout_dir, "Location History (Timeline)", "Semantic Location History"
    )

    if not os.path.exists(location_history_dir):
        raise FileNotFoundError(f"The location directories are not as expected.")

    history = read_history(location_history_dir)
    processed_history = process_history(history)
    statistics = compute_statistics(processed_history)

    with open("timeline_statistics.json", "w") as f:
        f.write(json.dumps(statistics))
