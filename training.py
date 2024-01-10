import os
from datetime import datetime

INPUT_PATH = 'Users/mac/Downloads/UROP_2023_work/featurized_df3.p'
base_directory = '/Users/mac/Downloads/UROP_2023_work/output'

def run_training(task_name, model_id, epoches):
    dataset = load_dataset(INPUT_PATH)
    results = train_model(dataset, parameters, epoches)
    OUTPUT_PATH = generate_output_path(base_directory, task_name=task_name)
    save_model(results, OUTPUT_PATH)
    return results

def generate_output_path(task_name):
    """
    Generate an output path with the current date and time and the task name.

    :param base_directory: The base directory where the output will be saved.
    :param task_name: The name of the task.
    :return: A string representing the file path.
    """
    # Current date and time in a formatted string (e.g., '2023-03-15_16-30-00')
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create a directory path using the base directory, task name, and timestamp
    directory_path = os.path.join(base_directory, f"{task_name}_{timestamp}")

    # Optionally, create the directory if it doesn't exist
    os.makedirs(directory_path, exist_ok=True)

    # Return the directory path
    return directory_path



