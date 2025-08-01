import pandas as pd
import os

from sklearn.preprocessing import MinMaxScaler
from lib.file_ops import FileOps


class DatasetOps():
    def __init__(self, dataset_path):
        self.inputPath = FileOps.get_input_path()
        self.outputPath = FileOps.get_output_path()
        self.dataset = pd.read_csv(self.inputPath)
        self.dataset_columns = self.get_dataset_columns()
        self.generate_urban_bloom_index()

    def get_dataset_columns(self):
        return self.dataset.columns.tolist()

    def generate_urban_bloom_index(self):
        fileoperator = FileOps()
        relative_path = os.path.join("datasets", "Metro Area Dataset - MAP - Town to Urban Bloom Index.csv")
        if not fileoperator.file_exists_in_project(relative_path):

            income_file_path = "Metro Area Dataset - Income by Metro Area.csv"
            df = fileoperator.get_dataset_path(income_file_path)

            WEIGHTS = {"median_income": 0.4, "high_earner_percent": 0.4, "log_population": 0.2}

            # Select the features that will be part of our index
            features = self.dataset[["median_income", "high_earner_percent", "log_population"]]

            # Initialize the MinMaxScaler to scale features between 0 and 1
            scaler = MinMaxScaler()
            scaled_features = scaler.fit_transform(features)

            # Create a new DataFrame with the scaled features
            scaled_df = pd.DataFrame(
                scaled_features,
                columns=[
                    "norm_median_income",
                    "norm_high_earner_percent",
                    "norm_log_population",
                ],
                index=features.index,
            )

            # Join the scaled features back to the original DataFrame
            df = df.join(scaled_df)

            # Calculate the final UrbanBloom Potential Index using the defined weights
            df["urbanbloom_index"] = (
                    df["norm_median_income"] * WEIGHTS["median_income"]
                    + df["norm_high_earner_percent"] * WEIGHTS["high_earner_percent"]
                    + df["norm_log_population"] * WEIGHTS["log_population"]
            )

            # Sort the DataFrame by the new index in descending order
            df_ranked = df.sort_values(by="urbanbloom_index", ascending=False)

            df_ranked.to_csv(os.path.join(self.inputPath, "Metro Area Dataset - Income by Metro Area.csv"))
            return
        else:
            return


    def rename_columns_to_mapping(self, column_rename_map):
        required_original_cols = list(column_rename_map.keys())
        self.dataset = self.dataset[required_original_cols].copy()
        self.dataset = self.dataset.rename(columns=column_rename_map)