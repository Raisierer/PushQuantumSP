import os
import numpy as np
import matplotlib.pyplot as plt

from lunaSolve import solveCustomMatrix

# from dotenv import load_dotenv

# import luna_sdk
# from use_case import get_active_edges


# Example input. Parameters will be injected here by aqora
input = (
    # V_L
    np.array([1, 1, 1, 1, 1, 1], dtype=np.int8),
    # V_S
    np.array([1, 1, 1, 1, 1], dtype=np.int8),
    # Edges (L x S)
    np.array(
        [
            [0, 1, 1, 1, 0],
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
        ],
        dtype=np.int8,
    ),
)


V_L, V_S, edges = input


# Set blocking to True to pause `aqora test` execution until the plot is closed
def plt_bipartite_graph(V_L, V_S, edges, block=False):
    # Set up positions for nodes in the two sets
    x_l = np.zeros(len(V_L))  # x-coordinates of the first set
    y_l = np.linspace(0, 1, len(V_L))  # y-coordinates of the first set
    x_s = np.ones(len(V_S))  # x-coordinates of the second set
    y_s = np.linspace(0, 1, len(V_S))  # y-coordinates of the second set

    # Plot the nodes
    plt.scatter(
        x_l[V_L.nonzero()], y_l[V_L.nonzero()], color="green", label="V_L active"
    )
    plt.scatter(
        x_l[np.nonzero(V_L == 0)],
        y_l[np.nonzero(V_L == 0)],
        color="red",
        label="V_L inactive",
    )
    plt.scatter(x_s, y_s, color="blue", label="V_S")

    # Plot the edges
    for i in range(len(V_L)):
        for j in range(len(V_S)):
            if (
                edges[i, j] == 1
            ):  # There's an edge between node i in Set 1 and node j in Set 2
                plt.plot(
                    [x_l[i], x_s[j]],
                    [y_l[i], y_s[j]],
                    color="gray",
                    linestyle="-",
                    linewidth=1,
                )

    # Add labels and legend
    plt.title("Bipartite Graph")
    plt.legend()
    plt.axis("off")
    plt.show(block=block)


plt_bipartite_graph(V_L, V_S, edges)


# Insert your code here
from data.sp_data import SPData
from models.sp_qubo_binary import QuboSPBinary
from networkx import Graph
from networkx.classes.reportviews import NodeView
import networkx as nx
import math
from numpy.typing import NDArray

graph = Graph()

for idx, lidar in enumerate(V_L):
    graph.add_node(f"ld{idx}", pos=(0, idx), type="lidar")

for idx, streetpoint in enumerate(V_S):
    graph.add_node(f"sp{idx}", pos=(2, idx), type="streetpoint")

for row in range(len(V_L)):
    for col in range(len(V_S)):
        if edges[row, col] == 1:
            graph.add_edge(f"ld{row}", f"sp{col}")

plt.clf()
pos = {node: graph.nodes[node]["pos"] for node in graph.nodes}
nx.draw(graph, pos=pos)
plt.savefig("./test.png")

lidar_points = []
streetpoints = []

for node in graph.nodes:
    match graph.nodes[node]["type"]:
        case x if "lidar" in x:
            lidar_points.append(node)
        case x if "streetpoint" in x:
            streetpoints.append(node)

# Calc q shape
# naive approach: Z = len(V_L) - 1
size = len(V_L)
limit_s = 1000
s_list = []
s_size = 0

used_lidars = []
mandatory_lidars = []

for point in streetpoints:
    deg = len(graph.adj[point].items())
    bits = int(math.ceil(math.log2(deg))) if deg < limit_s else limit_s

    lidar_per_sp = []
    for ls in graph.adj[point].items():
        lidar_per_sp.append(ls[0])
        used_lidars.append(ls[0])
        if bits == 0:
            mandatory_lidars.append(ls[0])

    s_list.append([lidar_per_sp, {s_size + i + 1: 2**i for i in range(bits)}])
    s_size += bits

used_lidars = list(set(used_lidars))
idx_list = list(range(len(used_lidars)))
used_lidars_idx = dict(zip(used_lidars, idx_list))

for s in s_list:
    if s[1]:
        s[1] = {key + len(used_lidars) - 1: -value for key, value in s[1].items()}

size += s_size

# Calc Q
Q = np.zeros((size, size))
P1 = 1
P2 = 2
P3 = 2


for i in range(0, len(used_lidars)):
    Q[i, i] = P1
    if used_lidars[i] in mandatory_lidars:
        Q[i, i] -= P2

for s in s_list:
    if s[1]:
        sdict = s[1]
        ldict = {}
        for l in s[0]:
            ldict[used_lidars_idx[l]] = 1
        ldict.update(sdict)

        for i in ldict:
            Q[i, i] -= 2 * P3 * ldict[i]
            for j in ldict:
                Q[i, j] += P3 * ldict[i] * ldict[j]

# def to_binary(value) -> np.NDArray[np.int8]:
#    bits = math.floor(math.log2(value))
#    np.zeros((bits,))
#    for k in range()

# Main diagonal
# for i in range(len(V_L)):
#    Q[i,i] = 1

# print(len(lidar_points))
# print(len(streetpoints))
# print(s_idx)

# def int_to_binary(value, max_size) -> NDArray[np.int8]:
#    bin_array = np.zeros(max_size, dtype=np.int8)
#    bin_str = bin(value)
#    for idx, b in enumerate(bin_str[2:]):
#        bin_array[idx] = b
#    return bin_array

# point: NodeView
# for point in streetpoints:
#    neighbours = list(graph.neighbors(point))
#    print(f"neighbours: {list(neighbours)}")

# A = np.zeros((len(V_L), len(V_L)))
# for n in range(len(V_L)):
#    for m in range(len(V_L)):
#        A[n,m] += 1 if f"ld{n}" in neighbours and f"ld{m}" in neighbours else 0
#
#    print(f"A = {A}")
#    Q[0:len(V_L), 0:len(V_L)] += A
#
#    C = np.zeros((size-len(V_L), size - len(V_L)))
#    for k in range(size-len(V_L)):
#        for l in range(size-len(V_L)):
#            C[k, l] -= 1
#    Q[len(V_L):size, len(V_L):size] += C
#
#    B = np.zeros((len(V_L), size - len(V_L)))
##    for y in range(len(V_L)):
#        for x in range(size - len(V_L)):
#            B[y,x] -= 1
#    Q[len(V_L):size, size - len(V_L):size] -= B.T
#    Q[size - len(V_L):size, len(V_L):size] -= B

print(Q)

solveCustomMatrix(
    solver={"name": "SAGA+", "params": {"p_size": 40, "mut_rate": 1, "rec_rate": 2}},
    qubo_matrix=Q,
    lidarVectorSize=len(V_L),
    solutionFile="./submission/solution.json",
)


# We do a trivial solution for the example input
V_L[2:] = 0

# plt_bipartite_graph(V_L, V_S, get_active_edges(V_L, V_S, edges))
