'''Qalculate the Q-Matrix for the QUDO-Problem.
'''


import numpy as np
from numpy.typing import NDArray
from data.sp_data_rework import SPData
import math

from networkx.classes.reportviews import NodeView
from networkx import Graph

def get_state_len(graph: Graph, limit_s=1000) -> int:
    nodes = graph.nodes
    size = 0
    node: NodeView
    for node in nodes:
        ty = nodes[node]["type"]
        match ty:
            case x if "lidar" in x:
                size += 1
                continue
            case x if "streetpoint" in x:
                pass
            case _: 
                continue

        deg = len(graph.adj[node].items())

        # add num of bits needed to state
        size += int(math.ceil(math.log2(deg))) if deg < limit_s else limit_s

    return size

def get_qubo_matrix(data: SPData, penalty: int) -> NDArray[np.int64]:
    nodes = data.G.nodes
    
    state_len = get_state_len(data.G)

    Q = np.zeros((state_len, state_len), dtype=np.int64)
        
    node: NodeView
    for node in nodes:
        # Skip all non-street point nodes
        #match 
        pass
        
        

    return Q