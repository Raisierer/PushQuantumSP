import os
import time
from dotenv import load_dotenv
import luna_sdk
from luna_sdk.schemas.qpu_token import QpuToken, TokenProvider

from lunaHelper import read_json, exportSolution, qpu_token_create

def lunaSolve(solver, qubo_matrix, solver_parameters):
    print("Setting up the job..")
    # Retrieve api and tokens from .env file
    load_dotenv()
    api_key = os.getenv("LUNA_API_TOKEN")
    dwave_token = os.getenv("D_WAVE_TOKEN")

    # Initiate the luna sdk objects
    ls = luna_sdk.LunaSolve(api_key=api_key)
    lq = luna_sdk.LunaQ(api_key=api_key)

    # Upload your QUBO to LunaSolve
    optimization = ls.optimization.create_from_qubo(name="My QUBO", matrix=qubo_matrix)

    # Create Token for d-wave if not already done
    qpu_token_create(ls, dwave_token)

    print("Ready to start quantum computing!")

    # Solve the QUBO using the QAGA+ algorithm and retrieve a job
    job = ls.solution.create(
        optimization_id=optimization.id,
        solver_name=solver,
        provider="dwave",
        qpu_tokens=TokenProvider(
            dwave=QpuToken(
                source="personal",
                name="PushQuantumDWaveToken"
            )
        ),
        solver_parameters=solver_parameters
    )

    # After the execution of your algorithm has been finished, retrieve your solution
    solution = None
    running = True

    while running:
        solution = ls.solution.get(job.id)
        running = True if solution.status == "IN_PROGRESS" or solution.status == "REQUESTED" or solution.status == "CREATED" else False
        print("Status: " + str(solution.status), end="\r")
        time.sleep(2)

    # Store solution
    exportSolution(solution=solution, folder_name="output")

lunaSolve("QAGA+", read_json("./input/test/qubo_00.json"), {
            'p_size': 40,
            'mut_rate': 1,
            'rec_rate': 2
        })