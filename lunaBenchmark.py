from lunaSolve import lunaSolve

from lunaHelper import read_json

solver = "QAGA+" # QAGA+ | SAGA+ | QA
dataset = "v1c3"
lidarVectorSize = 5 # v1 = 5 | v2 = 5 | v3 = 10

lunaSolve(solver="QAGA+", qubo_matrix=read_json(f'./input/qubo_{dataset}.json'), solver_parameters={
            'p_size': 40,
            'mut_rate': 1,
            'rec_rate': 2
        }, lidarVectorSize=lidarVectorSize, solutionFile=f'./output/{solver}_{dataset}.json')