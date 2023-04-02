import datetime
import json
import matplotlib.pyplot as plt
import numpy as np
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Datapoint:
    date: datetime.date
    happy: int
    meh: int
    sad: int


def parse_files(dir_path: str) -> List[dict]:
    # Get a list of all the JSON files in the directory, sorted by filename
    json_files = sorted([filename for filename in os.listdir(dir_path) if filename.endswith('.json')])

    # Loop through all the JSON files in chronological order
    data = []
    for filename in json_files:
        # Open the file and load the data as a dictionary
        with open(Path(dir_path, filename)) as file:
            json_data = json.load(file)
            if len(json_data) > 1 and len(json_data['retro']['items']) > 0:
                # Append the dictionary to the data list
                data.append(json_data)
    return data


def count_occurrences(datapoint: dict) -> Datapoint:
    results = datapoint['retro']['items']
    counts = {"happy": 0, "meh": 0, "sad": 0}
    for result in results:
        if result['category'] in counts:
            counts[result['category']] += 1

    return Datapoint(date=parse_date(results),
                     happy=counts["happy"],
                     meh=counts["meh"],
                     sad=counts["sad"])


# parse the date from the first element of the response for the week
# I know it's adhoc but the created_at and retro_item_end_time for all submissions are the same
def parse_date(results: List[dict]) -> datetime.date:
    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    return datetime.datetime.strptime(results[0]['created_at'], date_format).date()


def graph_data(cleaned_data: List[Datapoint]) -> None:
    happy_array = np.array([obj.happy for obj in cleaned_data])
    meh_array = np.array([obj.meh for obj in cleaned_data])
    sad_array = np.array([obj.sad for obj in cleaned_data])
    date_array = np.array([obj.date for obj in cleaned_data])

    # Create a new figure and set the title
    plt.figure()
    plt.title("Comparison of Happiness over time based on Postfacto cards")

    # Add a line plot for each dataset
    plt.plot(date_array, happy_array, label="Happy")
    plt.plot(date_array, meh_array, label="Meh")
    plt.plot(date_array, sad_array, label="Sad")

    # Add axis labels and a legend
    plt.xlabel("Date")
    plt.ylabel("Postfacto card count")
    plt.legend()

    # Display the plot
    plt.show()


if __name__ == "__main__":
    raw_data = parse_files("./data")
    cleaned_data = []

    for dat in raw_data:
        cleaned_data.append(count_occurrences(dat))

    graph_data(cleaned_data)
