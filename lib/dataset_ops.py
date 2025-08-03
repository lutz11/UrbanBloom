import pandas as pd
import os
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from lib.file_ops import FileOps


class DatasetOps():
    def __init__(self, dataset_path):
        file_ops = FileOps()
        self.inputPath = file_ops.get_input_path()
        self.outputPath = file_ops.get_output_path()
        full_path = file_ops.get_dataset_path(dataset_path)
        self.dataset = pd.read_csv(full_path)
        self.dataset_columns = self.get_dataset_columns()
        self.generate_urban_bloom_index()

    def get_dataset_columns(self):
        return self.dataset.columns.tolist()

    def generate_urban_bloom_index(self):
        fileoperator = FileOps()
        relative_path = os.path.join("datasets", "Metro Area Dataset - MAP - Town to Urban Bloom Index.csv")
        if not fileoperator.file_exists_in_project(relative_path):
            WEIGHTS = {"Households - Median income (dollars)": 0.4, "high_earner_percent": 0.4, "log_population": 0.2}
            
            # Creates the features needed for the index calculation.
            high_earner_cols = ['Households - $150,000 to $199,999', 'Households - $200,000 or more']
            self.dataset['high_earner_percent'] = self.dataset[high_earner_cols[0]] + self.dataset[high_earner_cols[1]]
            self.dataset['log_population'] = np.log1p(self.dataset['Population'])
            
            # Select the features that will be part of our index
            features = self.dataset[["Households - Median income (dollars)", "high_earner_percent", "log_population"]]

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
            df = self.dataset.join(scaled_df)

            # Calculate the final UrbanBloom Potential Index using the defined weights
            df["urbanbloom_index"] = (
                    df["norm_median_income"] * WEIGHTS["Households - Median income (dollars)"]
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

    def sort_by_column(self, column_name, ascending=False):
        """
        Sorts the dataset by a given column.
        This is simple because features are created during initialization
        """
        if column_name not in self.dataset.columns:
            raise ValueError(f"Column '{column_name}' not found. Available columns are: {self.get_dataset_columns()}")

        print(f"Sorting by '{column_name}'")
        return self.dataset.sort_values(by=column_name, ascending=ascending)
