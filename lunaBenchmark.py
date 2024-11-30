from lunaSolve import solve

from lunaHelper import read_json

solver = "SAGA+" # QAGA+ | SAGA+ | QA
dataset = "v2c20"
lidarVectorSize = 20 # v1 = 5 | v2 = 5 | v3 = 20

solve(solver=solver, qubo_matrix=read_json(f'./input/qubo_{dataset}.json'), solver_parameters={
            'p_size': 40,
            'mut_rate': 1,
            'rec_rate': 2
        }, lidarVectorSize=lidarVectorSize, solutionFile=f'./output/{solver}_{dataset}.json')