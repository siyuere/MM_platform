import os
import pickle
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

INPUT_PATH = 'Users/mac/Downloads/UROP_2023_work/featurized_df_mn_ac_pd_pb.p'
base_directory = '/Users/mac/Downloads/UROP_2023_work/output'


def train_model(dataset, model_name, parameters, epoches, output_path):
    if "RandomForestClassifier" in model_name:
        model = RandomForestClassifier(random_state=1, min_samples_split=5, max_depth=None, min_samples_leaf=2)

    X = dataset.drop(['structure', "composition", 'oxi_state', 'site_symbol','site_composition','structure_idx', 'site_idx'], axis = 1)
    y = dataset['oxi_state'].values

    accuracy = cross_val_score(model, X, y, scoring='accuracy', cv=5)
    model.fit(X, y)
    pickle.dump(model, output_path)

    return accuracy


def run_training(task_id, model_name, parameters, epochs, output_path):
    with open(INPUT_PATH, 'rb') as file:
        dataset = pickle.load(file)

    results = train_model(dataset, model_name, parameters, epochs, output_path=output_path)

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

def predict(model_path, structure):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    x = structure.drop(['structure', "composition", 'site_symbol','site_composition', 'site_idx'], axis = 1)
    y = model.predict(x)
    return y.tolist()



