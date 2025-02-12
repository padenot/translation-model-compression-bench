#!/usr/bin/python3

import json
import re
import matplotlib.pyplot as plt
import numpy as np
import os

compressed_dir = "compressed_output"

file_sizes = {}
for file in os.listdir(compressed_dir):
    match = re.search(r'model\.(.*?)\.intgemm\.alphas\.bin\.([a-z0-9]+)\.(\d+)', file)
    if match:
        model, compression, level = match.groups()
        key = f"{compression}.{level}"
        if model == "jaen":
            key += ".jaen"
        file_sizes[key] = os.path.getsize(os.path.join(compressed_dir, file))
    # brotli has different extension
    match = re.search(r'model\.(.*?)\.intgemm\.alphas\.bin\.(\d+)\.([a-z0-9]+)', file)
    if match:
        model, level, compression = match.groups()
        print(model, level, compression)
        key = f"{compression}.{level}"
        if model == "jaen":
            key += ".jaen"
        file_sizes[key] = os.path.getsize(os.path.join(compressed_dir, file))

with open('benchmark_results/decompression_results.json', 'r') as file:
    data = json.load(file)

sizes = []
times = []
labels = []
commands = []
levels = []

for entry in data['results']:
    match = re.search(r'\.([a-z0-9]+)\.([0-9]+)', entry['command'])
    if match:
        key = f"{match.group(1)}.{match.group(2)}"
        if "jaen" in entry['command']:
            key += ".jaen"
        size = file_sizes.get(key, None)
        if size:
            sizes.append(size)
            times.append(entry['mean'])
            commands.append(entry['command'].split()[0])
            levels.append(match.group(2))
            labels.append(f"{entry['command'].split()[0]}-{match.group(2)}")
    # brotli has different extension
    match = re.search(r'\.([0-9]+)\.br', entry['command'])
    if match:
        key = f"br.{match.group(1)}"
        if "jaen" in entry['command']:
            key += ".jaen"
        size = file_sizes.get(key, None)
        if size:
            sizes.append(size)
            times.append(entry['mean'])
            commands.append(entry['command'].split()[0])
            levels.append(match.group(1))
            labels.append(f"{entry['command'].split()[0]}-{match.group(1)}")
    # snz has different extension
    match = re.search(r'\.([0-9]+)\.snz', entry['command'])
    if match:
        key = f"snz.{match.group(1)}"
        if "jaen" in entry['command']:
            key += ".jaen"
        size = file_sizes.get(key, None)
        if size:
            sizes.append(size)
            times.append(entry['mean'])
            commands.append(entry['command'].split()[0])
            levels.append(match.group(1))
            labels.append(f"{entry['command'].split()[0]}-{match.group(1)}")


unique_commands = list(set(commands))
colors = plt.cm.tab10(np.linspace(0, 1, len(unique_commands)))
command_color_map = {cmd: colors[i] for i, cmd in enumerate(unique_commands)}

# Plot data
plt.figure(figsize=(10, 6))
for i in range(len(sizes)):
    plt.scatter(sizes[i], times[i], color=command_color_map[commands[i]], label=commands[i] if commands[i] not in plt.gca().get_legend_handles_labels()[1] else "")
    plt.annotate(labels[i], (sizes[i], times[i]), textcoords="offset points", xytext=(5,5), ha='right')

plt.xlabel('Compressed Size (bytes)')
plt.ylabel('Decompression Time (s)')
plt.title('Decompression Time vs Compressed Size')
plt.legend(title="Command")
plt.grid(True)
plt.show()
