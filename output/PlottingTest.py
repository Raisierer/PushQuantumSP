import numpy as np
import matplotlib.pyplot as plt
import json
import os

exampleName = "v3-c20-1-2-0.25"


def readJSON(file):
    with open(file, "r") as f:
        return json.load(f)


def loadData(files, filesFolder):
    return [readJSON(os.path.join(filesFolder, file)) for file in files]


filesFolder = "./generated"
files = [
    # "v2-c5-1-2-2-QA.json",
    # "v2-c5-1-2-2-QAGA+.json",
    # "v2-c5-1-2-2-SAGA+.json",
    f"{exampleName}-QA.json",
    f"{exampleName}-QAGA+.json",
    f"{exampleName}-SAGA+.json",
]

dataRead = loadData(files, filesFolder)

algorithms = [d["solver"] for d in dataRead]
dataseries = []
for d in dataRead:
    dataseries.append([r["obj_value"] for r in d["results"]])


# Generate sample data for algorithms
np.random.seed(42)
# sample_runs = 182

# Simulate obj_values for each algorithm (mean and stddev can be adjusted per algorithm)
data = {}  # {"Algorithm": {"Objective Value": [], "sample_size": 0}}

for d in dataRead:
    obj_values = [r["obj_value"] for r in d["results"]]
    sample_size = len(d["results"])

    for run, value in enumerate(obj_values):
        data[d["solver"]] = {"obj_values": obj_values, "sample_size": sample_size}

# Create the plot
plt.figure(figsize=(12, 6))
for algorithm in data.items():
    plt.plot(
        range(1, algorithm[1]["sample_size"] + 1),
        algorithm[1]["obj_values"],
        marker="o",
        label=algorithm[0],
    )

plt.plot(range(1, 201), 11 * np.ones(200), marker="+", label="Ground Truth")

# Customize the plot
plt.title(exampleName, fontsize=16)
plt.xlabel("Sample Run", fontsize=12)
plt.ylabel("Objective Value", fontsize=12)
plt.legend(title="Algorithms", fontsize=10)
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.savefig(f"./newPlots/{exampleName}.png")
plt.show()
