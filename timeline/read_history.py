import json
import os


def read_history(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.startswith("."):
                continue

            with open(os.path.join(root, file), "r") as f:
                yield file, json.loads(f.read())
