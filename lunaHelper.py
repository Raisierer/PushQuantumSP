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
    # output_folder_path = os.path.join(os.getcwd(), folder_name)
    # os.makedirs(output_folder_path, exist_ok=True)

    ensure_directories(output)

    # file_path = os.path.join(output_folder_path, f'{solution.created_date.strftime("%Y-%m-%d_%H-%M-%S")}_solution.json')

    write_json(solution, file_name=output)


def qpu_token_create(ls, dwave_token):
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
