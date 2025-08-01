import os

class FileOps:
    def __init__(self):


        @staticmethod
        def get_project_directory():
            current_path = os.path.dirname(__file__)
            parent_path = os.path.dirname(current_path)
            return parent_path

        @staticmethod
        def get_output_path():
            project_path = get_project_directory()
            target_path = os.path.join(project_path, "output")
            return target_path

        @staticmethod
        def get_input_path():
            project_path = get_project_directory()
            target_path = os.path.join(project_path, "datasets")
            return target_path