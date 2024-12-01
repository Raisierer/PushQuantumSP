import json
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# Load and process JSON data
def load_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
    # Assuming we're extracting the first `sample` from `results` for comparison
    return data['results'][0]['sample']

def plot_combined_radar_chart(files, labels):
    datasets = [load_json(file) for file in files]

    # Radar chart setup
    categories = list(datasets[0].keys())
    num_vars = len(categories)
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    for dataset, label in zip(datasets, labels):
        values = list(dataset.values())
        values += values[:1]
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=label)
        ax.fill(angles, values, alpha=0.25)

    # Add labels and legend
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["25%", "50%", "75%", "100%"], color="gray", size=8)
    ax.set_ylim(0, 1)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.title("Radar Chart Comparison", size=16, weight='bold', y=1.1)
    plt.show()

files = ['v1-c5-1-2-0.5-QA.json','v1-c5-1-2-0.5-QAGA+.json', 'v1-c5-1-2-0.5-SAGA+.json']
labels = ['QA', 'QAGA+', 'SAGA+']
plot_combined_radar_chart(files, labels)