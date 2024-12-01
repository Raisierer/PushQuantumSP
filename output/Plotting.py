import os
import json
import time
import matplotlib.pyplot as plt
from math import pi

# Directory where JSON files are located
input_directory = r"C:/Users/vishn/PushQuantumSP"

# Helper function to read JSON data and extract values
def read_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    # Extract objective values
    obj_values = [sample["obj_value"] for sample in data["results"]]
    return obj_values

# Function to plot radial graph
def plot_radial(data_dict, title, save_path):
    categories = list(data_dict.keys())
    num_vars = len(categories)
    
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]  # Complete the circle
    
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    
    # Draw one axis per variable and add labels
    plt.xticks(angles[:-1], categories)
    
    # Plot data and fill
    for label, values in data_dict.items():
        values += values[:1]  # Complete the circle
        ax.plot(angles, values, label=label)
        ax.fill(angles, values, alpha=0.25)
    
    plt.title(title, size=15, y=1.1)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.savefig(save_path)
    plt.close()

# Initialize variables
time_taken = {}
v_groups = {}
c_groups = {}

# Start processing JSON files
start_time = time.time()
for filename in sorted(os.listdir(input_directory)):
    if filename.endswith(".json"):
        file_path = os.path.join(input_directory, filename)
        # Measure time for processing each file
        file_start = time.time()
        
        obj_values = read_json(file_path)
        
        # Parse filename to extract v and c values (assumes format vXcY.json)
        base_name = os.path.splitext(filename)[0]
        v_index = base_name.index('v')
        c_index = base_name.index('c')
        v_key = base_name[:c_index]  # Extract v group (e.g., v1, v2)
        c_key = base_name[c_index:]  # Extract c group (e.g., c3, c5)
        
        # Add to v_groups and c_groups
        if v_key not in v_groups:
            v_groups[v_key] = {}
        if c_key not in c_groups:
            c_groups[c_key] = {}
        
        v_groups[v_key][c_key] = obj_values
        c_groups[c_key][v_key] = obj_values
        
        # Store time taken for this file
        time_taken[filename] = time.time() - file_start

# Output directory for plots
output_directory = os.path.join(os.getcwd(), "Graphs")
os.makedirs(output_directory, exist_ok=True)

# Plot v-groups (changing c)
for v_key, data in v_groups.items():
    save_path = os.path.join(output_directory, f"{v_key}_radial_plot.png")
    plot_radial(data, f"Radial Plot for {v_key} (Changing c)", save_path)

# Plot c-groups (changing v)
for c_key, data in c_groups.items():
    save_path = os.path.join(output_directory, f"{c_key}_radial_plot.png")
    plot_radial(data, f"Radial Plot for {c_key} (Changing v)", save_path)

# Print total time taken for each file
print("Processing Times:")
for file, duration in time_taken.items():
    print(f"File: {file} - Time Taken: {duration:.2f} seconds")

# Print total time for entire processing
total_time = time.time() - start_time
print(f"\nTotal Time Taken for All Files: {total_time:.2f} seconds")

