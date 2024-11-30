import os
from dotenv import load_dotenv
import luna_sdk

# Retrieve api and tokens from .env file
load_dotenv()
api_key = os.getenv("LUNA_API_TOKEN")
dwave_token = os.getenv("D_WAVE_TOKEN")

# Initiate the luna sdk objects
ls = luna_sdk.LunaSolve(api_key=api_key)
lq = luna_sdk.LunaQ(api_key=api_key)



# Define the problem type
problem_name = "qubo"

# Define the dataset
dataset = {
    "qubo_00": {
        problem_name: [
            [2, 1],
            [1, 2]
        ]
    },
    "qubo_01": {
        problem_name: [
            [-2, 3],
            [3, -2]
        ]
    },
    "qubo_02": {
        problem_name: [
            [2, 1, 0],
            [1, 2, 1],
            [0, 1, 2]
        ]
    },
}
