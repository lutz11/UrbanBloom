import os

import pandas as pd


class FileOps:

    def __init__(self):
        self.project_dir = os.path.dirname(os.path.dirname(__file__))

    def get_dataset_path(self, csv_file):
        return os.path.join(self.get_dataset_dir(), csv_file)

    def file_exists_in_project(self, relative_file_path):
        destination_path = os.path.join(self.project_dir, relative_file_path)
        return os.path.exists(destination_path)

    @staticmethod
    def append_path(path, filename):
        return os.path.join(path, filename)

    @staticmethod
    def get_output_dir():
        project_path = get_project_directory()
        target_path = os.path.join(project_path, "output")
        return target_path

    @staticmethod
    def get_dataset_dir():
        project_path = get_project_directory()
        target_path = os.path.join(project_path, "datasets")
        return target_path

    @staticmethod
    def get_project_dir():
        return get_project_directory()

    @staticmethod
    def open_file(absolute_file_path):
        if not os.path.exists(absolute_file_path):
            return None
        with open(absolute_file_path, 'r') as file:
            content = file.read()
            if content is None:
                print("Could not open file")
                return None
            return file

    @staticmethod
    def find_file_from_column(column_name):
        # iterate over files and check if file contains the column.
        for file in os.listdir(get_dataset_directory()):
            filepath = os.path.join(get_dataset_directory(), file)
            temp_df = pd.read_csv(filepath)
            try:
                if column_name in temp_df.columns:
                    print(f"Found {column_name} in {filepath}")
                    return filepath
            except KeyError:
                print(f"Could not find {column_name} in {filepath}")
                continue

        return None

# Helper function
def get_project_directory():
    current_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(current_path)
    return parent_path

def get_output_directory():
    project_path = get_project_directory()
    target_path = os.path.join(project_path, "output")
    return target_path

def get_dataset_directory():
    project_path = get_project_directory()
    target_path = os.path.join(project_path, "datasets")
    return target_path
