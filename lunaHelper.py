import os
import json
import luna_sdk


def read_json(file_path):
    """
    Reads a JSON file and returns its content as a Python object.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        object: Parsed JSON data as a Python object (e.g., dict or list).

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file content is not valid JSON.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in file {file_path}: {e}")


# Example usage
# if ask_to_proceed():
#     pass
# else:
#     exit()
def ask_to_proceed(prompt="Do you want to proceed? (yes/no): "):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ['yes', 'y']:
            print("Proceeding...")
            return True
        elif choice in ['no', 'n']:
            print("Operation cancelled.")
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def write_json(solution, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(solution, f, ensure_ascii=False, default=lambda x: x.__dict__ if hasattr(x, '__dict__') else str(x), indent=4)


def ensure_directories(file_path):
    """
    Ensures all directories in the given file path exist. Creates them if necessary.

    Args:
        file_path (str): The full path to the file.

    Example:
        ensure_directories("/path/to/your/file.txt")
    """
    # Extract the directory from the file path
    directory = os.path.dirname(file_path)

    if directory:  # If there's a directory component in the path
        os.makedirs(directory, exist_ok=True)


def exportSolution(solution, output="test.json"):
    ensure_directories(output)
    write_json(solution, file_name=output)


def qpu_token_create(ls, dwave_token, name):
    try:
        # Set your token to access D-Wave's hardware
        ls.qpu_token.create(
            name=name,
            provider="dwave",
            token=dwave_token,
            token_type="personal"
        )
    except luna_sdk.exceptions.luna_server_exception.LunaServerException as e:
        print(e)


def generateMatrix(version=1, num_cols=3, P1 = 1, P2 = 2, P3 = 2):
    from data.sp_data import SPData
    from models import SPQuboBinary

    data = SPData().gen_problem(version=version, num_cols=num_cols, rad_max=2.4) 

    qubo_model_bin = SPQuboBinary(data, P1=P1, P2=P2, P3=P3)

    return qubo_model_bin.model, len(data.listLidar3D)