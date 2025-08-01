import os

class FileOps:

    def __init__(self):
        self.project_dir = FileOps.get_project_directory()

    def get_output_path(self):
        project_path = self.project_dir
        target_path = os.path.join(project_path, "output")
        return target_path

    def get_input_path(self):
        project_path = self.project_dir
        target_path = os.path.join(project_path, "datasets")
        return target_path

    def get_dataset_path(self, csv_file):
        return os.path.join(self.get_input_path(), csv_file)

    def file_exists_in_project(self, relative_file_path):
        destination_path = os.path.join(self.project_dir, relative_file_path)
        return os.path.exists(destination_path)

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
    def get_project_directory():
        current_path = os.path.dirname(__file__)
        parent_path = os.path.dirname(current_path)
        return parent_path
