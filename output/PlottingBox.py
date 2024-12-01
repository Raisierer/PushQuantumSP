import matplotlib.pyplot as plt
import numpy as np
import os
import json


def readJSON(file):
    with open(file, "r") as f:
        return json.load(f)


def loadData(files, filesFolder):
    return [readJSON(os.path.join(filesFolder, file)) for file in files]

filesFolder = "./generated"
files = [
    "v2-c5-1-2-2-QA.json",
    "v2-c5-1-2-2-QAGA+.json",
    "v2-c5-1-2-2-SAGA+.json",
]

data = loadData(files, filesFolder)

categories = [d["solver"] for d in data]
dataseries = []
for d in data:
    dataseries.append([r["obj_value"] for r in d["results"]])


print(categories)
print(dataseries)

print(f"Number of datasets: {len(dataseries)}")
print(f"Number of labels: {len(categories)}")


# Create the box plot
plt.figure(figsize=(10, 6))
plt.(
    dataseries,
    labels=categories,
    patch_artist=True,
)

# Customizing the plot
plt.title("Performance of Different Algorithms", fontsize=16)
plt.ylabel("Performance Metric", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

# Show the plot
plt.show()
