import os
import time
from dotenv import load_dotenv
import luna_sdk
from luna_sdk.schemas.qpu_token import QpuToken, TokenProvider
import numpy as np

from lunaHelper import generateMatrix, read_json, exportSolution, qpu_token_create


def solveCustomMatrix(solver, qubo_matrix, lidarVectorSize, solutionFile):
    print("Setting up the job..")
    # Retrieve api and tokens from .env file
    load_dotenv()
    api_key = os.getenv("LUNA_API_TOKEN")
    dwave_token = os.getenv("D_WAVE_TOKEN")
    dwaveTokenName = os.getenv("D_WAVE_TOKEN_NAME")

    # Initiate the luna sdk objects
    ls = luna_sdk.LunaSolve(api_key=api_key)
    lq = luna_sdk.LunaQ(api_key=api_key)

    # Upload your QUBO to LunaSolve
    optimization = ls.optimization.create_from_qubo(name="My QUBO", matrix=qubo_matrix)

    # Create Token for d-wave if not already done
    qpu_token_create(ls, dwave_token, dwaveTokenName)

    print("Ready to start quantum computing!")

    # Solve the QUBO using the QAGA+ algorithm and retrieve a job
    job = ls.solution.create(
        optimization_id=optimization.id,
        solver_name=solver["name"],
        provider="dwave",
        qpu_tokens=TokenProvider(
            dwave=QpuToken(source="personal", name=dwaveTokenName)
        ),
        solver_parameters=solver["params"],
    )

    # After the execution of your algorithm has been finished, retrieve your solution
    solution = None
    running = True

    while running:
        solution = ls.solution.get(job.id)
        running = (
            True
            if solution.status == "IN_PROGRESS"
            or solution.status == "REQUESTED"
            or solution.status == "CREATED"
            else False
        )
        print("Status: " + str(solution.status), end="\r")
        time.sleep(2)
    print(end="\r")
    print("Done computing!                     ")

    try:
        # Recalculate the objective value
        for result in solution.results:
            sorted_samples = {key: result.sample[key] for key in sorted(result.sample)}
            # x_values = np.array([x for x in sorted_samples.values()])
            # print(x_values)
            # print(np.array(qubo_matrix))

            # error_value = x_values.T @ np.array(qubo_matrix) @ x_values

            obj_val = sum([sorted_samples[f"x{ind}"] for ind in range(lidarVectorSize)])

            # print(f"Equal? {error_value} == {obj_val}")

            # sum = 0
            # for i in range(lidarVectorSize):
            #    sum = sum + result.sample["x"+str(i)]
            if result.feasible:
                result.obj_value = obj_val
            else:
                result.obj_value = lidarVectorSize + 1

        # Sort the results according to the new objective value
        solution.results.sort(key=lambda x: x.obj_value)

        # Store solution
        exportSolution(solution=solution, output=solutionFile)
        print("Exported solution!")
    except Exception as e:
        print(e)
        print("Error!!")
        print(solution)


def solveGeneratedMatrix(solver, version=1, num_cols=3, P1=1, P2=2, P3=3):
    filename = f'./output/generated/v{version}-c{num_cols}-{P1}-{P2}-{P3}-{solver["name"]}.json'

    if os.path.exists(filename):
        print("Already calculated. Skipping.")
        return

    qubo_matrix, lidarVectorSize = generateMatrix(version, num_cols, P1, P2, P3)
    solveCustomMatrix(
        solver,
        qubo_matrix=qubo_matrix,
        lidarVectorSize=lidarVectorSize,
        solutionFile=filename,
    )


if __name__ == "__main__":
    solveCustomMatrix(
        solver="QAGA+",
        qubo_matrix=read_json("./input/test/qubo_00.json"),
        solver_parameters={"p_size": 40, "mut_rate": 1, "rec_rate": 2},
        lidarVectorSize=5,
        solutionFile="./output/test/MySolution.json",
    )
