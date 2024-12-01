import json
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import os


# Function to create radar chart
def create_radar_chart(data, categories, title):
    N = len(categories)

    # Compute angle for each category
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # Close the plot

    # Initialize the radar chart
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Loop through each data series
    for label, values in data.items():
        values += values[:1]  # Close the plot
        ax.plot(angles, values, linewidth=2, linestyle="solid", label=label)
        ax.fill(angles, values, alpha=0.25)

    # Add labels for each category
    plt.xticks(angles[:-1], categories)

    # Add title and legend
    plt.title(title, size=20, color="blue", y=1.1)
    ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))

    plt.show()


def readJSON(file):
    with open(file, "r") as f:
        return json.load(f)


def loadData(files, filesFolder):
    return [readJSON(os.path.join(filesFolder, file)) for file in files]


# Example JSON structure:
# {
#     "categories": ["Category1", "Category2", "Category3", "Category4"],
#     "data": {
#         "Series1": [4, 2, 5, 3],
#         "Series2": [3, 4, 2, 5]
#     }
# }


filesFolder = "../output/generated"
files = [
    "v1-c3-1-2-0.5-QA.json",
    "v1-c3-1-2-0.5-QAGA+.json",
    "v1-c3-1-2-0.5-SAGA+.json",
]

data = loadData(files, filesFolder)

# categories = [d["solver"] for d in data]
#
# dataseries = {}
#
# for d in data:
#     dataseries[d["id"]] = [r["obj_value"] for r in d["results"]]

categories = (["Category1", "Category2", "Category3", "Category4"],)
dataseries = {"Series1": [4, 2, 5, 3], "Series2": [3, 4, 2, 5]}

print(categories)
print(dataseries)

title = "Radar Chart Example"

create_radar_chart(dataseries, categories, title)
