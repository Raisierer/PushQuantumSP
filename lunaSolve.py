import os
import time
from dotenv import load_dotenv
import luna_sdk
from luna_sdk.schemas.qpu_token import QpuToken, TokenProvider

from lunaHelper import read_json, ask_to_proceed, exportSolution

# Retrieve api and tokens from .env file
load_dotenv()
api_key = os.getenv("LUNA_API_TOKEN")
dwave_token = os.getenv("D_WAVE_TOKEN")

# Initiate the luna sdk objects
ls = luna_sdk.LunaSolve(api_key=api_key)
lq = luna_sdk.LunaQ(api_key=api_key)

# Import Input
qubo_matrix = read_json("./input/test1.json")

# Upload your QUBO to LunaSolve
optimization = ls.optimization.create_from_qubo(name="My QUBO", matrix=qubo_matrix)

try:
    # Set your token to access D-Wave's hardware
    ls.qpu_token.create(
        name="PushQuantumDWaveToken",
        provider="dwave",
        token=dwave_token,
        token_type="personal"
    )
except luna_sdk.exceptions.luna_server_exception.LunaServerException as e:
    print(e)

print("Ready to start quantum computing!")

# Example usage
if ask_to_proceed():
    pass
else:
    exit()

# Solve the QUBO using the QAGA+ algorithm and retrieve a job
job = ls.solution.create(
    optimization_id=optimization.id,
    solver_name="QAGA+",
    provider="dwave",
    qpu_tokens=TokenProvider(
        dwave=QpuToken(
            source="personal",
            name="PushQuantumDWaveToken"
        )
    ),
    solver_parameters={
        'p_size': 40,
        'mut_rate': 1,
        'rec_rate': 2
    }
)

# After the execution of your algorithm has been finished, retrieve your solution
solution = None
running = True

while running:
    solution = ls.solution.get(job.id)
    running = True if solution.status == "IN_PROGRESS" or solution.status == "REQUESTED" or solution.status == "CREATED" else False
    print("Status: " + str(solution.status), end="\r")
    time.sleep(2)

print(solution.head)

# Store solution

exportSolution(solution=solution, folder_name="output")

# Display best result
best_result = ls.solution.get_best_result(solution)
print(best_result)
