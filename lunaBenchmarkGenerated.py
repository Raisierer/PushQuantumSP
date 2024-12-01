from lunaSolve import solveGeneratedMatrix

saga_solver = {"name": "SAGA+", "params": {"p_size": 40, "mut_rate": 1, "rec_rate": 2}}

qaga_solver = {"name": "QAGA+", "params": {"p_size": 40, "mut_rate": 1, "rec_rate": 2}}

qa_solver = {
    "name": "QA",
    "params": {
        "sampling_params": {"max_answers": 200, "num_reads": 200},
        "embedding": {
            "embedding_parameters": {"max_no_improvement": 100, "tries": 100}
        },
    },
}

solver = [qa_solver, qaga_solver, saga_solver]
version = [1, 2, 3]
num_cols = [3, 5, 10, 20]
P1 = 1
P2 = 2
P3 = [0.25, 0.5, 1, 2]

for s in solver:
    print("Using solver: ", s)
    print("---------------")
    for v in version:
        print("Using version: ", v)
        print("---------------")
        for n in num_cols:
            print("Using num_cols: ", n)
            print("---------------")
            for p in P3:
                print("Using P3: ", p)
                print("---------------")
                solveGeneratedMatrix(
                    solver=s, version=v, num_cols=n, P1=P1, P2=P2, P3=p
                )
                print("Done.")
