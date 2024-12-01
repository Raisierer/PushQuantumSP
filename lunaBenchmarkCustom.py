from lunaSolve import solveCustomMatrix

from lunaHelper import read_json

saga_solver = {
    "name": "SAGA+",  # QAGA+ | SAGA+ | QA
    "params": {"p_size": 40, "mut_rate": 1, "rec_rate": 2},
}

qaga_solver = {
    "name": "SAGA+",  # QAGA+ | SAGA+ | QA
    "params": {"p_size": 40, "mut_rate": 1, "rec_rate": 2},
}

qa_solver = {
    "name": "QA",  # QAGA+ | SAGA+ | QA
    "params": {
        "sampling_params": {"max_answers": 200, "num_reads": 200},
        "embedding": {
            "embedding_parameters": {"max_no_improvement": 100, "tries": 100}
        },
    },
}

dataset = "glb"  # 3 | 5 | 10 | 20
lidarVectorSize = 48  # v1 = 5 | v2 = 5 | v3 = 20

solveCustomMatrix(
    solver=qa_solver,
    qubo_matrix=read_json(f"./input/qubo_{dataset}.json"),
    lidarVectorSize=lidarVectorSize,
    solutionFile=f'./output/{qa_solver["name"]}_{dataset}.json',
)
